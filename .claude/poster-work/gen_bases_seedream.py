# -*- coding: utf-8 -*-
"""Seedream (火山方舟) 垫图底图生成器 —— 替代 gen_bases.py 的 SenseNova 后端。

用法:
  python gen_bases_seedream.py <slug> --char asahi-shio [--count 2]
                               [--model doubao-seedream-5-0-flash-260915]
                               [--size 2560x1440] [--theme "..."] [--props "..."]

- 角色原型: characters/<char>/profile.json + prototype.png（垫图保持角色一致性）
- 输出候选图: bases-seedream/<slug>-<序号>.png
- API key: 环境变量 ARK_API_KEY 或 ~/.ark_key（绝不写入项目文件）
- 计费按输出张数（官方约 ¥0.2/张 2K 档），参考图不计费；watermark 已关闭
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

WORK = Path(__file__).parent
API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

# 每个文章主题的道具/姿势描述（新增文章时在这里加一条，或用 --theme/--props 覆盖）
THEMES = {
    "vue3-springboot": dict(
        theme="Vue3 frontend plus SpringBoot backend full-stack AI application development",
        char_pose="standing confidently holding a slim laptop in one arm, looking slightly toward the viewer with a gentle smile",
        props="browser windows, floating UI component cards, a spring-leaf tech badge, API request arrows and a small database cylinder",
    ),
}

PROMPT_TMPL = (
    "Composition: wide 16:9 landscape anime illustration for a technology blog cover. "
    "RIGHT HALF: the girl from the reference image, keep her EXACT hairstyle, hair color, "
    "eye color, face, outfit and art style, {char_pose}, surrounded by floating holographic {props}. "
    "LEFT HALF: keep mostly empty and clean, only a very soft light neutral gradient background "
    "with a subtle grid and faint abstract data lines, strictly no objects and no character on the left third, "
    "reserved for text overlay. "
    "Theme: {theme}. Color accents: {palette}. "
    "Style: high-quality anime illustration, clean line art, detailed hair and clothing, "
    "soft lighting, light particles, subtle glow around the character, professional developer aesthetic. "
    "Strictly avoid: any text, letters, numbers, watermark, logo, signature, dark background, "
    "photorealistic style, vertical composition, clutter on the left side."
)


def load_key() -> str:
    key = os.environ.get("ARK_API_KEY")
    if key:
        return key.strip()
    p = Path.home() / ".ark_key"
    if p.exists():
        return p.read_text(encoding="utf-8").strip()
    sys.exit("[x] 未找到 API key：请设置环境变量 ARK_API_KEY 或创建 ~/.ark_key")


def gen_once(model: str, prompt: str, ref_png: Path, size: str, out: Path, seed: int | None) -> dict:
    ref_b64 = base64.b64encode(ref_png.read_bytes()).decode()
    body = {
        "model": model,
        "prompt": prompt,
        "image": [f"data:image/png;base64,{ref_b64}"],
        "size": size,
        "response_format": "b64_json",
        "watermark": False,
    }
    if seed is not None:
        body["seed"] = seed
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {load_key()}"},
    )
    last_err = None
    for attempt in (1, 2, 3):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                resp = json.loads(r.read().decode("utf-8"))
            break
        except Exception as e:  # 网络/限流抖动重试
            last_err = e
            print(f"  attempt {attempt} failed: {e}", flush=True)
            time.sleep(5 * attempt)
    else:
        raise RuntimeError(f"API 调用失败: {last_err}")

    data = resp.get("data") or []
    if not data or not data[0].get("b64_json"):
        raise RuntimeError(f"响应中没有图片: {json.dumps(resp)[:600]}")
    out.write_bytes(base64.b64decode(data[0]["b64_json"]))
    return resp.get("usage", {})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", help="主题标识，如 vue3-springboot")
    ap.add_argument("--char", default="asahi-shio", help="角色目录名 characters/<char>")
    ap.add_argument("--count", type=int, default=2, help="生成候选图数量")
    ap.add_argument("--model", default="doubao-seedream-5-0-flash-260915",
                    help="默认 flash（15s/张）；重点封面可用 doubao-seedream-5-0-pro-260628")
    ap.add_argument("--size", default="2560x1440", help="16:9 建议 2560x1440，失败可退 2K")
    ap.add_argument("--theme", default=None, help="覆盖 THEMES 里的主题描述")
    ap.add_argument("--props", default=None, help="覆盖道具描述")
    ap.add_argument("--char-pose", default=None, help="覆盖姿势描述")
    args = ap.parse_args()

    char_dir = WORK / "characters" / args.char
    profile = json.loads((char_dir / "profile.json").read_text(encoding="utf-8"))
    ref_png = char_dir / "prototype.png"
    if not ref_png.exists():
        sys.exit(f"[x] 找不到原型图: {ref_png}")

    t = THEMES.get(args.slug, {})
    theme = args.theme or t.get("theme") or sys.exit(f"[x] THEMES 里没有 {args.slug}，请用 --theme 指定")
    props = args.props or t.get("props", "floating technology panels and glowing icons")
    pose = args.char_pose or t.get("char_pose", "standing naturally, looking slightly toward the viewer")

    prompt = PROMPT_TMPL.format(
        char_pose=pose, props=props, theme=theme, palette=profile["palette"]["primary"]
    )
    out_dir = WORK / "bases-seedream"
    out_dir.mkdir(exist_ok=True)
    model_tag = args.model.replace("doubao-seedream-", "")

    total_imgs = 0
    for i in range(1, args.count + 1):
        out = out_dir / f"{args.slug}-{model_tag}-{i}.png"
        print(f"[{i}/{args.count}] {args.model} + {args.char} -> {out.name} ...", flush=True)
        usage = gen_once(args.model, prompt, ref_png, args.size, out, seed=None)
        total_imgs += 1
        print(f"  OK  {out.stat().st_size/1024:.0f}KB  usage={json.dumps(usage, ensure_ascii=False)}", flush=True)
    print(f"\n完成 {total_imgs} 张候选图，目录: {out_dir}")


if __name__ == "__main__":
    main()

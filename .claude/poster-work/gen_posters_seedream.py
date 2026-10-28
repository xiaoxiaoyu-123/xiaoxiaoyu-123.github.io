# -*- coding: utf-8 -*-
"""整张海报一次生成（模仿用户图库海报的设计排版，非 HTML 排版层）。

用法:
  python gen_posters_seedream.py <slug>            # 生成一张候选
  python gen_posters_seedream.py all               # 按 POST_MAP 全量生成

每篇 = 角色垫图（characters/<char>/prototype.png，保人物一致性）
     + 海报风格参考（characters/arikawa-hime/prototype.png 即图库 13.jpg，只学设计语言）
     + 文案来自 configs/<slug>.json（title/slogan/chips）
输出: bases-seedream/poster-<slug>.png（2560×1440，flash ≈15s/张）
角色分配按文章主题与角色色板匹配，见 POST_MAP。
"""
import base64
import json
import sys
import time
import urllib.request
from pathlib import Path

WORK = Path(__file__).parent
API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
# 绕过系统代理直连（方舟在北京，走挂掉的本地代理只会 connection refused）
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
MODEL = "doubao-seedream-5-0-flash-260915"
SIZE = "2560x1440"
STYLE_REF = WORK / "characters/arikawa-hime/prototype.png"  # 图库 13.jpg，设计参考

# slug -> (角色, 封面文件名)；文案读 configs/<slug>.json
POST_MAP = {
    "1panel":        ("leo",           "anime-tech-1panel-20260424.jpg"),
    "css":           ("libra",         "anime-tech-css-20260129.jpg"),
    "git":           ("gemini",        "anime-tech-git-20260321.jpg"),
    "html":          ("aries",         "anime-tech-html-20251014.jpg"),
    "linux":         ("sagittarius",   "anime-tech-linux-20260419.jpg"),
    "markdown":      ("virgo",         "anime-tech-markdown-20251012.jpg"),
    "mysql":         ("aquarius",      "anime-tech-mysql-20260812.jpg"),
    "hexo":          ("asahi-shio",    "anime-tech-hexo-20251011.jpg"),
    "pingjiao":      ("komazawa-noi",  "anime-tech-pingjiao-20260325.jpg"),
    "deploy":        ("taurus",        "anime-tech-deploy-20260325.jpg"),
    "frontend-run":  ("cancer",        "anime-tech-frontend-20260321.jpg"),
    "vue3springboot": ("osawa-mahiro", "anime-tech-vue3springboot-20261019.jpg"),
    "404":           ("cancer",       "anime-tech-404-20261028.jpg"),
    "blog-refactor":  ("aquarius",     "anime-tech-blogrefactor-20261027.jpg"),
}

PROMPT_TMPL = """WIDE 16:9 LANDSCAPE anime technology recommendation poster for a Chinese programming blog cover.
Reference image 1 = THE ONLY CHARACTER IDENTITY SOURCE, and the only character allowed in the poster. She has {appearance}. The girl in the poster MUST be exactly this character: same hairstyle, same hair color, same eye color, same outfit, same art style. Do NOT invent any other character.
Place her on the RIGHT side of the frame, standing, smiling cheerfully, one hand gesturing toward the title, occupying about 60% of the frame height.
Reference image 2 = DESIGN STYLE reference ONLY (ignore its character and its text): imitate its design language — soft pastel gradient background, big bold rounded Chinese title typography, rounded info cards with small cute icons — but in 16:9 landscape composition.
All Chinese text and English words must be rendered EXACTLY as given, correctly spelled:
- Huge main title (upper left): {title}
- Small subtitle under it: {slogan}
- {chip_count} small rounded chip tags: {chips}
Decoration: tiny hearts, stars and sparkles; one small speech bubble containing only a heart symbol, no text inside the bubble. NO bottom info bar, NO extra text blocks anywhere.
Color theme: {palette}, light clean background, cute but professional.
Strictly no other text, no watermark, no logo, no extra English words beyond the technology names above."""


def load_key() -> str:
    import os
    key = os.environ.get("ARK_API_KEY")
    if key:
        return key.strip()
    return (Path.home() / ".ark_key").read_text(encoding="utf-8").strip()


def gen(slug: str) -> Path:
    char_en, _cover = POST_MAP[slug]
    cfg = json.loads((WORK / "configs" / f"{slug}.json").read_text(encoding="utf-8"))
    profile = json.loads((WORK / "characters" / char_en / "profile.json").read_text(encoding="utf-8"))
    chips = [str(c) for c in cfg["chips"]][:4]
    prompt = PROMPT_TMPL.format(
        title=cfg["title"], slogan=cfg["slogan"], chip_count=len(chips),
        chips=" / ".join(chips), palette=profile["palette"]["primary"],
        appearance=profile["appearance"],
    )
    refs = [
        (WORK / "characters" / char_en / "prototype.png").read_bytes(),
        STYLE_REF.read_bytes(),
    ]
    body = {
        "model": MODEL,
        "prompt": prompt,
        "image": [f"data:image/png;base64,{base64.b64encode(r).decode()}" for r in refs],
        "size": SIZE,
        "response_format": "b64_json",
        "watermark": False,
    }
    req = urllib.request.Request(
        API_URL, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {load_key()}"},
    )
    out = WORK / "bases-seedream" / f"poster-{slug}.png"
    for attempt in (1, 2, 3):
        try:
            with OPENER.open(req, timeout=300) as r:
                resp = json.loads(r.read().decode("utf-8"))
            break
        except Exception as e:
            print(f"  attempt {attempt} failed: {e}", flush=True)
            time.sleep(5 * attempt)
    else:
        raise RuntimeError(f"{slug} 生成失败")
    out.write_bytes(base64.b64decode(resp["data"][0]["b64_json"]))
    print(f"[ok] {out.name}  {out.stat().st_size//1024}KB  char={char_en}", flush=True)
    return out


def main() -> None:
    (WORK / "bases-seedream").mkdir(exist_ok=True)
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    slugs = list(POST_MAP) if arg == "all" else [arg]
    for s in slugs:
        print(f"[{s}] generating ...", flush=True)
        try:
            gen(s)
        except Exception as e:
            print(f"[FAIL] {s}: {e}", flush=True)


if __name__ == "__main__":
    main()

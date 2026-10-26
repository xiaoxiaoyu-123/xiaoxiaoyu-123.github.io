# -*- coding: utf-8 -*-
"""一次性工具：把 C:/Users/xinan/Pictures/二次元高清图 的 21 张图登记进角色库。

产生 characters/<en>/prototype.png + profile.json，以及 characters/index.json 总目录。
用户以后在图库新增图片时，可以往 CATALOG 里加条目重跑本脚本（已存在的目录会跳过）。
"""
import json
import shutil
from pathlib import Path

SRC = Path(r"C:/Users/xinan/Pictures/二次元高清图")
WORK = Path(__file__).parent
CHARS = WORK / "characters"
IP_NOTE = "⚠️ 现有作品角色（版权角色）：仅建议个人非商用博客低调使用，不要作为站点主力形象"

CATALOG = [
    # file, en, 中文名, appearance, personality, palette(primary, secondary), suit_for, ip
    ("1.png", "asahi-shio", "有川汐 / Asahi Shio（双鱼座）",
     "long wavy pastel-pink hair with a shell hair ornament, gentle blue eyes, white sailor collar shirt under a light blue cardigan, plaid pastel skirt",
     "温柔、安静、治愈", ("soft pink and pastel blue", "pale lavender"),
     "前端 / CSS / 设计 / 生活随笔（粉色系）", False),
    ("2.png", "aries", "艾丽丝 / Aries（白羊座）",
     "long peach-orange side ponytail with white ram-horn hair accessories, red eyes, cream school blazer over red plaid skirt and red ribbon, red school bag; energetic pose",
     "热血、直率、元气", ("warm coral red and cream", "soft peach"),
     "热血鼓励、入门动员、运动向内容（暖橙红）", False),
    ("3.png", "libra", "天秤诗澜 / Libra（天秤座）",
     "long wavy light-ash hair with pink ribbons and flower clips, gentle pink-brown eyes, lavender blazer over cream knit vest and pink-grey plaid skirt, small chain bag",
     "温柔、优雅、和平", ("lavender pink and soft grey", "cream gold"),
     "设计审美、对比评测、优雅主题（粉紫灰）", False),
    ("4.png", "cancer", "海汐 / Cancer（巨蟹座）",
     "long wavy silver-white hair with pearl and shell hairpins, soft blue eyes, fluffy white cardigan over pale blue chiffon layered skirt, hugging a pink crab plushie",
     "温柔、守护、慢热", ("moonlight white and pale blue", "soft pink"),
     "治愈随笔、情感文章、睡前向内容（月白蓝）", False),
    ("5.png", "leo", "莉欧 / Leo（狮子座）",
     "long wavy golden-blonde hair with a dark red ribbon, warm amber eyes, cream school blazer with gold buttons over a knit vest, red bow tie, plaid brown skirt, brown school bag",
     "自信、阳光、有领导力", ("warm gold and deep red", "cream and amber"),
     "Linux / 部署 / 系统类（暖色系）", False),
    ("6.png", "gemini", "岚染 / Weyoung（双子座）",
     "ash-blonde twin tails with blue ribbons and star clips, blue eyes, white jacket over pale yellow vest and white pleated skirt, holding a notebook; peace sign",
     "灵动、机敏、话痨", ("sky blue and pale yellow", "white"),
     "轻松闲聊、工具分享、对比类文章（蓝黄）", False),
    ("7.png", "sagittarius", "星野惠乃 / Hoshino Sena（射手座）",
     "light brown high ponytail with star hairpins, amber eyes, dark brown school blazer with wine-red bow tie and brown plaid skirt, holding a red passport, leather school bag",
     "自由、乐观、冒险", ("warm brown and deep red", "gold"),
     "旅行见闻、探索新工具、成长记录（棕金）", False),
    ("8.png", "aquarius", "艾瑞丝·Aria / Aquarius（水瓶座）",
     "long straight ice-blue hair with crystal flower ornaments, pale blue eyes, white jacket over blue vest dress and blue-grey plaid skirt, holding a dark blue notebook",
     "自由、理性、创新", ("ice blue and white", "silver"),
     "前沿技术、新概念科普、理性评测（冰蓝白）", False),
    ("9.png", "virgo", "禾澄 / Wojuang（处女座）",
     "long straight ash-brown hair with a green check ribbon, calm brown eyes, beige blazer over green knit vest and grey-green plaid skirt, holding a green book",
     "细致、理性、温柔", ("sage green and beige", "grey"),
     "整理控、方法论、清单类文章（米绿灰）", False),
    ("10.png", "taurus", "暖禾 / Nosane（金牛座）",
     "long wavy ash-brown hair with small bull horns and a flower crown, warm brown eyes, cream knit cardigan over white blouse and long taupe skirt, holding a flower bouquet and books",
     "温和、踏实、治愈", ("milk-tea brown and cream", "soft sage green"),
     "生活方式、笔记软件、慢节奏教程（奶咖绿）", False),
    ("11.png", "scorpio", "塞珊娜 / Selera（天蝎座）",
     "long wavy black-purple hair with black ribbons and chains, purple eyes, black choker, cropped black jacket over dark purple plaid skirt, thigh strap and black boots",
     "神秘、酷感、忠诚", ("black and deep purple", "wine red"),
     "深度技术、进阶硬核、逆向思维内容（黑紫）", False),
    ("13.jpg", "arikawa-hime", "有川姬 / Arikawa Hime",
     "twin pink tails with red ribbons, blue eyes, school uniform with red bow tie and cream knit vest, red armband; bright idol mood",
     "元气、推荐官、亲切", ("pink and red", "white"),
     "入门推荐、C 语言类主题（粉红）", False),
    ("14.jpg", "komazawa-noi", "驹泽乃依 / Komazawa Noi",
     "long black hair with pink streaks, cat ears with a pink paw accessory, striped cat tail, pink-black kimono-inspired dress with a big pink bow",
     "酷炫、猫系、自信", ("black and pink", "grey"),
     "高性能、硬核进阶主题（黑粉）", False),
    ("15.jpg", "sakuraba-emma", "樱羽艾玛 / Sakuraba Emma",
     "short silver-white hair with pink tips, black beret with cherry blossom, red eyes, black gothic-lolita coat with white frills and sakura accents",
     "安静、优雅、樱花", ("black and sakura pink", "white"),
     "优雅现代、跨平台主题（黑白粉）", False),
    ("16.jpg", "osawa-mahiro", "绪山真寻 / Osawa Mahiro",
     "very long pastel-pink straight hair, warm brown eyes, light blue oversized tee dress with a red name tag, peace sign",
     "元气、治愈、可靠", ("pastel pink and sky blue", "white"),
     "安全可靠、友好入门主题（粉蓝）", False),
    ("17.jpg", "venti", "温迪 / Venti",
     "dark blue-black twin braids with teal tips, green beret with a white flower, bard cape outfit holding a lyre",
     "自由、吟游、灵动", ("teal green and white", "gold"),
     "音乐/创意类主题", True),
    ("18.jpg", "hatsune-miku", "初音未来 / Hatsune Miku",
     "very long teal twin tails, grey-white shirt with teal tie, black arm sleeves, black skirt with teal trim",
     "活力、歌姬、未来感", ("teal and grey", "black"),
     "JS / 创意编程类主题", True),
    ("19.jpg", "hirasawa-yui", "平泽唯 / Hirasawa Yui",
     "short brown hair with a yellow hairpin, amber eyes, navy school blazer, holding an electric guitar",
     "天然、元气、 音乐", ("navy blue and warm brown", "cream"),
     "Web 开发 / 轻松入门主题", True),
    ("20.jpg", "astolfo", "阿斯托尔福 / Astolfo",
     "pink braided hair with a black headband and small crown, black-red knight outfit with fur-trimmed cape and a sword",
     "开朗、骑士、热血", ("pink and deep red", "black"),
     "企业级 / 严肃技术主题的反差萌", True),
    ("21.jpg", "yukinoshita-yukino", "雪之下雪乃 / Yukinoshita Yukino",
     "long straight black hair, blue-grey eyes, pale blue kimono-style haori over white, holding a folded fan; cool elegant mood",
     "清冷、学霸、完美主义", ("pale blue and white", "grey"),
     "科学计算 / 学术向主题", True),
]


def main() -> None:
    roster = []
    for fname, en, name, appearance, personality, palette, suit_for, ip in CATALOG:
        src = SRC / fname
        if not src.exists():
            print(f"[skip] 原图不存在: {src}")
            continue
        cdir = CHARS / en
        proto = cdir / "prototype.png"
        if not proto.exists():
            cdir.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, proto)
        profile = {
            "name": name,
            "en_name": en,
            "source": f"C:/Users/xinan/Pictures/二次元高清图/{fname}（已拷贝为 prototype.png）",
            "appearance": appearance,
            "personality": personality,
            "palette": {"primary": palette[0], "secondary": palette[1]},
            "suit_for": suit_for,
        }
        if ip:
            profile["note"] = IP_NOTE
        (cdir / "profile.json").write_text(
            json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        roster.append({
            "en": en, "name": name,
            "palette_primary": palette[0], "suit_for": suit_for, "ip": ip,
        })
        print(f"[ok] {en:<20} {name}")

    # 十二星座合照：不是单一角色，留作专题/年度总结封面的合影参考图
    group_src = SRC / "12.png"
    if group_src.exists():
        shutil.copyfile(group_src, WORK / "ref-zodiac-group.png")
        print("[ok] ref-zodiac-group.png（十二星座全员合照，不作为单角色垫图）")

    (CHARS / "index.json").write_text(
        json.dumps({"count": len(roster), "characters": roster}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n角色库完成：{len(roster)} 个角色，总目录 characters/index.json")


if __name__ == "__main__":
    main()

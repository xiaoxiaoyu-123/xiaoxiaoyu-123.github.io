# -*- coding: utf-8 -*-
"""补齐主题配置引用但缺失的图片（阶段一任务）。

favicon   <- 头像 tx01.jpg 中心裁方
bg03-06   <- Suzume-Travel 03~06 裁 2.5:1 横幅（归档/标签/分类页 banner）
404.jpg   <- Miku05 裁 8:5 加「404」字样（文章图片挂掉时的占位）
friend_404.gif <- Miku02 裁方图加字（友链卡片挂掉时的占位）
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

IMG = Path(r"C:/Users/xinan/my-blog/source/img")
FONT = "C:/Windows/Fonts/msyhbd.ttc"


def center_crop(im, ratio):
    """按目标宽高比中心裁剪，ratio = 宽/高"""
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio)
        box = ((w - nw) // 2, 0, (w - nw) // 2 + nw, h)
    else:
        nh = int(w / ratio)
        box = (0, (h - nh) // 2, w, (h - nh) // 2 + nh)
    return im.crop(box)


def banner(src, out, size=(1500, 600)):
    im = Image.open(src).convert("RGB")
    im = center_crop(im, size[0] / size[1]).resize(size, Image.LANCZOS)
    im.save(out, quality=85)
    print(f"[ok] {out.name} <- {Path(src).name} {im.size}")


def with_text(im, text, size_px, xy, fill=(255, 255, 255)):
    d = ImageDraw.Draw(im)
    d.text(xy, text, font=ImageFont.truetype(FONT, size_px), fill=fill,
           anchor="mm", stroke_width=3, stroke_fill=(90, 90, 110))
    return im


# 1. favicon：头像中心裁方 → 128
im = Image.open(IMG / "tx01.jpg").convert("RGB")
center_crop(im, 1).resize((128, 128), Image.LANCZOS).save(IMG / "favicon.png")
print("[ok] favicon.png <- tx01.jpg 128x128")

# 2. 页面横幅 bg03-06
pairs = [
    ("Suzume-Travel 03.jpg", "bg03.jpg"),
    ("Suzume-Travel 04.jpg", "bg04.jpg"),
    ("Suzume-Travel 05.jpg", "bg05.jpg"),
    ("Suzume-Travel 06.jpg", "bg06.jpg"),
]
for src, out in pairs:
    banner(IMG / src, IMG / out)

# 3. 404 占位图
im = Image.open(IMG / "Miku05.jpg").convert("RGB")
im = center_crop(im, 8 / 5).resize((800, 500), Image.LANCZOS)
with_text(im, "404", 120, (400, 210))
with_text(im, "图片去潜水了…", 34, (400, 330))
im.save(IMG / "404.jpg", quality=85)
print("[ok] 404.jpg <- Miku05.jpg 800x500")

# 4. 友链失效占位（单帧 GIF）
im = Image.open(IMG / "Miku02.jpg").convert("RGB")
im = center_crop(im, 1).resize((400, 400), Image.LANCZOS)
with_text(im, "链接失效啦", 36, (200, 330))
im.convert("P", palette=Image.ADAPTIVE).save(IMG / "friend_404.gif")
print("[ok] friend_404.gif <- Miku02.jpg 400x400")

# -*- coding: utf-8 -*-
"""Clean garbled text & watermark from AI base art via feathered clone patches.

Usage: python clean_base.py <in_png> <out_png>
"""
import sys
from PIL import Image, ImageFilter, ImageDraw


def _mask(w, h):
    """Feather ring: solid core, ~24px fade to zero at the box edge.

    The fade is why patch boxes must be sized so their outer ~24px lands on
    pixels that are already clean -- those edge pixels are never overwritten.
    """
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rectangle((14, 14, w - 14, h - 14), fill=255)
    return mask.filter(ImageFilter.GaussianBlur(10))


def feathered_paste(im, box, offset):
    """Clone region box shifted by offset, paste back with feathered edges."""
    x0, y0, x1, y1 = box
    ox, oy = offset
    src = im.crop((x0 + ox, y0 + oy, x1 + ox, y1 + oy))
    src = src.filter(ImageFilter.GaussianBlur(2))
    im.paste(src, (x0, y0), _mask(x1 - x0, y1 - y0))


def main(inp, outp):
    im = Image.open(inp).convert("RGB")

    # A1: garbled English headline. Source band (y+470) stops at x=1520 so it
    # never touches the purple server cube whose left edge sits near x=1525.
    feathered_paste(im, (60, 60, 1520, 440), (0, 470))
    # A2: "ablog" tail past A1's right edge. Runs AFTER A1 and clones from
    # x-280, i.e. out of the already-cleaned patch -- at these y's every
    # un-cleaned x still carries glyphs, so a neighbour source would re-import
    # them through this patch's own feather ring.
    # Height stops at y=300: below that the team/database icon panel begins
    # (top edge ~y310) and this patch would shear its corner off. The 'g'
    # descender runs to y~255, so the solid core must reach past y~276.
    feathered_paste(im, (1450, 60, 1680, 300), (-280, 0))
    # B: watermark block (logo + "日日新 sensenova", x2440-2730 y1384-1481) is
    # DELIBERATELY left alone. It overlaps the hoodie's lower-right edge, and
    # every clone we tried either duplicated that edge (vertical offset) or
    # clipped it (horizontal offset) -- the silhouette shape simply is not
    # reproducible from a neighbouring band. The poster covers y>=1380 with its
    # opaque bottom info bar, which is why the watermark is harmless here.

    im.save(outp, "PNG")
    print(f"cleaned -> {outp}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

# -*- coding: utf-8 -*-
"""Strip AI-generated garbage text from a base illustration.

Usage: python clean.py <in_png> <out_png> [x0 y0 x1 y1]

The image model reliably ignores "no text" and stamps a fake Latin headline over
the left third. Text is dark-on-light, so it can be located by comparing every
pixel against a stroke-free estimate of its neighbourhood: a median erases thin
dark strokes and returns the background, and the difference lights up exactly
where ink is.

Two thresholds do the separating, both measured on the 1Panel base rather than
guessed:
  * contrast. Headline ink runs ~230 levels darker than the background; the
    decorative dot grid peaks near 78. DARK=70 finds text bands; INK=4 catches
    the antialiased rim as well.
  * row density, counted over the left 1500 columns only. A text line inks ~15%
    of its row. The floating server rack sits at x>=1518 and reads as 33%, but
    it contributes nothing to those columns, so it never forms a band. Each
    band's horizontal extent still comes from the full mask, which is what keeps
    the far-right end of a headline covered.

Repair is cv2.inpaint over the ink mask, grown by INPAINT_DILATE so the rim goes
too, and confined to each band's box: a whole-panel pass would also erase the
art's border frame and dot grid, leaving a visible break where the frame line
stops mid-image. In practice 8 of the 10 batch images come back with no bands at
all -- the model only garbles the headline on some of them -- so "no text
detected" is a normal result, not a threshold failure.

Three approaches were tried and rejected before this one:
  * Re-interpolating each column between the clean rows above and below the
    text. Impossible here: measured over the left panel, only 105 of 1360 rows
    are ink-free at all, and none below y=343, so there is no clean row to
    anchor on. The fill starts from ink and fades out as a vertical ghost.
  * A max filter as the estimate. It reads the brightest pixel in the kernel,
    which over the panel's gradient sits ~30 levels above the local background,
    so repair fires on clean pixels too and repaints the text area as glowing
    white ghosts.
  * Blending each inked pixel toward that median. Statistically it lands within
    a level of the surrounding background, but it is a per-pixel statistic, so
    it leaves a ~2-level error shaped like the letters. Human vision reads
    coherent low-contrast shapes long before it reads noise, and the glyphs stay
    legible in the result.

The bottom-right sensenova watermark is deliberately not handled here: it is
light-on-dark and sits on the character's hoodie. It is at y>=1384, under the
poster's opaque bottom bar (y>=1380), which is what actually removes it.
"""
import sys

import cv2
import numpy as np
from PIL import Image

SEARCH = (0, 0, 1800, 1440)  # scanned for ink; below this the poster bar covers everything
DENSITY_X1 = 1500            # density counts only these columns (excludes props)
DARK = 70                    # levels darker than local background to count as ink
MEDIAN = 101                 # background-estimate kernel; must exceed 2x stroke width
ROW_FRAC = 0.15              # share of a row that must be ink to be a text line
MIN_ROWS = 4                 # ignore speckle
VALUE_MAX = 130              # headline ink is near-black; art panels are vivid
PAD = 10                     # grow each band's box before repairing
GAP = 60                     # column gap that ends a text run (word spaces are ~30)
EXPAND_MAX = 40              # how far a band may grow to reach sparse glyph tops
SMOOTH = 301                 # large-scale background, for deciding if a ring is flat
FLAT = 18                    # allowed deviation from that large-scale background


def background_estimate(arr: np.ndarray, size: int) -> np.ndarray:
    """Per-channel median, as a stroke-free estimate of the background.

    A max filter is not usable here: it returns the brightest pixel in the
    kernel, which over the panel's gradient reads ~30 levels above the local
    background, so the ink mask fires on clean pixels too.
    """
    if arr.ndim == 2:
        return cv2.medianBlur(arr, size)
    return np.stack([cv2.medianBlur(arr[:, :, c], size) for c in range(arr.shape[2])],
                    axis=2)


def find_bands(mask: np.ndarray):
    """Group consecutive ink-dense rows into (y_start, y_end) bands."""
    density = mask[:, :DENSITY_X1].sum(axis=1) / float(DENSITY_X1)
    hot = density > ROW_FRAC
    bands, start = [], None
    for y, is_hot in enumerate(hot):
        if is_hot and start is None:
            start = y
        elif not is_hot and start is not None:
            if y - start >= MIN_ROWS:
                bands.append((start, y - 1))
            start = None
    if start is not None and len(hot) - start >= MIN_ROWS:
        bands.append((start, len(hot) - 1))
    return bands


def band_box(mask: np.ndarray, flat: np.ndarray, by0: int, by1: int, h: int, w: int):
    """Turn a dense-row band into the box that actually needs repairing."""
    rows = mask[by0:by1 + 1]
    # Pick columns by how much ink they carry, not by "any ink at all". A glyph
    # stem fills most of the band's height; the art's thin frame lines put two
    # or three pixels in a column. Plain .any() therefore stretches the box
    # rightward onto frame lines and floating panels, and repairing their edges
    # smears them.
    cols = np.where(rows.sum(axis=0) >= max(2, 0.04 * (by1 - by0 + 1)))[0]
    if cols.size == 0:
        return None
    ca, cb = int(cols.min()), int(cols.max()) + 1
    # Grow to the real ink extent. The density threshold finds the band's core,
    # but a tall glyph's ascenders and serifs ink too few pixels per row to clear
    # it -- left outside the box they survive as outlines. Bounded by EXPAND_MAX
    # because the art's own left border line runs the full height and would
    # otherwise make every row look inked.
    steps = 0
    while by0 > 0 and steps < EXPAND_MAX and mask[by0 - 1, ca:cb].any():
        by0 -= 1
        steps += 1
    steps = 0
    while by1 < h - 1 and steps < EXPAND_MAX and mask[by1 + 1, ca:cb].any():
        by1 += 1
        steps += 1
    cols = np.where(mask[by0:by1 + 1].sum(axis=0)
                    >= max(2, 0.04 * (by1 - by0 + 1)))[0]
    # Cut the run at the first wide gap. Letters and words sit close together;
    # the character or a floating panel is hundreds of pixels away, so stopping
    # there keeps the box off the character instead of dragging it to x=1759.
    gaps = np.where(np.diff(cols) > GAP)[0]
    ca, cb = int(cols.min()), int(cols[gaps[0]] if gaps.size else cols.max()) + 1
    ya, yb = max(by0 - PAD, 0), min(by1 + PAD + 1, h)
    xa, xb = max(ca - PAD, 0), min(cb + PAD, w)

    # Push the box up and down until the ring just outside is flat *across the
    # text's own columns*. The fill reads its two anchor rows from the original
    # image, so a box edge on ink makes the fill start from that colour and fade
    # -- the vertical tail. The test is `flat`, not `mask`: a wide soft shadow
    # under a headline is large enough that the median window lands inside it,
    # so diff collapses and `mask` calls it background though it is ~100 levels
    # too dark. Only the vertical edges need this: the fill is a per-column
    # interpolation, so left and right edges are never sampled. Testing the full
    # padded width instead would keep the loop alive on far-away artwork until
    # its budget ran out, leaving the anchor stuck inside the glyphs.
    for _ in range(2 * EXPAND_MAX + PAD):
        moved = False
        if ya > 0 and not flat[ya - 1, ca:cb].all():
            ya -= 1
            moved = True
        if yb < h and not flat[yb, ca:cb].all():
            yb += 1
            moved = True
        if not moved:
            break
    return xa, ya, xb, yb


def clean(inp: str, outp: str, search=SEARCH) -> list:
    im = Image.open(inp).convert("RGB")
    x0, y0, x1, y1 = search
    x1, y1 = min(x1, im.width), min(y1, im.height)
    region = im.crop((x0, y0, x1, y1))
    h, w = region.height, region.width

    arr = np.asarray(region)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    gmed = background_estimate(gray, MEDIAN)
    diff = (gmed.astype(np.int16) - gray.astype(np.int16)).astype(np.float32)

    # Headline ink is near-black; the art's floating panels are vivid, so their
    # pixels sit high in V even where they are dark in blue. Without this the
    # box stretches right onto a swatch panel and repairing its edges smears it.
    value = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV)[:, :, 2]
    text = (diff > DARK) & (value < VALUE_MAX)

    smooth = cv2.medianBlur(gray, SMOOTH).astype(np.int16)
    flat = np.abs(gray.astype(np.int16) - smooth) <= FLAT

    out = arr.copy()
    found = []
    for by0, by1 in find_bands(text):
        box = band_box(text, flat, by0, by1, h, w)
        if box is None:
            continue
        xa, ya, xb, yb = box

        # Fill by interpolating vertically between the two clean rows that bound
        # the box. This only became possible once band_box grew the box until its
        # ring was ink-free -- with inky anchors the fill starts from glyph
        # colour and fades, leaving a vertical tail. Because each column keeps
        # its own colour, a horizontal gradient survives untouched.
        #
        # cv2.inpaint was tried here and is worse at this size: it propagates
        # boundary colours along the glyph directions and smears them, so tall
        # letter stems came back as grey streaks even though the box was fully
        # masked and its boundary clean.
        top = arr[(ya - 1) if ya > 0 else ya, xa:xb].astype(np.float32)
        bot = arr[(yb if yb < h else yb - 1), xa:xb].astype(np.float32)
        t = np.linspace(0.0, 1.0, yb - ya).astype(np.float32)[:, None, None]
        out[ya:yb, xa:xb] = top[None] * (1.0 - t) + bot[None] * t
        found.append((x0 + xa, y0 + ya, x0 + xb, y0 + yb))

    im.paste(Image.fromarray(out), (x0, y0))
    im.save(outp, "PNG")
    return found


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    search = tuple(int(v) for v in argv[3:7]) if len(argv) >= 7 else SEARCH
    found = clean(argv[1], argv[2], search)
    print(f"cleaned -> {argv[2]}")
    for xa, ya, xb, yb in found:
        print(f"   repaired x{xa}-{xb} y{ya}-{yb}")
    if not found:
        print("   (no text detected)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

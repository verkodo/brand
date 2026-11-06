#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Generates the verkodo brand kit: master SVGs, PNG exports, favicon.ico and the website's head icons.

The mark is ⊨ ∎: the double turnstile of logic ("is true" – vero) and the tombstone that ends a proof. The two bars of
⊨ cut into ∎ as notches – the truth is carried into the proof. Everything sits on one unit: stem, bars and the gap
between them are one unit, the bars run two units up to ∎, ∎ is five units (four in the small variant for 16–48 px,
on a coarser unit, so the notches stay open). The notches are cut out of ∎, not painted, so the mark also works in
one colour and on any ground. One colour beside the face: titanium grey.

The wordmark and all text are set in Crimson Pro (fonts/, SIL OFL 1.1) and converted to outlines, so they need no font
where they are shown. The name is always lowercase.

Needs rsvg-convert (Homebrew: librsvg) and fontTools (pip install fonttools). Run from anywhere:
    python3 generate.py
Edit this file, not the exports; brandkit.py (the export) stays as it is.
"""
import os

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from brandkit import export, svg

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "verkodo"
TAGLINE = "Truth code – mathematics and law written formally, checked by machine"

NIGHT = "#0D1117"         # near-black – dark ground
PAPER = "#E6EDF3"         # face (strokes, text) on dark
INK = "#14202B"           # face on light
TITAN = "#8F959B"         # the one colour beside the face, on dark (6.3 : 1 on NIGHT)
TITAN_DARK = "#646A70"    # titanium on light grounds (5.0 : 1 on SHEET)
SHEET = "#F7F4EC"         # warm paper – light ground

DARK = dict(face=PAPER, accent=TITAN)
LIGHT = dict(face=INK, accent=TITAN_DARK)

# --- mark (drawn in a 100×100 box) -----------------------------------------------------------------------------------

MARK_BOX = "0 0 100 100"


def mark_parts(unit=11.0, q=5, notch=1):
    """⊨ and the notched ∎ as two path strings, centred in the 100 box: (face, accent)."""
    u, Q, P = unit, q * unit, notch * unit
    h = max(6, q + 2) * u                     # the stem: one unit above and below ∎
    x = 50 - (3 * u + Q) / 2                  # stem, two units of bar, ∎
    sx, y0, y1 = x + 3 * u, 50 - Q / 2, 50 + Q / 2
    t1, b1, t2, b2 = 50 - 1.5 * u, 50 - 0.5 * u, 50 + 0.5 * u, 50 + 1.5 * u   # the two bars
    n = lambda v: f"{v:.2f}".rstrip("0").rstrip(".")
    face = (f"M{n(x)},{n(50 - h / 2)}h{n(u)}v{n(h)}h{n(-u)}Z"
            f"M{n(x + u)},{n(t1)}h{n(2 * u)}v{n(u)}h{n(-2 * u)}Z"
            f"M{n(x + u)},{n(t2)}h{n(2 * u)}v{n(u)}h{n(-2 * u)}Z")
    proof = (f"M{n(sx)},{n(y0)}H{n(sx + Q)}V{n(y1)}H{n(sx)}V{n(b2)}H{n(sx + P)}V{n(t2)}H{n(sx)}"
             f"V{n(b1)}H{n(sx + P)}V{n(t1)}H{n(sx)}Z")
    return face, proof


def mark(p=DARK, small=False):
    face, proof = mark_parts(12.5, 4) if small else mark_parts()
    return f'<path d="{face}" fill="{p["face"]}"/><path d="{proof}" fill="{p["accent"]}"/>'


def flat_mark(color):
    return mark(dict(face=color, accent=color))


def placed(body, cx, cy, width, box=100):
    k = width / box
    return f'<g transform="translate({cx} {cy}) scale({k:.4f}) translate({-box / 2} {-box / 2})">{body}</g>'


def icon(rounded=True, small=False):
    r = 160 if rounded else 0
    return svg("0 0 1024 1024", f'<rect width="1024" height="1024" rx="{r}" fill="{NIGHT}"/>'
               + placed(mark(small=small), 512, 512, 820 if small else 740))


# --- text as outlines (Crimson Pro; baseline y=0, x-height XH) --------------------------------------------------------

FONTS = {w: os.path.join(HERE, "fonts", f"CrimsonPro-{w}.ttf") for w in ("SemiBold", "Regular")}
_FONTS = {}


def font(weight):
    if weight not in _FONTS:
        f = TTFont(FONTS[weight])
        _FONTS[weight] = (f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    return _FONTS[weight]


def text_path(text, size, weight="SemiBold"):
    """The text as one path (font size `size`, baseline y=0) and its advance width."""
    gs, cmap, hmtx, em = font(weight)
    k, x, d = size / em, 0.0, []
    for ch in text:
        g = cmap[ord(ch)]
        sp = SVGPathPen(gs)
        gs[g].draw(TransformPen(sp, (k, 0, 0, -k, x, 0)))
        d.append(sp.getCommands())
        x += hmtx[g][0] * k
    return "".join(d), x


def text_bounds(text, size, weight="SemiBold"):
    """Ink bounds (x0, top, x1, bottom) of the text, y down, baseline 0."""
    gs, cmap, hmtx, em = font(weight)
    k, x, box = size / em, 0.0, None
    for ch in text:
        g = cmap[ord(ch)]
        bp = BoundsPen(gs)
        gs[g].draw(bp)
        if bp.bounds:
            a, b, c, e = bp.bounds
            r = (x + a * k, -e * k, x + c * k, -b * k)
            box = r if box is None else (min(box[0], r[0]), min(box[1], r[1]), max(box[2], r[2]), max(box[3], r[3]))
        x += hmtx[g][0] * k
    return box


def text(t, size, x, y, fill, weight="SemiBold"):
    d, _ = text_path(t, size, weight)
    return f'<path transform="translate({x:.2f} {y:.2f})" d="{d}" fill="{fill}"/>'


# --- wordmark and lockup ----------------------------------------------------------------------------------------------

SIZE = 100                                     # font size of the wordmark


def wordmark_body(p=DARK):
    """The name in Crimson Pro SemiBold as outlines, baseline y=0. Returns the body and its ink bounds."""
    d, _ = text_path(NAME, SIZE)
    return f'<path d="{d}" fill="{p["face"]}"/>', text_bounds(NAME, SIZE)


def wordmark(p=DARK):
    body, (x0, top, x1, bottom) = wordmark_body(p)
    pad = 8
    return svg(f"{x0 - pad:.1f} {top - pad:.1f} {x1 - x0 + 2 * pad:.1f} {bottom - top + 2 * pad:.1f}", body)


def lockup_body(p=DARK):
    """Mark and wordmark: the stem of ⊨ runs from the ascender of k down to the baseline. Returns body and bounds."""
    body, (x0, top, x1, bottom) = wordmark_body(p)
    asc = -text_bounds("k", SIZE)[1]
    width = asc / 0.77 * 1.0                  # the stem is 77 of the 100 box
    cx, cy = -width * 0.44 - SIZE * 0.2, -asc / 2   # ∎ ends 0.2 em before the v
    return placed(mark(p), cx, cy, width) + body, (cx - width * 0.44, top, x1, max(bottom, cy + width / 2))


def lockup(p=DARK):
    body, (x0, top, x1, bottom) = lockup_body(p)
    pad = 8
    return svg(f"{x0 - pad:.1f} {top - pad:.1f} {x1 - x0 + 2 * pad:.1f} {bottom - top + 2 * pad:.1f}", body)


# --- social preview, favicon ------------------------------------------------------------------------------------------

def social():
    """1280×640: GitHub social preview, link previews."""
    lines = TAGLINE_LINES
    tag = "".join(text(line, 36, 470, 400 + i * 46, PAPER, "Regular") for i, line in enumerate(lines))
    body, _ = wordmark_body(DARK)
    return svg("0 0 1280 640", f'<rect width="1280" height="640" fill="{NIGHT}"/>'
               + placed(mark(), 260, 300, 270)
               + f'<g transform="translate(466 318) scale(1.5)">{body}</g>'
               + tag
               + text("free software · a falkOSS project", 26, 470, 410 + len(lines) * 46 + 18, TITAN, "Regular"),
               (1280, 640))


TAGLINE_LINES = ["Truth code – mathematics and law", "written formally, checked by machine"]
assert " ".join(TAGLINE_LINES) == TAGLINE


def favicon():
    """The small mark, transparent: paper and titanium on dark tabs, ink and dark titanium on light ones."""
    face, proof = mark_parts(12.5, 4)
    style = (f'<style>.f{{fill:{PAPER}}}.a{{fill:{TITAN}}}'
             f'@media (prefers-color-scheme: light){{.f{{fill:{INK}}}.a{{fill:{TITAN_DARK}}}}}</style>')
    return svg(MARK_BOX, style + f'<path class="f" d="{face}"/><path class="a" d="{proof}"/>')


def main():
    kit = {
        "icon": icon(),
        "icon-square": icon(rounded=False),
        "icon-small": icon(small=True),
        "mark-on-dark": svg(MARK_BOX, mark(DARK)),
        "mark-on-light": svg(MARK_BOX, mark(LIGHT)),
        "mark-black": svg(MARK_BOX, flat_mark("#000000")),
        "mark-white": svg(MARK_BOX, flat_mark("#FFFFFF")),
        "wordmark-on-dark": wordmark(DARK),
        "wordmark-on-light": wordmark(LIGHT),
        "lockup-on-dark": lockup(DARK),
        "lockup-on-light": lockup(LIGHT),
        "social": social(),
        "favicon": favicon(),
    }
    export(HERE, NAME, kit, NIGHT)


if __name__ == "__main__":
    main()

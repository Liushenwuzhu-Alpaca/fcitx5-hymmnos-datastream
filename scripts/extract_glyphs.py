#!/usr/bin/env python3
"""Extract Hymmnos glyph outlines into a JSON table consumed by generate_assets.py.

Run once (needs fontTools + brotli only for this step):

    uv run --with fonttools --with brotli scripts/extract_glyphs.py

Outlines are stored as SVG path data in font units (y axis up) together with
their bounding boxes, so the skin generator can place glyphs as plain vector
paths without depending on the font at runtime.
"""

from __future__ import annotations

import json
import string
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "Hymmnos.woff2"
OUT = ROOT / "scripts" / "hymmnos_glyphs.json"
CHARS = string.ascii_letters + string.digits + "/.#"


def main() -> int:
    font = TTFont(FONT)
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    table: dict[str, object] = {
        "unitsPerEm": font["head"].unitsPerEm,
        "ascent": font["hhea"].ascent,
        "descent": font["hhea"].descent,
        "glyphs": {},
    }
    for ch in CHARS:
        name = cmap.get(ord(ch))
        if name is None:
            continue
        path_pen = SVGPathPen(glyph_set)
        glyph_set[name].draw(path_pen)
        bounds_pen = BoundsPen(glyph_set)
        glyph_set[name].draw(bounds_pen)
        table["glyphs"][ch] = {
            "d": path_pen.getCommands(),
            "advance": font["hmtx"][name][0],
            "bounds": bounds_pen.bounds,
        }
    OUT.write_text(json.dumps(table, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {len(table['glyphs'])} glyphs to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

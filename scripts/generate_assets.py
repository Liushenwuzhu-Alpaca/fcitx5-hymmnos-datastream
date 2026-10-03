#!/usr/bin/env python3
"""Generate the Hymmnos Datastream fcitx5 skins (all palettes) into dist/.

Geometry targets fcitx5 classicui with in-app preedit (the panel then shows a
single candidate row):
  - font: Noto Sans Mono CJK SC Bold 13pt at 96 DPI (fontHeight 25),
  - one-row panel: fontHeight + textMargin(T+B) + contentMargin(T+B).

fcitx5 5.1.22 note: Theme::paint() ignores dx/dy for overlay images, so a
highlight overlay is pinned to the panel origin instead of riding the
highlight. The E/. cursor tag is therefore baked into the highlight image
itself, inside its unscaled 9-slice corner. No overlays are used.

The glyph rain streams "Was yea ra chs hymmnos mea / Wee ki ra sonwe yor /
paks hymme" — the first complete Hymmnos sentence in Ar tonelico lore.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLYPHS = json.loads((ROOT / "scripts" / "hymmnos_glyphs.json").read_text())
UPM = GLYPHS["unitsPerEm"]
DIST = ROOT / "dist"

THEME_PREFIX = "hymmnos-datastream"
DISPLAY_NAME = "Hymmnos Datastream"


def glyph_fit(ch: str, cx: float, cy: float, h: float, attrs: str) -> str:
    g = GLYPHS["glyphs"][ch]
    x0, y0, x1, y1 = g["bounds"]
    s = h / (y1 - y0)
    tx, ty = cx - (x0 + x1) / 2 * s, cy + (y0 + y1) / 2 * s
    return (
        f'<path transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f} {-s:.5f})" '
        f'd="{g["d"]}" {attrs}/>'
    )


def svg_doc(w: int, h: int, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">{body}</svg>\n'
    )


def corner_brackets(w: int, h: int, color: str, width: float = 2.0) -> str:
    d = (
        f"M1,{1 + 10} V1 H{1 + 10} M{w - 11},1 H{w - 1} V{1 + 10} "
        f"M1,{h - 11} V{h - 1} H{1 + 10} M{w - 11},{h - 1} H{w - 1} V{h - 11}"
    )
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"/>'


# palette: p0 p1 bg0 bg1 main head alert split block blockText text label hlLabel name
PALETTES = {
    "cyan":    ("#20262e", "#10141a", "#06161a", "#020607", "#78f0ff", "#e2fdff", "#ff3b5c", "#18e0ff", "#e2fdff", "#021014", "#c8f7ff", "#4fb8c8", "#c42a48", "Cyan"),
    "phosphor":("#242a24", "#121612", "#06140a", "#020803", "#6dff9a", "#e4ffe8", "#ffb43a", "#3cff7a", "#d8ffe2", "#031208", "#c4ffd2", "#46b866", "#b06a00", "Phosphor"),
    "amber":   ("#2e2620", "#171310", "#160e04", "#080502", "#ffb547", "#fff0d4", "#ff5a3a", "#ffd27a", "#ffe8bf", "#1c1004", "#ffdca8", "#b8843a", "#c43a1e", "Amber"),
    "violet":  ("#2a2436", "#14101c", "#120a20", "#06030c", "#b48cff", "#f2eaff", "#ff4fb8", "#4fe0ff", "#f2eaff", "#14082a", "#e2d4ff", "#8a6cc8", "#d42a90", "Violet"),
    "crimson": ("#2e2022", "#160e10", "#1a0608", "#080203", "#ff5a6a", "#ffe2e6", "#ffd23a", "#ff9aa6", "#ffe2e6", "#24060a", "#ffd0d6", "#c04a58", "#b02030", "Crimson"),
    "paper":   ("#e0e8ec", "#c6d2d8", "#f4f8fa", "#e2eaef", "#0a8aa8", "#033848", "#e0284a", "#0ab0d8", "#073848", "#e8fbff", "#0e2a34", "#5a8a98", "#ff7a92", "Paper"),
}

# one-row panel geometry: height 69 = 25 + (14+6) + (12+12)
GEO = {
    "text_margin": {"L": 10, "R": 10, "T": 14, "B": 6},
    "content_margin": {"L": 72, "R": 72, "T": 12, "B": 12},
    "panel_w": 480,
    "panel_h": 69,
    "panel_m": {"L": 132, "R": 140, "T": 33, "B": 34},
    "hl_m": {"L": 24, "R": 10, "T": 13, "B": 7},
}


def panel_svg(p: tuple) -> str:
    _, _, bg0, bg1, main, head, alert, split, *_ = p
    W, H = GEO["panel_w"], GEO["panel_h"]
    seq = "WASYEARACHSHYMMNOSMEAWEEKIRAsonweyorpakshymme"
    k = 0

    # Glyph rows must lie entirely inside one 9-slice band, otherwise a glyph
    # that straddles a band boundary gets torn by mismatched scales.
    # Bands: top 0-33, center 33-36, bottom 36-69; glyph height 9.
    ROWS = (12, 27, 42, 57)

    def rain(xs: list[int], mirror: bool) -> str:
        nonlocal k
        out = []
        for ci, x in enumerate(xs):
            skip = (ci * 2 + (1 if mirror else 0)) % len(ROWS)
            rows = [r for idx, r in enumerate(ROWS) if idx != skip]
            depth = ci if mirror else len(xs) - 1 - ci
            for j, y in enumerate(rows):
                ch = seq[k % len(seq)]
                k += 1
                fade = (j + 1) / len(rows)
                op = (0.14 + 0.5 * fade) * (1 - depth * 0.16)
                is_head = j == len(rows) - 1
                out.append(
                    glyph_fit(
                        ch, x, y, 9,
                        f'fill="{head if is_head else main}" fill-opacity="{0.95 if is_head else op:.2f}"',
                    )
                )
        return "".join(out)

    scan = "".join(
        f'<rect x="0" y="{i * 3}" width="{W}" height="1" fill="{head}" fill-opacity=".035"/>'
        for i in range(math.ceil(H / 3))
    )
    mono = 'font-family="DejaVu Sans Mono, monospace" font-size="7" letter-spacing=".5"'
    return svg_doc(W, H, f"""
    <defs>
      <radialGradient id="v" cx=".5" cy=".5" r=".75">
        <stop offset="0" stop-color="{bg0}"/><stop offset="1" stop-color="{bg1}"/>
      </radialGradient>
    </defs>
    <rect x="0" y="0" width="{W}" height="{H}" fill="url(#v)"/>
    <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{main}" stroke-opacity=".25"/>
    <line x1="64" y1="8" x2="64" y2="{H - 8}" stroke="{main}" stroke-opacity=".28"/>
    <line x1="{W - 64}" y1="8" x2="{W - 64}" y2="{H - 8}" stroke="{main}" stroke-opacity=".28"/>
    {rain([10, 24, 38, 52], False)}
    {rain([W - 10, W - 24, W - 38, W - 52], True)}
    {scan}
    {corner_brackets(W, H, main)}
    <text x="72" y="9.5" {mono} fill="{main}" fill-opacity=".7">HYMMNOSERVER</text>
    <circle cx="{W - 76}" cy="7" r="2" fill="{alert}"/>
    <text x="{W - 82}" y="9.5" {mono} fill="{alert}" fill-opacity=".85" text-anchor="end">H-WAVE 98.2%</text>
    <text x="{W - 72}" y="{H - 4}" {mono} fill="{main}" fill-opacity=".55" text-anchor="end">EXEC_INPUT/.</text>""")


def highlight_svg(p: tuple) -> str:
    _, _, _, _, main, _, alert, split, block, block_text, *_ = p
    m = GEO["hl_m"]
    W, H = 56, m["T"] + 25 + m["B"]          # 56 x 45
    return svg_doc(W, H, f"""
    <rect x="0" y="14" width="3" height="26" fill="{alert}"/>
    <path d="M3,10 H53 V37 L45,45 H3 Z" fill="{block}"/>
    <path d="M54,13 V36" stroke="{split}" stroke-width="2.4"/>
    <rect x="3" y="38" width="17" height="1.6" fill="{alert}" fill-opacity=".55"/>
    <path d="M1,1 H17 L23,12 H1 Z" fill="{main}"/>
    {glyph_fit("E", 9, 6.5, 8, f'fill="{block_text}"')}""")


def menu_panel_svg(p: tuple) -> str:
    p0, p1, main = p[0], p[1], p[4]
    return svg_doc(96, 64, f"""
    <defs><linearGradient id="m" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{p0}"/><stop offset="1" stop-color="{p1}"/></linearGradient></defs>
    <path d="M3,3 H93 V61 H3 Z" fill="url(#m)"/>
    <path d="M3,3 H93 V61 H3 Z" fill="none" stroke="{main}" stroke-opacity=".65" stroke-width="1"/>""")


def menu_highlight_svg(p: tuple) -> str:
    main, block = p[4], p[8]
    return svg_doc(64, 24, f"""
    <rect x="2" y="2" width="3" height="20" fill="{main}"/>
    <path d="M2,2 H62 V19 L58,22 H2 Z" fill="{block}"/>""")


def arrow_svg(p: tuple) -> str:
    return svg_doc(12, 12, f'<path d="M4.5,2.5 L9.5,6 L4.5,9.5" fill="none" stroke="{p[4]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')


def theme_conf(p: tuple) -> str:
    p0, p1, _bg0, _bg1, main, head, alert, split, block, block_text, text, label, hl_label, name = p
    tm, cm, pm, hm = GEO["text_margin"], GEO["content_margin"], GEO["panel_m"], GEO["hl_m"]
    return f"""# vim: ft=dosini
[Metadata]
Name={DISPLAY_NAME} {name}
Version=1.1
Author=Liushenwuzhu-Alpaca
Description=Hymmnos Datastream fcitx5 skin, {name} palette. Fan-made, not affiliated with GUST/Banpresto/KOEI TECMO.
ScaleWithDPI=True

[InputPanel]
NormalColor={text}
HighlightCandidateColor={block_text}
HighlightColor={text}
HighlightBackgroundColor=#00000000
CandidateLabelColor={label}
HighlightCandidateLabelColor={hl_label}

[InputPanel/Background]
Image=panel.svg
Color=#0e0e0e
BorderColor=#00000000
BorderWidth=0

[InputPanel/Background/Margin]
Left={pm['L']}
Right={pm['R']}
Top={pm['T']}
Bottom={pm['B']}

[InputPanel/Highlight]
Image=highlight.svg
Color=#00000000
BorderColor=#00000000

[InputPanel/Highlight/Margin]
Left={hm['L']}
Right={hm['R']}
Top={hm['T']}
Bottom={hm['B']}

[InputPanel/TextMargin]
Left={tm['L']}
Right={tm['R']}
Top={tm['T']}
Bottom={tm['B']}

[InputPanel/ContentMargin]
Left={cm['L']}
Right={cm['R']}
Top={cm['T']}
Bottom={cm['B']}

[InputPanel/BlurMargin]
Left=16
Right=16
Top=16
Bottom=16

[Menu]
NormalColor={text}
HighlightCandidateColor={block_text}
Spacing=4

[Menu/Background]
Image=menu-panel.svg
Color={p0}
BorderColor={main}
BorderWidth=0

[Menu/Background/Margin]
Left=6
Right=6
Top=6
Bottom=6

[Menu/Highlight]
Image=menu-highlight.svg
Color={block}
BorderColor=#00000000

[Menu/Highlight/Margin]
Left=2
Right=2
Top=2
Bottom=2

[Menu/TextMargin]
Left=8
Right=8
Top=4
Bottom=4

[Menu/ContentMargin]
Left=3
Right=3
Top=3
Bottom=3

[Menu/Separator]
Color={main}66

[Menu/SubMenu]
Image=arrow.svg
"""


def build_theme(palette_id: str, p: tuple) -> Path:
    out = DIST / f"{THEME_PREFIX}-{palette_id}"
    if out.exists():
        for stale in out.iterdir():
            stale.unlink()
    out.mkdir(parents=True, exist_ok=True)
    (out / "panel.svg").write_text(panel_svg(p))
    (out / "highlight.svg").write_text(highlight_svg(p))
    (out / "menu-panel.svg").write_text(menu_panel_svg(p))
    (out / "menu-highlight.svg").write_text(menu_highlight_svg(p))
    (out / "arrow.svg").write_text(arrow_svg(p))
    (out / "theme.conf").write_text(theme_conf(p))
    return out


def main() -> None:
    DIST.mkdir(exist_ok=True)
    for pid, p in PALETTES.items():
        print(build_theme(pid, p).name)


if __name__ == "__main__":
    main()

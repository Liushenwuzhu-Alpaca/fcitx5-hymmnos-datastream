# fcitx5-hymmnos-datastream

[中文](README.md)

A [fcitx5](https://fcitx-im.org) skin themed on the **Hymmnos language** from
Ar tonelico. Sister project:
[fcitx5-hymmnos-hymn-score](https://github.com/Liushenwuzhu-Alpaca/fcitx5-hymmnos-hymn-score).

**Datastream** recreates a Hymmnoserver terminal: glyph rain falls along both
edges of the panel, and the falling stream *is* the song itself:

> **Was yea ra chs hymmnos mea · Wee ki ra sonwe yor · paks hymme**
> ("I shall become a song - calmly I sing for you - rejoicing, it resounds")

The HUD reads `HYMMNOSERVER` / `H-WAVE 98.2%` / `EXEC_INPUT/.`, and the
highlighted candidate is a cut-corner data block pinned with a **Love vowel `E`**
tag and chromatic-aberration glitch stripes.

## Themes

| Theme | Preview |
|---|---|
| **Cyan** (default dark) | ![cyan](images/cyan.png) |
| **Paper** (default light) | ![paper](images/paper.png) |
| Phosphor | ![phosphor](images/phosphor.png) |
| Violet | ![violet](images/violet.png) |
| Amber | ![amber](images/amber.png) |
| Crimson | ![crimson](images/crimson.png) |

## Installation

```bash
git clone https://github.com/Liushenwuzhu-Alpaca/fcitx5-hymmnos-datastream.git
cd fcitx5-hymmnos-datastream
./install.sh   # copies dist/* to ~/.local/share/fcitx5/themes and restarts fcitx5
```

Then pick `Hymmnos Datastream Cyan` (dark) or `Hymmnos Datastream Paper` (light)
in fcitx5 Configtool -> Addon -> Classic User Interface. Noto Sans CJK and
Noto Sans Mono CJK fonts are recommended.

## Regenerating

`dist/` is produced by a generator script (glyph outlines come from the bundled
Hymmnos font):

```bash
python3 scripts/generate_assets.py
```

## Disclaimer

Fan work, unaffiliated with GUST / Bandai Namco. Hymmnos and Ar tonelico belong to
their respective owners. The bundled font is only used to bake SVG outlines and is
not required at runtime.

## License

[MIT](LICENSE)

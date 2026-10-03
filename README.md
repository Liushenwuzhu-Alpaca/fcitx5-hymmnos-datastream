# fcitx5-hymmnos-datastream

以《魔塔大陆》(Ar tonelico) **Hymmnos 语**为主题的 fcitx5 输入法皮肤,姊妹篇:
[fcitx5-hymmnos-hymn-score](https://github.com/Liushenwuzhu-Alpaca/fcitx5-hymmnos-hymn-score)。

**数据流 (Datastream)** -- 再现 Hymmnoserver 终端界面:面板两侧是下坠的
Hymmnos 字形数据雨,文字流内容正是诗歌本身:

> **Was yea ra chs hymmnos mea · Wee ki ra sonwe yor · paks hymme**
> (我将化身为诗 · 平静专注地为你歌唱 · 兴奋地奏响)

HUD 标注 `HYMMNOSERVER` / `H-WAVE 98.2%` / `EXEC_INPUT/.`,候选高亮是一块
切角数据块,左上角钉着**爱音 `E`** 标签,边缘带色差故障(glitch)条纹。

## 主题

| 主题 | 预览 |
|---|---|
| **Cyan** (默认深色) | ![cyan](images/cyan.png) |
| **Paper** (默认浅色) | ![paper](images/paper.png) |
| Phosphor | ![phosphor](images/phosphor.png) |
| Violet | ![violet](images/violet.png) |
| Amber | ![amber](images/amber.png) |
| Crimson | ![crimson](images/crimson.png) |

## 安装

```bash
git clone https://github.com/Liushenwuzhu-Alpaca/fcitx5-hymmnos-datastream.git
cd fcitx5-hymmnos-datastream
./install.sh   # 复制 dist/* 到 ~/.local/share/fcitx5/themes 并重启 fcitx5
```

然后在 fcitx5 配置 → 附加组件 → 经典用户界面中选择
`Hymmnos Datastream Cyan`(深色)或 `Hymmnos Datastream Paper`(浅色),
亦可搭配 hymn-score 系列混搭。

建议安装 Noto Sans CJK 与 Noto Sans Mono CJK 字体以获得最佳效果。

## 重新生成

`dist/` 由生成脚本产出(字形取自自带的 Hymmnos 字体):

```bash
python3 scripts/generate_assets.py
```

## 声明

粉丝作品,与 GUST / 万代南梦宫无关。Hymmnos 语与《魔塔大陆》相关权利归原作者所有。
字体文件来自公开的 Hymmnos 字库,仅用于生成 SVG 轮廓,运行时不再需要。

## 许可

[MIT](LICENSE)

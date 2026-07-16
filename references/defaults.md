# 默认参数

当前用户要求优先于本文件。只在用户没有指定时使用以下默认值。

## 正文配图

```yaml
preset: saas-guide
density: per-section
palette: macaron
language: zh
watermark: false
output_dir: assets/
image_backend: Codex 内置生图模型
generation_batch_size: 4
```

图片与文章放在同一目录层级下的 `assets/`：

```text
文章目录/
├── 文章.md
└── assets/
    ├── cover.png
    ├── section-01.png
    ├── section-02.png
    └── section-03.png
```

文件名使用两位连续序号。不要把章节标题、长句或中文标点写入文件名。

## 公众号封面

```yaml
type: conceptual
palette: macaron
rendering: hand-drawn
text: title-subtitle
mood: bold
aspect: 2.35:1
language: zh
watermark: false
output_dir: assets/
filename: cover.png
image_backend: Codex 内置生图模型
```

## 文章排版

```yaml
theme: moyu-green
body_font_size: 16px
body_line_height: 1.85
content_horizontal_padding: 8px
container_width: 100%
preview_width: 820px
```

附加要求：

- 精选导读完整展示所有二级标题，不只抽取部分章节。
- 章节序号连续且与正文一致。
- 纯净 HTML 保留相对图片路径。
- 一键复制预览版内嵌本地图片，并优先使用支持富文本与图片的剪贴板复制方式。
- 生成后检查 Markdown 图片路径、目录数量、标题数量和排版校验结果。

## 产物命名

默认不覆盖用户原稿：

```text
原稿.md
原稿_去除AI味.md
原稿_配图版.md
原稿_排版_摸鱼绿.html
原稿_排版_摸鱼绿_预览.html
```

如果从中间步骤开始，直接基于用户指定的输入文件生成该步骤产物。

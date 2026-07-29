# 默认参数

当前用户要求优先于本文件。只在用户没有指定时使用以下默认值。

## 子 Skill 调用

```yaml
child_skill_invocation:
  resolve_from_workflow: true
  skip_first_time_setup: true
  persist_preferences: false
  prompt_only_for_unresolved_required_values: true
```

这些参数表示本文件就是子 Skill 在本次工作流中的调用配置。即使子 Skill 没有
`EXTEND.md` 或其它偏好文件，也不得触发首次配置，不得询问偏好保存范围，更不得把
本工作流的默认值写成全局或项目偏好。只有本文件与当前用户要求都缺少某个必需值时，
才询问该缺失项。

## 工作流交互

```yaml
mode: ask
step_mode:
  pause_after_each_step: true
auto_mode:
  selection_is_authorization: true
  show_execution_summary: true
  start_immediately_after_summary: true
  pause_after_each_step: false
  progress_receipt_after_each_step: true
  reuse_default_generation_parameters: true
```

用户回复 `自动 N` 就是对本次执行和默认生成参数的总授权。自动执行摘要只用于说明
接下来会做什么，发出后立即开始；不得再要求用户回复 `开始`、步骤序号，或确认配图、
封面方案。执行期间仍逐步反馈。

## 正文配图

```yaml
preset: saas-guide
type: infographic
style: notion
density: per-section
palette: macaron
language: zh
watermark: false
output_dir: assets/
image_backend: Codex 内置生图模型
generation_batch_size: 4
```

`saas-guide` 在本工作流中固定展开为 `infographic + notion`。这里显式写出展开结果，
子 Skill 不得再单独询问默认插画风格。

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
type: metaphor
palette: ai-product-series
rendering: hand-drawn
text: title-subtitle
mood: balanced
aspect: 2.35:1
language: zh
watermark: false
output_dir: assets/
filename: cover.png
image_backend: Codex 内置生图模型
style_preferences: .baoyu-skills/baoyu-cover-image/EXTEND.md
style_reference: .baoyu-skills/baoyu-cover-image/refs/ai-product-series-cover.png
```

系列封面以 `style_reference` 为视觉基准，并遵循 `style_preferences` 中的
“AI 编程从想法到产品：系列封面规则”。后续文章沿用纸张、线条、配色、手写标题和
“标题主导 + 内容隐喻”的构图，只替换文章序号、标题和核心隐喻；不要固定复用第 01 篇的跨桥画面。

## 文章排版

```yaml
theme: moyu-green
body_font_size: 16px
body_line_height: 1.85
content_horizontal_padding: 8px
container_width: 100%
preview_width: 820px
show_header_card: false
show_toc: false
show_author_signature: false
show_footer_cta: false
```

附加要求：

- 不生成正文顶部封面卡或章节目录。
- 不生成作者介绍、点赞/在看/转发互动卡或品牌尾图。
- 章节序号连续且与正文一致。
- 纯净 HTML 保留相对图片路径。
- 一键复制预览版内嵌本地图片，并优先使用支持富文本与图片的剪贴板复制方式。
- 生成后检查 Markdown 图片路径、标题数量和排版校验结果。

## 公众号摘要

```yaml
source_priority:
  - "{原稿}_配图版.md"
  - "{原稿}_去除AI味.md"
  - "{原稿}.md"
max_chars: 120
single_paragraph: true
include_title: false
include_emoji: false
include_hashtags: false
include_links: false
filename: "{原稿}_公众号摘要.md"
validation_script: scripts/validate_summary.py
```

摘要必须忠于正文，直接说明文章主题和读者能获得的内容。文件只保留摘要正文，不添加
“摘要”标题、解释、备选版本或字数说明。去除首尾空白后按 Unicode 字符计数，中文、
标点、英文字母和数字都计入长度，结果必须不超过 120 个字符。

## 朋友圈转发文案

```yaml
source_priority:
  - "{原稿}_配图版.md"
  - "{原稿}_去除AI味.md"
  - "{原稿}.md"
max_han_chars: 100
single_paragraph: true
tone: natural-share
include_title: false
include_emoji: false
include_hashtags: false
include_links: false
filename: "{原稿}_朋友圈文案.md"
validation_script: scripts/validate_moments_copy.py
```

朋友圈文案必须忠于正文，但不照抄公众号摘要。用自然、具体的分享口吻表达分享动机，
并提供一个与正文核心内容相关的阅读钩子。文件只保留文案正文，不添加“朋友圈文案”
标题、解释或备选版本；开头直接进入问题、观察或观点，不使用文章标题、系列名或
“第 N 篇”起手。去除首尾空白后不超过 100 个汉字，只统计汉字，标点、空格、
英文字母和数字不计入汉字数。

## 产物命名

默认不覆盖用户原稿：

```text
原稿.md
原稿_去除AI味.md
原稿_配图版.md
原稿_排版_摸鱼绿.html
原稿_排版_摸鱼绿_预览.html
原稿_公众号摘要.md
原稿_朋友圈文案.md
```

如果从中间步骤开始，直接基于用户指定的输入文件生成该步骤产物。

## 收尾清理

```yaml
cleanup:
  enabled: true
  run_after_final_step_validation: true
  keep_root_documents:
    - "{原稿}.md"
    - "{原稿}_去除AI味.md"
    - "{原稿}_配图版.md"
    - "{原稿}_排版_{主题}.html"
    - "{原稿}_排版_{主题}_预览.html"
    - "{原稿}_公众号摘要.md"
    - "{原稿}_朋友圈文案.md"
  keep_assets:
    - assets/cover.png
    - 被保留 Markdown 或纯净 HTML 引用的图片
  remove_known_intermediates:
    - assets/cover-*
    - 未被保留文档引用的 assets/section-*
    - assets/outline.md
    - assets/*prompt*
    - assets/*提示词*
    - assets/prompts/
    - assets/.prompts/
    - 未被保留文档引用的 assets/refs/
    - assets/tmp/
    - assets/.tmp/
```

清理不删除文章根目录中的任何 Markdown 或 HTML，也不删除命名规则之外的未知文件。
必须先预览删除清单，再由工作流自行核对并执行，不需要用户二次确认。

# wechat-draft-to-publish

把一份 Markdown 草稿依次完成去除 AI 味、正文配图、封面制作、公众号排版、120 字以内的公众号摘要和 100 个汉字以内的朋友圈转发文案，生成可直接发布与转发的微信公众号图文成稿。

## 工作流程

1. 去除 AI 味
2. 正文配图
3. 封面制作
4. 文章排版
5. 公众号摘要
6. 朋友圈转发文案

支持两种执行方式：

- 分步确认：每一步完成后给出回执，等待确认再继续。
- 自动完成：回复 `自动 N` 后立即连续执行；先展示执行摘要，每一步仍反馈进度，但不再等待第二次“开始”确认。

两种模式都可以从任意一步开始。最终预览生成并校验后，会自动清理已知的无用候选图、
参考图副本、提示词和临时文件，同时保留原稿、阶段稿、排版 HTML、公众号摘要、朋友圈文案、正式封面和正文引用图片。

## 使用方式

将 Skill 安装到项目的 `.agents/skills/`：

```bash
git clone https://github.com/vincent4j/wechat-draft-to-publish.git \
  .agents/skills/wechat-draft-to-publish
```

然后在 Codex 中使用：

```text
$wechat-draft-to-publish 处理这篇文章
```

Skill 会识别文章草稿，并让你选择执行模式和起始步骤。

## 默认效果

- 正文配图：`saas-guide`、`per-section`、`macaron`
- 图片目录：文章同目录下的 `assets/`
- 公众号封面：2.35:1、系列定制配色、手绘隐喻风格
- 公众号排版：摸鱼绿、16px 正文、8px 两侧留白，不添加正文封面卡、目录或互动尾卡
- 最终生成纯净 HTML 和一键复制预览版
- 公众号摘要：单段、无标题和链接，不超过 120 字，并单独保存为 Markdown
- 朋友圈转发文案：自然分享口吻、直接进入问题或观点、单段、无链接和话题标签，不超过 100 个汉字，并单独保存为 Markdown
- 收尾清理：删除无用候选图、未引用配图、参考图副本、提示词和已知临时文件

## 依赖

需要提前安装以下 Skills：

- `humanizer-zh`
- `baoyu-article-illustrator`
- `baoyu-cover-image`
- `gzh-design`

具体工作流和约束以 [SKILL.md](SKILL.md) 为准。

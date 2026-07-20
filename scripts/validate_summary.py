#!/usr/bin/env python3
"""校验公众号摘要是否可直接粘贴到后台。"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\([^)]+\)")
LIST_PREFIX = re.compile(r"^(?:[-*+]\s+|\d+[.)]\s+)")


def contains_emoji(text: str) -> bool:
    return any(
        0x1F000 <= ord(char) <= 0x1FAFF
        or 0x2600 <= ord(char) <= 0x27BF
        for char in text
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 120 字以内的公众号摘要")
    parser.add_argument("summary_file", type=Path, help="公众号摘要 Markdown 文件")
    parser.add_argument("--max-chars", type=int, default=120, help="最大字符数")
    args = parser.parse_args()

    path = args.summary_file.expanduser().resolve()
    if not path.is_file():
        parser.error(f"摘要文件不存在：{path}")

    summary = path.read_text(encoding="utf-8").strip()
    errors: list[str] = []
    if not summary:
        errors.append("摘要不能为空")
    if "\n" in summary or "\r" in summary:
        errors.append("摘要必须是单个自然段")
    if len(summary) > args.max_chars:
        errors.append(f"摘要长度为 {len(summary)} 字，超过 {args.max_chars} 字")
    if summary.startswith("#") or LIST_PREFIX.match(summary):
        errors.append("摘要不能带标题或列表前缀")
    if any(mark in summary for mark in ("**", "__", "`")):
        errors.append("摘要不能包含 Markdown 标记")
    if MARKDOWN_LINK.search(summary) or "http://" in summary or "https://" in summary:
        errors.append("摘要不能包含链接")
    if "#" in summary:
        errors.append("摘要不能包含话题标签")
    if contains_emoji(summary):
        errors.append("摘要不能包含 Emoji")

    if errors:
        print("公众号摘要校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"公众号摘要校验通过：{len(summary)}/{args.max_chars} 字。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

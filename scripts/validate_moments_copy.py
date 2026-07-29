#!/usr/bin/env python3
"""校验朋友圈转发文案是否可直接使用。"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\([^)]+\)")
LIST_PREFIX = re.compile(r"^(?:[-*+]\s+|\d+[.)]\s+)")
FORBIDDEN_OPENING = re.compile(
    r"^(?:《[^》]+》|[^。！？]{0,30}第\s*[0-9一二三四五六七八九十]+\s*篇|这篇文章(?:讲了|讲的是|介绍了|主要讲))"
)
HAN_RANGES = (
    (0x3400, 0x4DBF),
    (0x4E00, 0x9FFF),
    (0xF900, 0xFAFF),
    (0x20000, 0x2A6DF),
    (0x2A700, 0x2B73F),
    (0x2B740, 0x2B81F),
    (0x2B820, 0x2CEAF),
    (0x2CEB0, 0x2EBEF),
    (0x30000, 0x3134F),
)


def contains_emoji(text: str) -> bool:
    return any(
        0x1F000 <= ord(char) <= 0x1FAFF
        or 0x2600 <= ord(char) <= 0x27BF
        for char in text
    )


def count_han(text: str) -> int:
    return sum(
        char == "〇" or any(start <= ord(char) <= end for start, end in HAN_RANGES)
        for char in text
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 100 个汉字以内的朋友圈转发文案")
    parser.add_argument("copy_file", type=Path, help="朋友圈转发文案 Markdown 文件")
    parser.add_argument("--max-han", type=int, default=100, help="最大汉字数")
    parser.add_argument(
        "--allow-emoji",
        action="store_true",
        help="允许 Emoji；仅在用户明确要求时使用",
    )
    args = parser.parse_args()

    path = args.copy_file.expanduser().resolve()
    if not path.is_file():
        parser.error(f"朋友圈文案文件不存在：{path}")

    copy = path.read_text(encoding="utf-8").strip()
    han_count = count_han(copy)
    errors: list[str] = []
    if not copy:
        errors.append("朋友圈文案不能为空")
    if "\n" in copy or "\r" in copy:
        errors.append("朋友圈文案必须是单个自然段")
    if han_count > args.max_han:
        errors.append(f"朋友圈文案含 {han_count} 个汉字，超过 {args.max_han} 个汉字")
    if copy.startswith("#") or LIST_PREFIX.match(copy):
        errors.append("朋友圈文案不能带标题或列表前缀")
    if FORBIDDEN_OPENING.match(copy):
        errors.append("朋友圈文案不能用文章标题、系列名称、第 N 篇或“这篇文章讲了……”起手")
    if any(mark in copy for mark in ("**", "__", "`")):
        errors.append("朋友圈文案不能包含 Markdown 标记")
    if MARKDOWN_LINK.search(copy) or "http://" in copy or "https://" in copy:
        errors.append("朋友圈文案不能包含链接")
    if "#" in copy:
        errors.append("朋友圈文案不能包含话题标签")
    if not args.allow_emoji and contains_emoji(copy):
        errors.append("朋友圈文案默认不能包含 Emoji")

    if errors:
        print("朋友圈转发文案校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"朋友圈转发文案校验通过：{han_count}/{args.max_han} 个汉字"
        f"（总字符 {len(copy)}）。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

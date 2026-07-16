#!/usr/bin/env python3
"""清理公众号成稿工作流生成后不再使用的已知中间产物。

默认只预览待删除清单；传入 --apply 才实际删除。脚本只检查文章目录下的
assets/，不会删除文章根目录中的 Markdown 或 HTML 文档。
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
from pathlib import Path
from urllib.parse import unquote


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
PROMPT_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml"}
INTERMEDIATE_DIRECTORIES = {"prompts", ".prompts", "refs", "tmp", ".tmp"}
REFERENCE_PATTERN = re.compile(r"""assets/[^\s"'()<>\]]+""")


def is_inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def collect_referenced_assets(article_dir: Path, assets_dir: Path) -> set[Path]:
    referenced: set[Path] = set()

    for document in article_dir.iterdir():
        if not document.is_file() or document.suffix.lower() not in {".md", ".html"}:
            continue
        if document.name.endswith("_预览.html"):
            continue

        text = document.read_text(encoding="utf-8", errors="replace")
        for match in REFERENCE_PATTERN.findall(text):
            relative = unquote(html.unescape(match)).split("?", 1)[0].split("#", 1)[0]
            target = article_dir / relative
            if is_inside(target, assets_dir):
                referenced.add(target.resolve())

    cover = assets_dir / "cover.png"
    if cover.exists():
        referenced.add(cover.resolve())

    return referenced


def collect_candidates(assets_dir: Path, referenced: set[Path]) -> list[Path]:
    candidates: set[Path] = set()

    def is_referenced(path: Path) -> bool:
        if path.is_dir():
            return any(is_inside(item, path) for item in referenced)
        return path.resolve() in referenced

    for path in assets_dir.iterdir():
        if path.is_dir():
            if path.name.lower() in INTERMEDIATE_DIRECTORIES and not is_referenced(path):
                candidates.add(path)
            continue

        suffix = path.suffix.lower()
        name = path.name.lower()

        if suffix in IMAGE_EXTENSIONS:
            if name.startswith("cover-") and not is_referenced(path):
                candidates.add(path)
            elif name.startswith("section-") and not is_referenced(path):
                candidates.add(path)
            continue

        if path.name == "outline.md" and not is_referenced(path):
            candidates.add(path)
        elif suffix in PROMPT_EXTENSIONS and (
            "prompt" in name or "提示词" in path.name
        ) and not is_referenced(path):
            candidates.add(path)

    return sorted(candidates, key=lambda item: item.as_posix())


def remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="预览或删除公众号成稿工作流生成的无用中间产物"
    )
    parser.add_argument("article_dir", type=Path, help="文章所在目录")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="实际删除；不传时只输出待删除清单",
    )
    args = parser.parse_args()

    article_dir = args.article_dir.expanduser().resolve()
    assets_dir = article_dir / "assets"
    if not article_dir.is_dir():
        parser.error(f"文章目录不存在：{article_dir}")
    if not assets_dir.is_dir():
        print("未找到 assets/，无需清理。")
        return 0

    referenced = collect_referenced_assets(article_dir, assets_dir)
    candidates = collect_candidates(assets_dir, referenced)
    candidate_paths = {path.resolve() for path in candidates}
    preserved_unknown = []
    for path in sorted(assets_dir.iterdir(), key=lambda item: item.as_posix()):
        resolved = path.resolve()
        is_known_reference = resolved in referenced or (
            path.is_dir() and any(is_inside(item, path) for item in referenced)
        )
        if resolved not in candidate_paths and not is_known_reference:
            preserved_unknown.append(path)

    mode = "删除" if args.apply else "待删除"
    print(f"{mode}中间产物：{len(candidates)} 项")
    for path in candidates:
        print(f"- {path.relative_to(article_dir)}")

    print(f"保留正式资源：{len(referenced)} 项")
    print(f"保留未识别资源：{len(preserved_unknown)} 项")
    for path in preserved_unknown:
        print(f"- {path.relative_to(article_dir)}")
    print("文章目录中的 Markdown 和 HTML 文档不会被删除。")

    if not args.apply:
        print("这是预览模式；确认清单后加 --apply 执行。")
        return 0

    for path in candidates:
        if not is_inside(path, assets_dir):
            raise RuntimeError(f"拒绝删除 assets/ 之外的路径：{path}")
        remove_path(path)

    print("清理完成。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

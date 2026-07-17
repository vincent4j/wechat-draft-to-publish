#!/usr/bin/env python3
"""检查父工作流不会把子 Skill 的首次配置暴露给用户。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

REQUIRED_TEXT = {
    ROOT / "SKILL.md": [
        "## 子 Skill 配置继承（硬约束）",
        "禁止执行子 Skill 的首次配置流程",
        "首次偏好配置不属于生成前确认",
        "不得因为缺少 `EXTEND.md` 触发首次配置",
        "分步模式只等待用户确认本次配图方案",
        "不得因为缺少偏好文件触发首次配置",
        "分步模式只等待用户确认本次封面方案",
    ],
    ROOT / "references" / "defaults.md": [
        "resolve_from_workflow: true",
        "skip_first_time_setup: true",
        "persist_preferences: false",
        "prompt_only_for_unresolved_required_values: true",
        "preset: saas-guide",
        "type: infographic",
        "style: notion",
        "watermark: false",
        "output_dir: assets/",
        "image_backend: Codex 内置生图模型",
        "generation_batch_size: 4",
    ],
}


def main() -> int:
    missing: list[str] = []
    for path, required in REQUIRED_TEXT.items():
        text = path.read_text(encoding="utf-8")
        for value in required:
            if value not in text:
                missing.append(f"{path.relative_to(ROOT)}: {value}")

    if missing:
        print("工作流配置继承检查失败：")
        for item in missing:
            print(f"- 缺少 {item}")
        return 1

    print("工作流配置继承检查通过：父工作流默认值会跳过子 Skill 首次配置。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

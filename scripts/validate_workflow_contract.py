#!/usr/bin/env python3
"""检查父级配置继承、自动授权、摘要和朋友圈文案契约。"""

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
        "用户回复 `自动 N` 即视为",
        "展示执行摘要后立即开始",
        "## 第 5 步：公众号摘要",
        "{原稿}_公众号摘要.md",
        "scripts/validate_summary.py",
        "## 第 6 步：朋友圈转发文案",
        "{原稿}_朋友圈文案.md",
        "scripts/validate_moments_copy.py",
        "连续执行到第 6 步结束",
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
        "selection_is_authorization: true",
        "start_immediately_after_summary: true",
        "max_chars: 120",
        "filename: \"{原稿}_公众号摘要.md\"",
        "## 朋友圈转发文案",
        "max_han_chars: 100",
        "filename: \"{原稿}_朋友圈文案.md\"",
        "validation_script: scripts/validate_moments_copy.py",
        "run_after_final_step_validation: true",
    ],
    ROOT / "references" / "receipts.md": [
        "5. **公众号摘要**",
        "6. **朋友圈转发文案**",
        "自动开始：第 N 步「步骤名称」。",
        "第 6 步「朋友圈转发文案」已完成",
        "摘要字符数与格式校验结果",
        "朋友圈文案汉字数与格式校验结果",
    ],
    ROOT / "README.md": [
        "5. 公众号摘要",
        "6. 朋友圈转发文案",
        "不再等待第二次“开始”确认",
        "不超过 120 字",
        "不超过 100 个汉字",
    ],
    ROOT / "agents" / "openai.yaml": [
        "自动模式连续完成六步",
        "120 字以内的公众号摘要",
        "100 个汉字以内的朋友圈转发文案",
    ],
    ROOT / "scripts" / "validate_summary.py": [
        "摘要必须是单个自然段",
        "摘要不能包含链接",
        "公众号摘要校验通过",
    ],
    ROOT / "scripts" / "validate_moments_copy.py": [
        "朋友圈文案必须是单个自然段",
        "朋友圈文案不能包含链接",
        "朋友圈文案不能包含话题标签",
        "不能用文章标题、系列名称、第 N 篇",
        "朋友圈转发文案校验通过",
    ],
}

FORBIDDEN_TEXT = {
    ROOT / "SKILL.md": [
        "等待用户回复 `开始`",
        "使用自动执行摘要并等待 `开始`",
        "连续执行到第 4 步结束",
        "连续执行到第 5 步结束",
    ],
    ROOT / "references" / "defaults.md": [
        "confirmation_word: 开始",
    ],
    ROOT / "references" / "receipts.md": [
        "回复 `开始`：按以上配置连续执行。",
        "未收到 `开始` 前不要执行。",
        "第 5 步改用最终回执",
        "第 5 步完成后不再显示下一步",
    ],
    ROOT / "README.md": [
        "用户回复“开始”后连续跑完",
    ],
    ROOT / "agents" / "openai.yaml": [
        "在我确认开始后连续跑完",
    ],
}


def main() -> int:
    missing: list[str] = []
    for path, required in REQUIRED_TEXT.items():
        text = path.read_text(encoding="utf-8")
        for value in required:
            if value not in text:
                missing.append(f"{path.relative_to(ROOT)}: {value}")

    forbidden: list[str] = []
    for path, values in FORBIDDEN_TEXT.items():
        text = path.read_text(encoding="utf-8")
        for value in values:
            if value in text:
                forbidden.append(f"{path.relative_to(ROOT)}: {value}")

    if missing or forbidden:
        print("工作流契约检查失败：")
        for item in missing:
            print(f"- 缺少 {item}")
        for item in forbidden:
            print(f"- 仍包含旧协议 {item}")
        return 1

    print("工作流契约检查通过：父级默认值会跳过首次配置，自动模式立即执行，并生成 120 字以内摘要和 100 个汉字以内朋友圈文案。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

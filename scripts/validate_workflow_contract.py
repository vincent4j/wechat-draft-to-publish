#!/usr/bin/env python3
"""检查配置继承、执行范围、关键确认和完整回执契约。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

REQUIRED_TEXT = {
    ROOT / "SKILL.md": [
        "## 子 Skill 配置继承（硬约束）",
        "禁止执行子 Skill 的首次配置流程",
        "不得因为缺少 `EXTEND.md` 触发首次配置",
        "不得因为缺少偏好文件触发首次配置",
        "支持“直接完成”和“边做边看”两种模式",
        "支持只做一项、执行一段范围、选择多个指定产物或生成完整发布包",
        "只在正文、配图、封面和排版这些需要主观判断的实际结果完成后暂停",
        "展示执行摘要，列出实际执行和明确跳过的步骤",
        "`自动 N` 表示直接完成第 N 至第 6 步",
        "清楚指定单项任务，即视为",
        "展示执行摘要后立即开始",
        "不擅自扩大范围",
        "## 识别执行范围",
        "用户列出多个不连续产物时，只执行列出的步骤",
        "不得因为某一步通常位于后面，就擅自执行用户没有要求的前置步骤",
        "在实际图片生成后确认结果，不增加生成前方案确认",
        "在实际封面生成后确认结果，不增加生成前方案确认",
        "## 第 5 步：公众号摘要",
        "{原稿}_公众号摘要.md",
        "scripts/validate_summary.py",
        "## 第 6 步：朋友圈转发文案",
        "{原稿}_朋友圈文案.md",
        "scripts/validate_moments_copy.py",
        "## 发布包一致性检查",
        "每次结束都必须给出完整执行回执",
        "明确实际完成、明确跳过、生成文件、检查结果和清理结果",
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
        "direct_mode:",
        "selection_is_authorization: true",
        "start_immediately_after_summary: true",
        "review_mode:",
        "confirm_actual_result_not_generation_plan: true",
        "execution_scope:",
        "allow_single_step: true",
        "allow_contiguous_range: true",
        "allow_selected_steps: true",
        "do_not_expand_scope: true",
        "max_chars: 120",
        "filename: \"{原稿}_公众号摘要.md\"",
        "## 朋友圈转发文案",
        "max_han_chars: 100",
        "filename: \"{原稿}_朋友圈文案.md\"",
        "validation_script: scripts/validate_moments_copy.py",
        "run_after_final_step_validation: true",
        "require_current_scope_steps:",
        "skip_for_partial_scope_by_default: true",
        "## 发布包一致性",
        "report_stale_outputs: true",
        "regenerate_only_when_in_scope: true",
    ],
    ROOT / "references" / "receipts.md": [
        "5. **公众号摘要**",
        "6. **朋友圈转发文案**",
        "**直接完成**",
        "**边做边看**",
        "只排版",
        "## 完整执行回执",
        "两种模式开始执行前都使用",
        "**实际完成**",
        "**明确跳过**",
        "**收尾处理**",
        "**需要留意**",
        "完整回执必须回答用户关心的“你都做了什么”",
    ],
    ROOT / "README.md": [
        "5. 公众号摘要",
        "6. 朋友圈转发文案",
        "不再等待第二次“开始”确认",
        "只做一项、执行一段流程、选择多个产物",
        "直接完成",
        "边做边看",
        "工作流不会自动扩大用户指定的范围",
        "完整执行回执",
        "只做单项或局部范围时默认不清理",
        "不超过 120 字",
        "不超过 100 个汉字",
    ],
    ROOT / "agents" / "openai.yaml": [
        "支持按需生成完整或局部公众号发布包，完成配图、封面、排版与文案",
        "识别需要的产物和执行范围",
        "结束时告诉我实际做了什么",
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
        "分步模式只等待用户确认本次配图方案",
        "分步模式只等待用户确认本次封面方案",
        "连续执行到第 6 步结束",
    ],
    ROOT / "references" / "defaults.md": [
        "confirmation_word: 开始",
    ],
    ROOT / "references" / "receipts.md": [
        "回复 `开始`：按以上配置连续执行。",
        "未收到 `开始` 前不要执行。",
        "第 5 步改用最终回执",
        "第 5 步完成后不再显示下一步",
        "回复 `分步 1`",
        "回复 `自动 1`",
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

    print("工作流契约检查通过：可按自然语言限定产物范围，支持直接完成或关键结果确认，并在结束时报告实际执行内容。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

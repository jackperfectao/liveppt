"""Markdown cleaning utilities for README preprocessing."""

import re


def clean_markdown(text: str) -> str:
    """Clean GitHub-flavored README for LivePPT rendering."""
    lines = text.splitlines()
    cleaned = []
    in_html_block = False
    seen_h1 = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("<div"):
            in_html_block = True
            continue
        if in_html_block:
            if stripped.endswith("</div>") or stripped == "</div>":
                in_html_block = False
            continue

        if stripped.startswith("![") and "](assets/" in stripped:
            continue
        if stripped.startswith("[") and "](" in stripped and "|" in stripped and not seen_h1:
            continue
        if stripped.startswith("[!["):
            continue
        if stripped in {"---", "***"}:
            continue

        if stripped.startswith("# "):
            seen_h1 = True
            cleaned.append(line)
            continue

        if stripped.startswith("## "):
            title = stripped[3:].strip()
            rename_map = {
                "What LivePPT Is": "What This Project Does",
                "LivePPT 是什么": "这个项目能做什么",
                "Why the Main Entry Should Not Be a \"14-Day Plan\"": "Why HTML Output Comes First",
                "为什么不是先生成“14 天执行计划”": "为什么先出 HTML",
                "30-Second Quick Start": "Quick Start",
                "30 秒快速开始": "快速开始",
                "Current Core Capabilities": "Core Capabilities",
                "当前核心能力": "核心能力",
                "Current Boundaries": "Current Boundaries",
                "当前边界": "当前边界",
                "Common Commands": "Common Commands",
                "常用命令": "常用命令",
            }
            cleaned.append(f"## {rename_map.get(title, title)}")
            continue

        if not seen_h1 and stripped.startswith((">", "- ", "* ")):
            continue

        if stripped.startswith("```"):
            continue

        if stripped:
            stripped = re.sub(r"`([^`]+)`", r"\1", stripped)

        cleaned.append(stripped)

    result = "\n".join(cleaned)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip() + "\n"

"""Markdown parsing functions for LivePPT deck generation."""

import re
from typing import Dict, List, Optional, Tuple


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9一-鿿]+", "-", value)
    return value.strip("-") or "section"


def extract_title(lines: List[str], fallback: str) -> Tuple[str, List[str]]:
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip(), lines[:index] + lines[index + 1 :]
    return fallback, lines


def split_sections(lines: List[str]) -> Tuple[List[str], List[Tuple[str, List[str]]]]:
    preamble: List[str] = []
    sections: List[Tuple[str, List[str]]] = []
    current_title: Optional[str] = None
    current_lines: List[str] = []

    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()
        if stripped.startswith("## "):
            if current_title is not None:
                sections.append((current_title, current_lines))
            current_title = stripped[3:].strip()
            current_lines = []
            continue

        if current_title is None:
            preamble.append(line)
        else:
            current_lines.append(line)

    if current_title is not None:
        sections.append((current_title, current_lines))

    return preamble, sections


def parse_key_value_bullet(line: str) -> Optional[Tuple[str, str]]:
    stripped = line.strip()
    if not stripped.startswith("- "):
        return None
    body = stripped[2:]
    if ":" not in body:
        return None
    key, value = body.split(":", 1)
    return key.strip(), value.strip()


def collect_intro(lines: List[str]) -> Tuple[List[dict], List[str]]:
    meta: List[dict] = []
    paragraphs: List[str] = []
    current_paragraph: List[str] = []

    def flush_paragraph() -> None:
        nonlocal current_paragraph
        if current_paragraph:
            paragraphs.append(" ".join(part.strip() for part in current_paragraph if part.strip()))
            current_paragraph = []

    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            flush_paragraph()
            continue

        key_value = parse_key_value_bullet(stripped)
        if key_value:
            flush_paragraph()
            key, value = key_value
            meta.append({"key": key, "value": value})
            continue

        current_paragraph.append(stripped)

    flush_paragraph()
    return meta, paragraphs


def detect_slide_type(title: str, bullets: List[str], paragraphs: List[str]) -> str:
    lowered = title.lower()
    if lowered == "kpi":
        return "summary"
    if any(keyword in title for keyword in ["kpi", "结果", "总结", "下一步"]):
        return "summary"
    if bullets and not paragraphs:
        return "list"
    return "content"


def parse_section(title: str, lines: List[str], index: int) -> dict:
    bullets: List[str] = []
    paragraphs: List[str] = []
    tags: List[dict] = []
    current_paragraph: List[str] = []

    def flush_paragraph() -> None:
        nonlocal current_paragraph
        if current_paragraph:
            paragraphs.append(" ".join(part.strip() for part in current_paragraph if part.strip()))
            current_paragraph = []

    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            flush_paragraph()
            continue

        key_value = parse_key_value_bullet(stripped)
        if key_value:
            flush_paragraph()
            key, value = key_value
            if key in {"任务", "交付", "目标受众", "主风格", "开始日期", "用户收益", "范围边界", "下一步"}:
                tags.append({"key": key, "value": value})
            else:
                bullets.append(f"{key}：{value}")
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            bullets.append(stripped[4:].strip())
            continue

        if stripped.startswith(("- ", "* ")):
            flush_paragraph()
            bullets.append(stripped[2:].strip())
            continue

        current_paragraph.append(stripped)

    flush_paragraph()

    nav = re.sub(r"^阶段\s*\d+[:：]\s*", "", title).strip()
    nav = nav[:12] if nav else f"第{index + 1}页"

    return {
        "id": slugify(title),
        "nav": nav,
        "title": title,
        "type": detect_slide_type(title, bullets, paragraphs),
        "paragraphs": paragraphs,
        "bullets": bullets,
        "tags": tags,
    }

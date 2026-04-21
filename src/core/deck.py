"""Deck data model builder for LivePPT."""

from typing import Optional

from src.core.parser import collect_intro, extract_title, parse_section, split_sections


def build_deck(markdown_text: str, fallback_title: str, subtitle: Optional[str], brand: str, theme: str) -> dict:
    lines = markdown_text.splitlines()
    title, remaining = extract_title(lines, fallback_title)
    preamble, sections = split_sections(remaining)
    meta, intro_paragraphs = collect_intro(preamble)

    slides: list[dict] = [
        {
            "id": "cover",
            "nav": "封面",
            "title": title,
            "type": "cover",
            "paragraphs": intro_paragraphs,
            "bullets": [],
            "tags": meta,
        }
    ]

    if sections:
        for index, (section_title, section_lines) in enumerate(sections):
            slides.append(parse_section(section_title, section_lines, index + 1))
    elif intro_paragraphs:
        slides[0]["paragraphs"] = intro_paragraphs

    return {
        "title": title,
        "subtitle": subtitle or "把 plan.md 直接渲染成可打开、可翻页、可分享的 HTML 演示页。",
        "brand": brand,
        "theme": theme,
        "slides": slides,
    }

"""Word (.docx) to LivePPT Markdown converter."""

import logging
from pathlib import Path

from docx import Document
from docx.opc.exceptions import PackageNotFoundError

from src.converters.base import BaseConverter

logger = logging.getLogger(__name__)

HEADING_STYLES = {"Heading 1", "Heading 2", "Heading 3", "Heading 4"}
LIST_STYLES_PREFIX = "List"


class DocxConverter(BaseConverter):
    """Convert Word .docx documents to LivePPT-compatible Markdown.

    Mapping:
    - First Heading 1 -> # (deck title)
    - Heading 2 -> ## (slide boundary)
    - Heading 3 -> ### (sub-section within slide)
    - List Bullet / List Number -> - item
    - Normal paragraph -> body text
    - core_properties -> cover metadata
    """

    def convert(self, input_path: Path) -> str:
        try:
            doc = Document(str(input_path))
        except PackageNotFoundError:
            raise ValueError(f"Cannot open .docx file: {input_path}")

        paragraphs = doc.paragraphs
        if not paragraphs:
            return self._empty_deck(str(input_path.stem))

        lines: list[str] = []
        heading_1_seen = False

        # Extract metadata from core_properties
        props = doc.core_properties
        meta_lines: list[str] = []
        if props.title:
            meta_lines.append(f"- 项目名：{props.title}")
        if props.author:
            meta_lines.append(f"- 作者：{props.author}")
        if props.subject:
            meta_lines.append(f"- 主题：{props.subject}")

        for para in paragraphs:
            text = para.text.strip()
            if not text:
                continue

            style_name = para.style.name if para.style else ""

            if style_name in HEADING_STYLES:
                level = int(style_name.split()[-1]) if style_name.split()[-1].isdigit() else 1
                if level == 1:
                    if not heading_1_seen:
                        heading_1_seen = True
                        lines.append(f"# {text}")
                        # Add metadata after title
                        for ml in meta_lines:
                            lines.append(ml)
                        lines.append("")
                    else:
                        # Subsequent H1s become H2s
                        lines.append(f"## {text}")
                        lines.append("")
                elif level == 2:
                    lines.append(f"## {text}")
                    lines.append("")
                elif level == 3:
                    lines.append(f"### {text}")
                    lines.append("")
                else:
                    lines.append(f"## {text}")
                    lines.append("")
                continue

            # List items
            if style_name and style_name.startswith(LIST_STYLES_PREFIX):
                lines.append(f"- {text}")
                continue

            # Check for bullet-like paragraphs (starts with -, *, •, or number + .)
            if text.startswith(("- ", "* ", "• ")):
                lines.append(f"- {text.lstrip('-•* ')}")
                continue

            # Regular paragraph -> body text
            lines.append(text)
            lines.append("")

        # If no H1 was found, prepend one from core_properties or filename
        if not heading_1_seen:
            title = props.title or input_path.stem.replace("-", " ").replace("_", " ").title()
            final_lines = [f"# {title}", ""]
            if meta_lines:
                final_lines.extend(meta_lines)
                final_lines.append("")
            final_lines.extend(lines)
            lines = final_lines

        result = "\n".join(line for line in lines if line is not None)
        return result.strip() + "\n"

    def _empty_deck(self, title: str) -> str:
        return f"# {title}\n\n文档内容为空或无法解析。\n"

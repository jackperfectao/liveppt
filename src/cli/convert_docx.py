"""CLI: Convert Word .docx to LivePPT HTML deck."""

import argparse
import sys
import tempfile
from pathlib import Path

from src.converters.docx_converter import DocxConverter
from src.render.render_plan import render_markdown_to_html


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a Word .docx file into a LivePPT HTML deck")
    parser.add_argument("input", help="Input .docx file path")
    parser.add_argument("--output", required=True, help="Output HTML path")
    parser.add_argument("--title", help="Fallback title when doc has no H1")
    parser.add_argument("--subtitle", help="Custom subtitle for cover page")
    parser.add_argument("--brand", default="LivePPT", help="Brand text shown in deck")
    parser.add_argument("--theme", default="neo-luxury", help="Visual theme preset")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    converter = DocxConverter()
    markdown_text = converter.convert(input_path)

    fallback_title = args.title or input_path.stem.replace("-", " ").replace("_", " ").title()
    render_markdown_to_html(
        markdown_text=markdown_text,
        output_path=args.output,
        fallback_title=fallback_title,
        subtitle=args.subtitle,
        brand=args.brand,
        theme=args.theme,
    )


if __name__ == "__main__":
    main()

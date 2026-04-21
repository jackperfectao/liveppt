"""CLI: Convert PowerPoint .pptx to LivePPT HTML deck."""

import argparse
import sys
from pathlib import Path

from src.converters.pptx_converter import PptxConverter
from src.render.render_plan import render_markdown_to_html


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a PowerPoint .pptx file into a LivePPT HTML deck")
    parser.add_argument("input", help="Input .pptx file path")
    parser.add_argument("--output", required=True, help="Output HTML path")
    parser.add_argument("--title", help="Fallback title when pptx has no title")
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

    converter = PptxConverter()
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

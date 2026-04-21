"""CLI: Convert README.md to LivePPT HTML deck with cleaning."""

import argparse
import sys
import tempfile
from pathlib import Path

from src.cli.clean_markdown import clean_markdown
from src.render.render_plan import render_markdown_to_html


DEFAULT_SUBTITLE = "Turn your README into a clickable HTML deck without rebuilding your project as a frontend app."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a README.md into a standalone HTML deck")
    parser.add_argument("input", help="Input README markdown path")
    parser.add_argument("--output", required=True, help="Output HTML path")
    parser.add_argument("--theme", default="neo-luxury", help="Visual theme preset")
    parser.add_argument("--brand", default="LivePPT", help="Brand text shown in deck")
    parser.add_argument("--subtitle", default=DEFAULT_SUBTITLE, help="Cover subtitle")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    cleaned = clean_markdown(input_path.read_text(encoding="utf-8"))

    fallback_title = input_path.stem.replace("-", " ").replace("_", " ").title()
    render_markdown_to_html(
        markdown_text=cleaned,
        output_path=args.output,
        fallback_title=fallback_title,
        subtitle=args.subtitle,
        brand=args.brand,
        theme=args.theme,
    )
    print(f"README deck written to {args.output}")


if __name__ == "__main__":
    main()

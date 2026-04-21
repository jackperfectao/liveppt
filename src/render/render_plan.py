"""CLI entry point for rendering LivePPT markdown plan to HTML."""

import argparse
from pathlib import Path
from typing import Optional

from src.core.deck import build_deck
from src.core.themes import resolve_theme
from src.render.html_template import render_html


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render LivePPT markdown plan into a standalone HTML deck")
    parser.add_argument("input", help="Input markdown plan path")
    parser.add_argument("--output", required=True, help="Output HTML path")
    parser.add_argument("--title", help="Fallback title when markdown has no H1")
    parser.add_argument("--subtitle", help="Custom subtitle used on cover page")
    parser.add_argument("--brand", default="LivePPT", help="Brand text shown in deck")
    parser.add_argument("--theme", default="neo-luxury", help="Visual theme preset")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    markdown_text = input_path.read_text(encoding="utf-8")
    fallback_title = args.title or input_path.stem.replace("-", " ").replace("_", " ").title()
    deck = build_deck(markdown_text, fallback_title, args.subtitle, args.brand, args.theme)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html(deck, resolve_theme(args.theme)), encoding="utf-8")
    print(f"HTML deck written to {output_path}")


def render_markdown_to_html(
    markdown_text: str,
    output_path: str,
    fallback_title: str = "LivePPT Deck",
    subtitle: Optional[str] = None,
    brand: str = "LivePPT",
    theme: str = "neo-luxury",
) -> None:
    """Programmatic API: render markdown text to HTML file."""
    deck = build_deck(markdown_text, fallback_title, subtitle, brand, theme)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_html(deck, resolve_theme(theme)), encoding="utf-8")
    print(f"HTML deck written to {out}")


if __name__ == "__main__":
    main()

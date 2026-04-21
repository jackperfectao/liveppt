#!/usr/bin/env python3
"""Backward-compatible wrapper: delegate to src/cli/convert_pptx.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.cli.convert_pptx import main

if __name__ == "__main__":
    main()

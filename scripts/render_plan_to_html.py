#!/usr/bin/env python3
"""Backward-compatible wrapper: delegate to src/render/render_plan.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.render.render_plan import main

if __name__ == "__main__":
    main()

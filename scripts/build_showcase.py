#!/usr/bin/env python3
"""Backward-compatible wrapper: delegate to src/cli/build_showcase.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.cli.build_showcase import main

if __name__ == "__main__":
    main()

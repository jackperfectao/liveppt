"""Theme presets for LivePPT HTML deck rendering."""

from typing import Dict

THEMES: Dict[str, Dict[str, str]] = {
    "neo-luxury": {
        "bg": "#f6efe5",
        "bg_strong": "#fffaf2",
        "surface": "rgba(255,255,255,0.78)",
        "surface_strong": "rgba(255,255,255,0.92)",
        "line": "rgba(126, 90, 48, 0.18)",
        "text": "#2f2217",
        "text_soft": "#6d5437",
        "accent": "#b58a52",
        "accent_deep": "#8b6236",
        "success": "#5f8d68",
        "shadow": "0 20px 60px rgba(96, 65, 31, 0.12)",
    },
    "cyber-pulse": {
        "bg": "#08111f",
        "bg_strong": "#0d1728",
        "surface": "rgba(11,23,40,0.76)",
        "surface_strong": "rgba(16,30,51,0.92)",
        "line": "rgba(57, 196, 255, 0.22)",
        "text": "#ebf7ff",
        "text_soft": "#9dd8ff",
        "accent": "#39c4ff",
        "accent_deep": "#17f1d1",
        "success": "#79f0b0",
        "shadow": "0 24px 70px rgba(3, 10, 28, 0.38)",
    },
    "minimal-editorial": {
        "bg": "#f7f7f4",
        "bg_strong": "#ffffff",
        "surface": "rgba(255,255,255,0.75)",
        "surface_strong": "rgba(255,255,255,0.94)",
        "line": "rgba(58, 58, 58, 0.14)",
        "text": "#1f1f1f",
        "text_soft": "#555555",
        "accent": "#222222",
        "accent_deep": "#6f6f6f",
        "success": "#2e7d32",
        "shadow": "0 18px 48px rgba(30, 30, 30, 0.08)",
    },
    "prism-command": {
        "bg": "#0b1220",
        "bg_strong": "#121a2b",
        "surface": "rgba(16,24,40,0.76)",
        "surface_strong": "rgba(19,29,48,0.92)",
        "line": "rgba(96, 165, 250, 0.20)",
        "text": "#e8f1ff",
        "text_soft": "#9fb7d8",
        "accent": "#60a5fa",
        "accent_deep": "#22d3ee",
        "success": "#67e8a5",
        "shadow": "0 24px 72px rgba(2, 8, 23, 0.42)",
    },
}


def resolve_theme(theme: str) -> Dict[str, str]:
    """Return theme tokens by name, falling back to neo-luxury."""
    return THEMES.get(theme, THEMES["neo-luxury"])

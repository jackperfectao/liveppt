"""Base converter interface for document-to-Markdown conversion."""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseConverter(ABC):
    """Abstract base for all document converters."""

    @abstractmethod
    def convert(self, input_path: Path) -> str:
        """Convert input document to LivePPT-compatible Markdown string."""
        ...

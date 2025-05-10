"""Core functionality for PyArchitect.

This module provides core utilities for configuration parsing,
error handling, and CLI interface.
"""

from src.core.constants import single_form_words
from src.core.dependecies import container
from src.core.utils import camel_to_snake

__all__ = ["container", "single_form_words", "camel_to_snake"]

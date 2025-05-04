"""Configuration schemas for DDD architecture.

This module provides Pydantic models for validating and structuring
configuration data used in project generation.
"""

# src/schemas/__init__.py
from src.schemas.config_schema import ConfigModel

__all__ = ["ConfigModel"]

"""Generators for DDD architecture components.

This module provides generators for creating domain, application,
infrastructure, and interface layer components based on configuration.
"""

from .project_generator import ProjectGenerator

__all__ = ["ProjectGenerator"]

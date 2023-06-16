"""Main hub for backend."""

from pathlib import Path

BACKEND_DIR = Path(__file__).parent.parent
"""Root directory for backend."""


FRONTEND_BUILD_DIR = BACKEND_DIR.parent / "frontend/build"
"""Directory with frontend build."""

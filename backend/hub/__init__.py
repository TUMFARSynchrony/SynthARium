"""Main hub for backend."""

from pathlib import Path

BACKEND_DIR = Path(__file__).parent.parent
"""Root directory for backend."""

FRONTEND_DIR = BACKEND_DIR.parent / "frontend"
"""Root directory for frontend"""

FRONTEND_BUILD_DIR = FRONTEND_DIR / "build"
"""Directory with frontend build."""

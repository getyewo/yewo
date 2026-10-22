"""Yewo — AI-driven mobile end-to-end testing agent."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("yewo")
except PackageNotFoundError:  # pragma: no cover - only when run uninstalled
    # Running from a checkout that was never installed. The number is a
    # property of a release, and there is no release here to read one from.
    __version__ = "0.0.0+unreleased"

__all__ = ["__version__"]

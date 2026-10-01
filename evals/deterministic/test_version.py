"""DETERMINISTIC EVAL — one version, stated once, agreed everywhere.

Found 2026-08-22 while tagging the first release: `pyproject.toml` said 0.1.4
and `friday.__version__` said 0.1.0. Four releases of drift, invisible because
nothing reads `__version__` — so nothing could ever contradict it.

That is exactly why it needs a test rather than a habit. A version that only a
human compares is a version that silently goes wrong, and the first person to
notice is whoever is holding a wheel that claims to be something it isn't.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

import friday

REPO = Path(__file__).resolve().parents[2]


def _declared() -> str:
    with (REPO / "pyproject.toml").open("rb") as fh:
        return tomllib.load(fh)["project"]["version"]


def test_package_version_matches_pyproject():
    """THE regression. The wheel's version comes from pyproject; anything
    reading friday.__version__ must be told the same story."""
    assert friday.__version__ == _declared(), (
        f"friday.__version__ is {friday.__version__} but pyproject.toml declares "
        f"{_declared()}. Bump both, or the package reports a version it is not."
    )


def test_version_is_a_plain_release_number():
    """Three dotted integers. Catches a stray 'v' prefix or a leftover suffix,
    either of which changes the filename PyPI would accept - permanently."""
    parts = _declared().split(".")
    assert len(parts) == 3, f"expected MAJOR.MINOR.PATCH, got {_declared()!r}"
    assert all(p.isdigit() for p in parts), f"non-numeric component in {_declared()!r}"

"""DETERMINISTIC EVAL — the CLI must not die on a console that can't spell.

Found live on Windows 2026-08-22, from a clean `pip install` of the wheel: the
very first command a new user runs,

    friday --help

crashed with UnicodeEncodeError before printing anything. The help text has
arrows in it, and the Windows console still defaults to a legacy codepage
(cp1252) that has no glyph for them. Nothing in CI could see this — CI is
Ubuntu, where the default is UTF-8 and every character encodes fine.

The fix keeps whatever encoding the terminal actually uses and only softens the
failure mode, so a UTF-8 terminal keeps its glyphs and a legacy one degrades to
`?` instead of a traceback.
"""

from __future__ import annotations

import io
import subprocess
import sys

import pytest

import friday.__main__ as entry


def test_help_text_survives_a_legacy_codepage(monkeypatch, capsys):
    """THE regression: printing the help through a cp1252 stream must not raise."""
    cp1252 = io.TextIOWrapper(io.BytesIO(), encoding="cp1252", newline="")
    monkeypatch.setattr(sys, "stdout", cp1252)
    monkeypatch.setattr(sys, "stderr", cp1252)
    monkeypatch.setattr(sys, "argv", ["friday", "--help"])

    with pytest.raises(SystemExit) as exc:
        entry.main()
    assert exc.value.code == 1

    cp1252.flush()
    out = cp1252.buffer.getvalue().decode("cp1252")
    assert "friday dashboard" in out          # the help actually printed
    assert "friday connections" in out


def test_reconfigure_is_survivable_when_streams_are_not_real():
    """Captured or piped streams may not offer reconfigure(); that is not fatal."""
    class Dummy:
        pass

    import friday.__main__ as m
    saved = (sys.stdout, sys.stderr)
    try:
        sys.stdout = sys.stderr = Dummy()      # no .reconfigure at all
        m._survive_a_legacy_console()          # must not raise
    finally:
        sys.stdout, sys.stderr = saved


def test_help_runs_as_a_subprocess_under_a_legacy_codepage():
    """End to end, in a child process forced onto cp1252 — the shape of the
    real failure, which only showed up outside the test runner."""
    r = subprocess.run(
        [sys.executable, "-X", "utf8=0", "-m", "friday", "--help"],
        capture_output=True, timeout=60, check=False,   # --help exits 1 by design
        env={**_clean_env(), "PYTHONIOENCODING": "cp1252:strict"},
    )
    assert b"Traceback" not in r.stderr, r.stderr.decode("latin-1")[-400:]
    assert b"friday dashboard" in r.stdout


def _clean_env() -> dict:
    import os
    env = dict(os.environ)
    env.pop("PYTHONUTF8", None)
    return env

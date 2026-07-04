"""W8 -- the legacy-runtime retirement seam (plan §7 #2 / roadmap open-Q2).

The legacy execution runtime is retained as the differential *reference* through
P3 (not deleted at G1); ``legacy_status`` declares that role and gates it.
"""

import importlib

from zuspec.be.py.rt import legacy_status as ls


def test_status_declares_reference_role():
    st = ls.status()
    assert st["present"] is True
    assert st["role"] == "differential-reference"
    assert st["retire_at"] == "P3-exit"
    assert st["successor"] == "zuspec.be.bc.interp"


def test_retiring_modules_are_importable_today():
    # Retained through P3: every module scheduled for deletion still imports.
    for mod in ls.RETIRING_MODULES:
        importlib.import_module(mod)


def test_reference_flag_defaults_on(monkeypatch):
    monkeypatch.delenv("ZUSPEC_LEGACY_REFERENCE", raising=False)
    assert ls.legacy_reference_enabled() is True


def test_reference_flag_can_be_disabled(monkeypatch):
    monkeypatch.setenv("ZUSPEC_LEGACY_REFERENCE", "0")
    assert ls.legacy_reference_enabled() is False
    assert ls.status()["reference_enabled"] is False

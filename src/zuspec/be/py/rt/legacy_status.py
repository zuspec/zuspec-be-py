"""
legacy_status.py -- the legacy runtime's role marker + retirement seam (W8 / P1-14).

The ``zuspec-be-py`` execution runtime (``ScenarioRunner`` / ``ActivityRunner`` /
``Executor`` / ``CompiledScenario`` / ``ir_compiler``) is being **retired** in
favor of the ZBC oracle (``zuspec.be.bc.interp``), the validated successor
execution engine (differential suite T1-A).

Per the accepted decision (plan §7 #2 / roadmap open-Q2), the legacy runtime is
**not deleted at G1**. It is retained, importable, as a *second differential
reference* through P3 and deleted at P3 exit. This module makes that role explicit
and provides the gate the differential harness keys on, so the eventual deletion
is a localized change rather than an archaeological dig.

Nothing here changes execution behavior: the legacy runtime remains the default
production path at G1 (the ZBC engine is not yet feature-complete -- parallel /
select / loop lowering is still deferred). The marker is documentation-as-code
plus a single import seam.
"""

import os

#: True while the legacy Python execution runtime ships in this package.
LEGACY_RUNTIME_PRESENT = True

#: The runtime's role as of G1. It is the differential *reference* the ZBC oracle
#: is checked against, not the strategic production engine.
RUNTIME_ROLE = "differential-reference"

#: When the legacy runtime is scheduled for deletion (plan §7 #2).
RETIRE_AT = "P3-exit"

#: The successor execution engine (import path).
SUCCESSOR_ENGINE = "zuspec.be.bc.interp"

#: Modules quarantined/deleted at P3 exit (the production execution path).
RETIRING_MODULES = (
    "zuspec.be.py.rt.scenario_runner",
    "zuspec.be.py.rt.activity_runner",
    "zuspec.be.py.rt.executor",
    "zuspec.be.py.rt.compiled_scenario",
    "zuspec.be.py.rt.ir_compiler",
)

#: Environment flag that opts a test into using the legacy runtime as the
#: differential reference. Default on; set ``ZUSPEC_LEGACY_REFERENCE=0`` to assert
#: the reference is gone (e.g. after P3-exit deletion).
_ENV_FLAG = "ZUSPEC_LEGACY_REFERENCE"


def legacy_reference_enabled() -> bool:
    """Whether the legacy runtime should be used as a differential reference."""
    val = os.environ.get(_ENV_FLAG)
    if val is None:
        return LEGACY_RUNTIME_PRESENT
    return val not in ("0", "false", "False", "")


def status() -> dict:
    """A small structured summary of the legacy runtime's retirement status."""
    return {
        "present": LEGACY_RUNTIME_PRESENT,
        "role": RUNTIME_ROLE,
        "retire_at": RETIRE_AT,
        "successor": SUCCESSOR_ENGINE,
        "reference_enabled": legacy_reference_enabled(),
    }

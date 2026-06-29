"""Runtime object model for the zuspec Python backend (``zuspec.be.py``).

`Component` / `Action` / struct bases, scalar types (`u1..u64`, `bv[N]`, …),
field declarators (`field`, `pool`, `inst`, …), and claim pools that the
IR → live-Python builder uses to materialize runtime classes.

Formerly part of ``zuspec.dataclasses``; relocated here so the backend owns its
runtime model and ``zuspec.dataclasses`` can become a pure frontend.
``zuspec.dataclasses.types`` / ``.decorators`` now re-export from here.

NOTE (transitional): a few behaviors still reach back into
``zuspec.dataclasses`` via *lazy* (function-local) imports — RTL clock/reset
domains, the action/activity runtime under ``.rt``, the constraint solver, and
the ``activity()``-source parser.  These back-edges are dormant for the IR-driven
backend path and are removed as ``.rt`` / ``solver`` relocate in Phase 3.
"""
from . import types, decorators, domain  # noqa: F401

# Re-export the public object-model surface (scalar types, Component/Action,
# field declarators, @dataclass, clock/reset domains) so the backend can use
# ``from zuspec.be.py import model as zdc`` instead of importing the frontend.
from .types import *        # noqa: F401,F403
from .decorators import *   # noqa: F401,F403
from .domain import *       # noqa: F401,F403

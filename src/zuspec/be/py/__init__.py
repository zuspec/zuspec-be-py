"""Zuspec live-Python backend (``zuspec.be.py``).

Consumes a ``zuspec.ir.core`` model and projects it into executable Python
classes built on the ``zuspec.dataclasses`` (zdc) runtime — the Python
analogue of the ``zuspec.be.sv`` SystemVerilog backend.

The ``ExportApi`` projection (``registry.create()`` → per-run instances) is in
:mod:`zuspec.be.py.export_api`.
"""
from .__version__ import version as __version__
from .builder import IrToRuntimeBuilder, ClassRegistry, build_runtime
from .export_api import (
    ExportApi, ActionResult, ActionRunner, ActionProgram,
    build_registry, build_import_protocol, render_module,
)
from zuspec.dataclasses.rt.import_resolver import ImportSpec, ImportResolver, PssImportError

__all__ = [
    "__version__",
    # builder
    "IrToRuntimeBuilder",
    "ClassRegistry",
    "build_runtime",
    # export-api projection
    "ExportApi",
    "ActionResult",
    "ActionRunner",
    "ActionProgram",
    "build_registry",
    "build_import_protocol",
    "render_module",
    # import wiring (re-exported from the runtime)
    "ImportSpec",
    "ImportResolver",
    "PssImportError",
]

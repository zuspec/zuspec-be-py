"""Zuspec live-Python backend (``zuspec.be.py``).

Consumes a ``zuspec.ir.core`` model and projects it into executable Python
classes built on the runtime object model — the Python analogue of the
``zuspec.be.sv`` SystemVerilog backend.

The ``ExportApi`` projection (``registry.create()`` → per-run instances) is in
:mod:`zuspec.be.py.export_api`.

Public names are resolved lazily (PEP 562) so that importing
``zuspec.be.py`` (e.g. transitively, when ``zuspec.dataclasses`` re-exports the
runtime object model from :mod:`zuspec.be.py.model`) does not eagerly pull in
``builder``/``export_api`` — which import ``zuspec.dataclasses`` — and create a
``dataclasses`` ⇄ ``be.py`` import cycle.  The heavy submodules load on first
attribute access, by which point ``zuspec.dataclasses`` has finished loading.
"""
from .__version__ import version as __version__

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

# name -> (module, attribute) for lazy resolution
_LAZY = {
    "IrToRuntimeBuilder": (".builder", "IrToRuntimeBuilder"),
    "ClassRegistry": (".builder", "ClassRegistry"),
    "build_runtime": (".builder", "build_runtime"),
    "ExportApi": (".export_api", "ExportApi"),
    "ActionResult": (".export_api", "ActionResult"),
    "ActionRunner": (".export_api", "ActionRunner"),
    "ActionProgram": (".export_api", "ActionProgram"),
    "build_registry": (".export_api", "build_registry"),
    "build_import_protocol": (".export_api", "build_import_protocol"),
    "render_module": (".export_api", "render_module"),
    "ImportSpec": ("zuspec.be.py.rt.import_resolver", "ImportSpec"),
    "ImportResolver": ("zuspec.be.py.rt.import_resolver", "ImportResolver"),
    "PssImportError": ("zuspec.be.py.rt.import_resolver", "PssImportError"),
}


def __getattr__(name):
    target = _LAZY.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    import importlib
    mod_name, attr = target
    mod = importlib.import_module(mod_name, __name__ if mod_name.startswith(".") else None)
    value = getattr(mod, attr)
    globals()[name] = value  # cache for subsequent access
    return value


def __dir__():
    return sorted(__all__)

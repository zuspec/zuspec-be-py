"""The export-api projection — run a PSS model as a live Python object.

Mirrors the SystemVerilog ``oo_api`` projection: a reusable registry acts as the
factory, and ``registry.create(imports, seed)`` yields a per-run
:class:`ExportApi` whose async methods invoke exported action traversals
(``pre_solve`` → ``randomize`` → ``post_solve`` → ``activity``/``body``).

This is an **API-only** capability — there is no CLI surface.  Drive it from a
Python environment (standalone scripts, pytest, cocotb, …)::

    registry = build_registry(ctx, export_actions=["Top::Go"])
    ep = registry.create(MyImports(), seed=1)
    await ep.Go()
"""
from __future__ import annotations

import dataclasses as _dc
from typing import Any, Dict, List, Optional

from zuspec.be.py.rt.scenario_runner import ScenarioRunner
from zuspec.be.py.rt.import_resolver import ImportResolver, ImportSpec

from .builder import build_runtime, ClassRegistry


# ---------------------------------------------------------------------------
# Result + command-pattern helpers
# ---------------------------------------------------------------------------

class ActionResult:
    """The outcome of one exported-action invocation.

    Wraps the solved root-action instance (randomized field values); attribute
    access is proxied to it, so ``result.addr`` reads the solved action field.
    """

    __slots__ = ("action",)

    def __init__(self, action: Any):
        object.__setattr__(self, "action", action)

    def __getattr__(self, name: str) -> Any:
        return getattr(object.__getattribute__(self, "action"), name)

    def __repr__(self) -> str:
        return f"ActionResult({self.action!r})"


class ActionRunner:
    """A bound, replayable invocation of one exported action (Command pattern).

    Mirrors the SV ``<action>_runner`` / ``pss_action_run_if`` facade: a uniform
    ``await run()`` that invokes the action through its :class:`ExportApi`.
    """

    def __init__(self, api: "ExportApi", method_name: str):
        self._api = api
        self._name = method_name

    async def run(self) -> ActionResult:
        return await getattr(self._api, self._name)()

    def __repr__(self) -> str:
        return f"ActionRunner({self._name})"


class ActionProgram:
    """An ordered, heterogeneous sequence of :class:`ActionRunner` invocations."""

    def __init__(self, runners: List[ActionRunner]):
        self._runners = list(runners)

    async def run(self) -> List[ActionResult]:
        return [await r.run() for r in self._runners]


# ---------------------------------------------------------------------------
# ExportApi
# ---------------------------------------------------------------------------

class ExportApi:
    """A per-run handle exposing one async method per exported action.

    Construct via :meth:`ClassRegistry.create`.  Holds a fresh component tree and
    a seeded :class:`ScenarioRunner` wired with the import resolver; each
    ``await ep.<Action>()`` runs that action's full lifecycle against the tree.
    """

    def __init__(self, registry: ClassRegistry, comp: Any, runner: ScenarioRunner):
        self._registry = registry
        self._comp = comp
        self._runner = runner
        self._actions: Dict[str, str] = {}   # method name -> qualified action name

    # --- construction ----------------------------------------------------

    @classmethod
    def _build(cls, registry: ClassRegistry, *, imports=None, seed=None,
               root: Optional[str] = None) -> "ExportApi":
        export_qnames = list(registry.export_actions) or registry.action_qnames()

        root_name = root or registry.root_component_name(export_qnames)
        root_cls = registry[root_name]
        comp = root_cls()

        specs = registry.import_specs
        resolver = (ImportResolver(imports, specs)
                    if (specs or imports is not None) else None)
        runner = ScenarioRunner(comp, seed=seed, import_resolver=resolver)

        api = cls(registry, comp, runner)
        for qname in export_qnames:
            api._bind_action(qname)
        return api

    def _bind_action(self, qname: str) -> None:
        name = qname.rsplit("::", 1)[-1]
        # On a short-name collision across components, fall back to the mangled
        # qualified name so neither action is shadowed.
        if name in self._actions and self._actions[name] != qname:
            name = qname.replace("::", "__")
        self._actions[name] = qname

        async def _invoke(**inline_constraints):
            return await self._run(qname, **inline_constraints)

        _invoke.__name__ = name
        _invoke.__qualname__ = f"ExportApi.{name}"
        object.__setattr__(self, name, _invoke)

    # --- invocation ------------------------------------------------------

    async def _run(self, qname: str, **inline_constraints) -> ActionResult:
        if inline_constraints:
            raise NotImplementedError(
                "inline constraints on exported actions are not yet supported")
        action_cls = self._registry[qname]
        solved = await self._runner.run(action_cls)
        return ActionResult(solved)

    # --- introspection / command pattern ---------------------------------

    @property
    def actions(self) -> List[str]:
        """Method names exposed for the exported actions."""
        return list(self._actions)

    def runner(self, name: str) -> ActionRunner:
        """A :class:`ActionRunner` bound to exported action *name*."""
        if name not in self._actions:
            raise KeyError(f"no exported action method '{name}' "
                           f"(have: {sorted(self._actions)})")
        return ActionRunner(self, name)

    def program(self, names: List[str]) -> ActionProgram:
        """An ordered program over exported action method *names*."""
        return ActionProgram([self.runner(n) for n in names])

    def __repr__(self) -> str:
        return f"ExportApi(root={type(self._comp).__name__}, actions={self.actions})"


# ---------------------------------------------------------------------------
# Import-api stub generation
# ---------------------------------------------------------------------------

def build_import_protocol(import_specs: Dict[str, ImportSpec]) -> type:
    """Return a structural stub class naming the imports the model requires.

    A lightweight reference for editors / type-checkers; supply an object with
    these methods to :meth:`ClassRegistry.create`.
    """
    ns: Dict[str, Any] = {
        "__doc__": "Structural reference for the imports this model requires.",
        "__pss_imports__": dict(import_specs),
    }
    for name in import_specs:
        ns[name] = None
    return type("ImportApi", (), ns)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

_MODULE_TEMPLATE = '''\
"""{doc}

Generated by zuspec-be-py — do not edit.

This module embeds the model's serialized IR and rebuilds the registry on import
(no PSS re-parse).  Import it and drive ``registry`` like a ``load_pss(...)`` one::

    from {modname} import registry
    ep = registry.create(MyImports(), seed=1)
    await ep.{first_action}()
"""
import base64 as _b64

import zuspec.ir.core as _ir
from zuspec.be.py import build_registry as _build_registry, ImportSpec as _ImportSpec

_IR_B64 = (
{ir_chunks}
)

_EXPORT_ACTIONS = {export_actions!r}
_IMPORT_SPECS = {import_specs!r}
_OWNER_MAP = {owner_map!r}


def load():
    """Reconstruct the registry from the embedded IR."""
    _deser = _ir.IRDeserializer()
    _deser.auto_register(_ir)
    _ctx, _ = _deser.deserialize(_b64.b64decode(_IR_B64).decode("utf-8"))
    _specs = {{n: _ImportSpec(name=n, **kw) for n, kw in _IMPORT_SPECS.items()}}
    return _build_registry(
        _ctx,
        export_actions=_EXPORT_ACTIONS,
        import_specs=_specs,
        owner_map=_OWNER_MAP,
    )


registry = load()
'''


def render_module(registry: ClassRegistry, *, module_doc=None,
                  modname: str = "model") -> str:
    """Render the source of a self-contained module reconstructing *registry*.

    See :meth:`ClassRegistry.emit_module`.
    """
    import base64
    import zuspec.ir.core as ir

    yaml = ir.IRSerializer().serialize(ir.Context(type_m=registry._type_m), "be-py")
    b64 = base64.b64encode(yaml.encode("utf-8")).decode("ascii")
    # Wrap the base64 blob into adjacent string literals for readability/line length.
    width = 76
    chunks = "\n".join(
        f'    "{b64[i:i + width]}"' for i in range(0, len(b64), width)
    ) or '    ""'

    export_actions = list(registry.export_actions)
    import_specs = {
        n: {"is_target": bool(s.is_target), "is_solve": bool(s.is_solve)}
        for n, s in registry.import_specs.items()
    }
    first_action = (export_actions[0].rsplit("::", 1)[-1]
                    if export_actions else "Action")

    return _MODULE_TEMPLATE.format(
        doc=module_doc or "PSS model (live-Python projection).",
        modname=modname,
        first_action=first_action,
        ir_chunks=chunks,
        export_actions=export_actions,
        import_specs=import_specs,
        owner_map=dict(registry.owner_map),
    )


def build_registry(ctx, *, export_actions=None, import_specs=None,
                   owner_map=None) -> ClassRegistry:
    """Build a :class:`ClassRegistry`, configured for the export-api projection.

    *ctx* is a :class:`zuspec.ir.core.Context`.  *export_actions* are qualified
    action names to expose (default: all actions).  *import_specs* maps each
    import name to an :class:`ImportSpec`.
    """
    import_names = set(import_specs) if import_specs else None
    reg = build_runtime(ctx, owner_map=owner_map, import_names=import_names)
    reg.configure_exports(export_actions=export_actions, import_specs=import_specs)
    return reg

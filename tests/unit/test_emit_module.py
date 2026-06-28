"""AOT module emission (Phase 5 B2).

``registry.emit_module(path)`` writes a self-contained module that embeds the
serialized IR and rebuilds the registry on import (no re-parse).  These tests
emit, import the generated module, and run it — asserting parity with the
in-memory registry.
"""
import importlib.util

import pytest

import zuspec.ir.core as ir
from zuspec.be.py import build_registry, ImportSpec
from zuspec.ir.core.expr import ExprConstant, ExprAttribute, TypeExprRefSelf, ExprCall
from zuspec.ir.core.stmt import StmtExpr

pytestmark = pytest.mark.anyio


def _self_call(name, *args):
    return ExprCall(func=ExprAttribute(value=TypeExprRefSelf(), attr=name), args=list(args))


def _ctx_atomic():
    go = ir.DataTypeClass(
        name="Go", super=None,
        fields=[ir.Field(name="addr", datatype=ir.DataTypeInt(bits=8, signed=False),
                         rand_kind=ir.RandKind.RAND)],
    )
    top = ir.DataTypeComponent(name="Top", super=None)
    return ir.Context(type_m={"Top": top, "Top::Go": go})


def _ctx_with_imports():
    body = ir.Function(name="body", body=[
        StmtExpr(expr=_self_call("doit", _self_call("getval", ExprConstant(value=7)))),
    ])
    go = ir.DataTypeClass(name="Go", super=None, functions=[body])
    top = ir.DataTypeComponent(name="Top", super=None)
    return ir.Context(type_m={"Top": top, "Top::Go": go})


def _import_generated(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


async def test_emitted_module_rebuilds_and_runs(tmp_path):
    reg = build_registry(_ctx_atomic(), export_actions=["Top::Go"])
    path = tmp_path / "atomic_model.py"
    reg.emit_module(path)

    mod = _import_generated(path, "atomic_model")
    # The generated module exposes a rebuilt registry with the same config.
    assert mod.registry.export_actions == ["Top::Go"]
    ep = mod.registry.create(seed=1)
    assert ep.actions == ["Go"]
    result = await ep.Go()
    assert 0 <= int(result.addr) <= 255


async def test_emitted_module_preserves_imports_and_body(tmp_path):
    reg = build_registry(
        _ctx_with_imports(),
        export_actions=["Top::Go"],
        import_specs={
            "doit": ImportSpec(name="doit", is_target=True),
            "getval": ImportSpec(name="getval", is_solve=True),
        },
    )
    path = tmp_path / "import_model.py"
    src = reg.emit_module(path)
    assert "_IR_B64" in src and "def load" in src

    mod = _import_generated(path, "import_model")
    assert set(mod.registry.import_specs) == {"doit", "getval"}

    calls = []

    class Imp:
        def getval(self, i):
            return i + 5

        def doit(self, i):
            calls.append(i)

    ep = mod.registry.create(Imp())
    await ep.Go()
    assert calls == [12]      # body doit(getval(7)) survived the round-trip


async def test_emit_module_returns_source_without_path():
    reg = build_registry(_ctx_atomic(), export_actions=["Top::Go"])
    src = reg.emit_module(module_doc="My model")
    assert src.startswith('"""My model')
    assert "registry = load()" in src

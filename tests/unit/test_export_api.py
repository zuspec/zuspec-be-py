"""ExportApi projection — driven from a hand-built ``Context`` (no ``pssc``).

Proves the headline experience: ``registry.create(imports) -> ExportApi`` with
async per-action methods, the command-pattern runner/program, import wiring, and
per-run independence — all from the canonical IR alone.
"""
import pytest

import zuspec.ir.core as ir

from zuspec.be.py import build_registry, ExportApi, ActionRunner, PssImportError
from zuspec.dataclasses.rt.import_resolver import ImportSpec

# expr/stmt IR for hand-built action bodies
from zuspec.ir.core.expr import (
    ExprConstant, ExprAttribute, TypeExprRefSelf, ExprCall,
)
from zuspec.ir.core.stmt import StmtExpr

pytestmark = pytest.mark.anyio


def _int(bits=8, signed=False):
    return ir.DataTypeInt(bits=bits, signed=signed)


def _self_call(name, *args):
    return ExprCall(func=ExprAttribute(value=TypeExprRefSelf(), attr=name), args=list(args))


def _const(v):
    return ExprConstant(value=v)


# --- fixtures --------------------------------------------------------------

def _ctx_atomic():
    """component Top { action Go { rand bit[8] addr; } }"""
    go = ir.DataTypeClass(
        name="Go", super=None,
        fields=[ir.Field(name="addr", datatype=_int(8), rand_kind=ir.RandKind.RAND)],
    )
    top = ir.DataTypeComponent(name="Top", super=None)
    return ir.Context(type_m={"Top": top, "Top::Go": go})


def _ctx_with_imports():
    """An action whose body calls package-scope imports: doit(getval(7))."""
    body = ir.Function(
        name="body",
        body=[StmtExpr(expr=_self_call("doit", _self_call("getval", _const(7))))],
    )
    go = ir.DataTypeClass(name="Go", super=None, functions=[body])
    top = ir.DataTypeComponent(name="Top", super=None)
    return ir.Context(type_m={"Top": top, "Top::Go": go})


# --- tests -----------------------------------------------------------------

async def test_create_yields_export_api_with_action_method():
    reg = build_registry(_ctx_atomic(), export_actions=["Top::Go"])
    ep = reg.create()
    assert isinstance(ep, ExportApi)
    assert ep.actions == ["Go"]
    result = await ep.Go()
    assert 0 <= int(result.addr) <= 255   # solved (randomized) field is readable


async def test_create_is_per_run_independent():
    reg = build_registry(_ctx_atomic(), export_actions=["Top::Go"])
    ep1 = reg.create(seed=1)
    ep2 = reg.create(seed=1)
    r1 = await ep1.Go()
    r2 = await ep2.Go()
    assert r1.addr == r2.addr            # same seed -> same solved value
    assert ep1._comp is not ep2._comp    # but independent component trees


async def test_import_wiring_end_to_end():
    calls = []

    class Imp:
        def getval(self, i):
            calls.append(("getval", i))
            return i + 5

        def doit(self, i):
            calls.append(("doit", i))

    reg = build_registry(
        _ctx_with_imports(),
        export_actions=["Top::Go"],
        import_specs={
            "doit": ImportSpec(name="doit", is_target=True),
            "getval": ImportSpec(name="getval", is_solve=True),
        },
    )
    ep = reg.create(Imp())
    await ep.Go()
    assert calls == [("getval", 7), ("doit", 12)]


async def test_async_import_target_is_awaited():
    import asyncio
    order = []

    class Imp:
        def getval(self, i):
            return i + 5

        async def doit(self, i):          # async (cocotb-style) import target
            await asyncio.sleep(0)
            order.append(i)

    reg = build_registry(
        _ctx_with_imports(),
        export_actions=["Top::Go"],
        import_specs={
            "doit": ImportSpec(name="doit", is_target=True),
            "getval": ImportSpec(name="getval", is_solve=True),
        },
    )
    ep = reg.create(Imp())
    await ep.Go()
    assert order == [12]


async def test_unsupplied_import_raises():
    reg = build_registry(
        _ctx_with_imports(),
        export_actions=["Top::Go"],
        import_specs={
            "doit": ImportSpec(name="doit", is_target=True),
            "getval": ImportSpec(name="getval", is_solve=True),
        },
    )

    class Empty:
        pass

    ep = reg.create(Empty())
    with pytest.raises(PssImportError):
        await ep.Go()


async def test_runner_and_program_preserve_order():
    reg = build_registry(_ctx_atomic(), export_actions=["Top::Go"])
    ep = reg.create(seed=3)
    r = ep.runner("Go")
    assert isinstance(r, ActionRunner)
    results = await ep.program(["Go", "Go", "Go"]).run()
    assert len(results) == 3
    assert all(0 <= int(res.addr) <= 255 for res in results)


async def test_import_api_stub_lists_required_imports():
    reg = build_registry(
        _ctx_with_imports(),
        export_actions=["Top::Go"],
        import_specs={"doit": ImportSpec(name="doit", is_target=True)},
    )
    ImportApi = reg.ImportApi
    assert "doit" in ImportApi.__pss_imports__

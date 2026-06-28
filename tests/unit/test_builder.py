"""Builder unit tests — driven by a hand-built ``zuspec.ir.core.Context``.

These tests deliberately avoid ``pssc``: they prove the backend builds live
Python classes from the canonical IR alone, which is the package-boundary
invariant for ``zuspec-be-py``.
"""
import dataclasses as dc
import enum as pyenum

import zuspec.dataclasses as zdc
import zuspec.ir.core as ir

from zuspec.be.py import IrToRuntimeBuilder, ClassRegistry, build_runtime


def _int(bits=8, signed=False):
    return ir.DataTypeInt(bits=bits, signed=signed)


def _ctx():
    """A tiny model: component Top with atomic action Top::Go, plus a struct and enum."""
    color = ir.DataTypeEnum(name="Color", items={"RED": 0, "GREEN": 1, "BLUE": 2})

    pkt = ir.DataTypeStruct(
        name="Pkt", super=None,
        fields=[ir.Field(name="len", datatype=_int(8))],
    )

    go = ir.DataTypeClass(
        name="Go", super=None,
        fields=[ir.Field(name="addr", datatype=_int(8), rand_kind=ir.RandKind.RAND)],
    )

    top = ir.DataTypeComponent(name="Top", super=None)

    return ir.Context(type_m={
        "Color": color,
        "Pkt": pkt,
        "Top": top,
        "Top::Go": go,
    })


def test_builds_from_pure_context_no_pss():
    reg = build_runtime(_ctx())
    assert isinstance(reg, ClassRegistry)
    assert {"Color", "Pkt", "Top", "Top::Go"} <= set(reg.keys())


def test_class_shapes():
    reg = build_runtime(_ctx())

    # Component -> zdc.Component subclass
    assert issubclass(reg["Top"], zdc.Component)

    # Action -> zdc.Action subclass
    assert issubclass(reg["Top::Go"], zdc.Action)

    # Enum -> IntEnum with the declared members
    Color = reg["Color"]
    assert issubclass(Color, pyenum.IntEnum)
    assert Color.GREEN == 1

    # Struct -> plain dataclass value container
    assert dc.is_dataclass(reg["Pkt"])


def test_owner_map_derived_attaches_action_to_component():
    reg = build_runtime(_ctx())
    # Owner derivation maps 'Top::Go' -> 'Top', so the action is exposed as an
    # attribute on its component class.
    assert hasattr(reg["Top"], "Go")
    assert reg["Top"].Go is reg["Top::Go"]


def test_owner_map_derivation_excludes_non_component_prefix():
    # A package-qualified action whose prefix is NOT a component must not be
    # treated as component-owned.
    ctx = _ctx()
    ctx.type_m["pkg::Free"] = ir.DataTypeClass(name="Free", super=None)

    builder = IrToRuntimeBuilder(ctx)
    assert builder._owner_map == {"Top::Go": "Top"}
    assert "pkg::Free" not in builder._owner_map


def test_explicit_owner_map_overrides_derivation():
    ctx = _ctx()
    builder = IrToRuntimeBuilder(ctx, owner_map={})
    # With an empty explicit map, the action has no owner and is not attached.
    assert builder._owner_map == {}
    reg = builder.build()
    assert not hasattr(reg["Top"], "Go")


def test_legacy_type_map_context_is_tolerated():
    # A producer exposing the legacy ``type_map`` attribute still works.
    class LegacyCtx:
        def __init__(self, type_m):
            self.type_map = type_m

    reg = build_runtime(LegacyCtx(_ctx().type_m))
    assert issubclass(reg["Top::Go"], zdc.Action)

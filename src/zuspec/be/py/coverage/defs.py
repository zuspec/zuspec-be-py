"""
Runtime definitions for Python-native covergroups.

These records hold the Python callables (``ref``, ``iff``) taken from the
covergroup descriptors. They belong to the Python runtime; the IR model in
``zuspec.ir.core.coverage`` is pure data (expressions, no callables).
"""
import dataclasses
from typing import Optional, List, Union, Callable, Any


@dataclasses.dataclass
class CoverpointDef:
    """Runtime definition of a coverpoint."""
    name: str
    field_type: type
    ref: Optional[Callable]
    bins: List['BinDef']
    auto_bins: bool
    auto_bin_max: int
    iff: Optional[Callable] = None
    weight: int = 1
    goal: int = 100
    comment: str = ""
    loc: Optional[Any] = None


@dataclasses.dataclass
class BinDef:
    """Runtime definition of a single bin."""
    name: str
    values: Union[range, List[int], int]
    is_ignore: bool = False
    is_illegal: bool = False
    is_default: bool = False
    iff: Optional[Callable] = None
    loc: Optional[Any] = None


@dataclasses.dataclass
class CrossDef:
    """Runtime definition of a cross."""
    name: str
    coverpoint_refs: List[Callable]
    bins: List[Any] = dataclasses.field(default_factory=list)
    auto_bins: bool = True
    iff: Optional[Callable] = None
    weight: int = 1
    goal: int = 100
    comment: str = ""
    loc: Optional[Any] = None

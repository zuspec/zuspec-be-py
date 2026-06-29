"""Zuspec Python runtime (``zuspec.be.py.rt``).

The PSS execution runtime (action/activity/scenario execution, resource claiming,
IR statement/expr evaluation) plus the RTL behavioural-simulation runtime
(clock/reset domains, tracers, pipeline). Relocated here from
``zuspec.dataclasses.rt`` so the Python backend owns its runtime; ``zuspec.dataclasses``
re-exports it (see docs/be-py-runtime-relocation-design.md, Phase 3).

Names are resolved lazily (PEP 562) so that importing a single PSS-execution
submodule (e.g. ``zuspec.be.py.rt.scenario_runner``) does NOT eagerly pull in the
RTL-sim modules (``obj_factory``, ``tracer``, ``pipeline_rt`` …), some of which
carry lazy back-edges to the ``zuspec.dataclasses`` frontend.  This keeps backend
imports cycle-free.
"""

# name -> (submodule, attribute)
_LAZY = {
    "ObjFactory": (".obj_factory", "ObjFactory"),
    "Timebase": (".timebase", "Timebase"),
    "MemoryRT": (".memory_rt", "MemoryRT"),
    "AddrHandleRT": (".addr_handle_rt", "AddrHandleRT"),
    "AddressSpaceRT": (".address_space_rt", "AddressSpaceRT"),
    "ChannelRT": (".channel_rt", "ChannelRT"),
    "GetIFRT": (".channel_rt", "GetIFRT"),
    "PutIFRT": (".channel_rt", "PutIFRT"),
    "LockRT": (".lock_rt", "LockRT"),
    "EventRT": (".event_rt", "EventRT"),
    "Tracer": (".tracer", "Tracer"),
    "SignalTracer": (".tracer", "SignalTracer"),
    "Thread": (".tracer", "Thread"),
    "with_tracer": (".tracer", "with_tracer"),
    "VCDTracer": (".vcd_tracer", "VCDTracer"),
    "posedge": (".edge", "posedge"),
    "negedge": (".edge", "negedge"),
    "edge": (".edge", "edge"),
    "ObjectExecutor": (".executor", "ObjectExecutor"),
    "SimDomain": (".sim_domain", "SimDomain"),
}

__all__ = list(_LAZY)


def __getattr__(name):
    target = _LAZY.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    import importlib
    mod = importlib.import_module(target[0], __name__)
    value = getattr(mod, target[1])
    globals()[name] = value
    return value


def __dir__():
    return sorted(__all__)

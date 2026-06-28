# Zuspec live-Python Backend

`zuspec-be-py` is the live-Python backend for Zuspec — the Python analogue of
[`zuspec-be-sv`](https://github.com/zuspec/zuspec-be-sv). It consumes a
`zuspec.ir.core.Context` and projects it into executable Python classes built on
the [`zuspec-dataclasses`](https://github.com/zuspec/zuspec-dataclasses) (zdc)
runtime, so a PSS model can be loaded and driven directly from Python.

On top of the class builder, the **export-api projection** runs a model as a live
Python object — mirroring the SystemVerilog `oo_api` projection: build a
registry, supply an import-API implementation, then `await` exported actions to
run their traversals (`pre_solve → randomize → post_solve → activity/body`).

This is an **API-only** capability (standalone scripts, pytest, cocotb). There is
no CLI.

## Quick start

From PSS source, the easiest entry point is `pssc.load_pss`, which returns a
`zuspec-be-py` registry:

```python
import asyncio
from pssc import load_pss

registry = load_pss(open("model.pss").read())   # parse + elaborate once (reusable)
ep = registry.create(seed=1)                     # a runnable, per-run instance
asyncio.run(ep.Entry())                          # run the exported action
```

Supplying imports (the model calling out to your code — sync or `async`):

```python
class MyImports:
    def getval(self, i): return i + 5            # import solve (pure)
    async def doit(self, i): print(f"[imp] doit({i})")   # import target (awaited)

ep = registry.create(MyImports())
await ep.Entry()                                 # prints: [imp] doit(12)
```

Driving from a `zuspec.ir.core.Context` directly (any IR producer, not just PSS):

```python
from zuspec.be.py import build_registry, ImportSpec

registry = build_registry(ctx, export_actions=["Top::Go"],
                          import_specs={"doit": ImportSpec(name="doit", is_target=True)})
ep = registry.create(MyImports(), seed=1)
await ep.Go()
```

## Public API

| Name | Role |
| --- | --- |
| `build_registry(ctx, *, export_actions, import_specs, owner_map)` | build a registry configured for the export-api projection |
| `build_runtime(ctx, *, owner_map, import_names)` | build a plain `ClassRegistry` of live classes |
| `ClassRegistry.create(imports=None, *, seed=None, root=None)` | factory → per-run `ExportApi` |
| `ClassRegistry.emit_module(path)` | ship a model: emit a self-contained `.py` (embedded IR) that rebuilds on import, no re-parse |
| `ExportApi` | per-run handle; one `async` method per exported action; `runner()` / `program()` |
| `ActionResult` | the solved root-action instance (attribute access proxied) |
| `ActionRunner` / `ActionProgram` | command-pattern, ordered replay |
| `ImportSpec` / `ImportResolver` / `PssImportError` | import wiring (re-exported from the runtime) |
| `IrToRuntimeBuilder` | the IR → live-class builder |

The builder is **PSS-agnostic**: it consumes the canonical IR (`Context.type_m`)
plus an action→component `owner_map` (derived from `Comp::Action` keys when not
supplied), and never imports `pssc`.

## Layout

```
src/zuspec/be/py/
  builder.py        IrToRuntimeBuilder / ClassRegistry  (IR -> live zdc classes)
  export_api.py     ExportApi / ActionRunner / build_registry  (the projection)
docs/               Sphinx documentation
tests/              unit tests
```

## Documentation

Build the HTML docs:

```bash
cd docs && make html      # -> docs/_build/html/index.html
```

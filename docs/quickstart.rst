Quickstart
==========

This guide gets you running a PSS model as a live Python object in a few minutes.
It is an **API-only** workflow — drive it from a script, a ``pytest`` test, or a
cocotb testbench. There is no CLI.

Load and run
------------

``pssc.load_pss`` parses PSS source and returns a ``zuspec-be-py`` registry. The
registry is the reusable factory; ``create()`` produces a runnable instance:

.. code-block:: python

   import asyncio
   from pssc import load_pss

   registry = load_pss("""
       component pss_top {
           action Entry {
               rand bit[8] addr;
               constraint addr % 4 == 0;
           }
       }
   """)

   ep = registry.create(seed=7)       # fresh component tree, seeded
   result = asyncio.run(ep.Entry())   # pre_solve -> randomize -> post_solve -> body
   assert result.addr % 4 == 0        # read a solved field off the result

Each exported action is an ``async`` method on the instance. ``await ep.Entry()``
returns an :class:`~zuspec.be.py.ActionResult` that proxies attribute access to
the solved root-action instance.

Supplying imports
-----------------

Package-scope ``import target`` / ``import solve`` functions are calls *out* of
the model. Supply them as an object passed to ``create()``:

.. code-block:: python

   class MyImports:
       def getval(self, i: int) -> int:        # import solve (pure, sync)
           return i + 5
       async def doit(self, i: int) -> None:    # import target (may await)
           print(f"[imp] doit({i})")

   ep = registry.create(MyImports())
   await ep.Entry()                             # prints: [imp] doit(12)

* ``import solve`` functions are pure/synchronous.
* ``import target`` functions may be synchronous **or** ``async def`` — an async
  target is awaited inside the action body (this is the cocotb path).
* Calling an unsupplied import raises :class:`~zuspec.be.py.PssImportError`.

Choosing exported actions
-------------------------

By default the single root action is auto-detected. Name a set explicitly:

.. code-block:: python

   registry = load_pss(text, export_actions=["pss_top::Entry", "pss_top::Reset"])
   ep = registry.create()
   await ep.Entry()
   await ep.Reset()

Reuse and determinism
---------------------

The registry is parsed once and reused; ``create()`` is per-run. The same seed
against the same registry yields the same solved values:

.. code-block:: python

   a = registry.create(seed=42)
   b = registry.create(seed=42)
   assert (await a.Entry()).addr == (await b.Entry()).addr

Ordered programs
----------------

Compose a heterogeneous, ordered sequence of invocations (the Command pattern):

.. code-block:: python

   ep = registry.create()
   results = await ep.program(["Entry", "Reset", "Entry"]).run()

Driving from the IR directly
----------------------------

If you already have a :class:`zuspec.ir.core.Context` (not from PSS), build a
registry directly:

.. code-block:: python

   from zuspec.be.py import build_registry, ImportSpec

   registry = build_registry(
       ctx,
       export_actions=["Top::Go"],
       import_specs={"doit": ImportSpec(name="doit", is_target=True)},
   )
   ep = registry.create(MyImports(), seed=1)
   await ep.Go()

Examples
========

Atomic action
-------------

.. code-block:: python

   import asyncio
   from pssc import load_pss

   registry = load_pss("""
       component pss_top {
           action Entry { rand bit[8] addr; constraint addr % 4 == 0; }
       }
   """)
   ep = registry.create(seed=7)
   result = asyncio.run(ep.Entry())
   assert result.addr % 4 == 0

Imports (sync solve + async target)
-----------------------------------

.. code-block:: python

   registry = load_pss("""
       package dut_api {
           import target function void doit(int i);
           import solve  function int  getval(int i);
       }
       component pss_top {
           import dut_api::*;
           action Entry { exec body { doit(getval(7)); } }
       }
   """)

   class Imports:
       def getval(self, i): return i + 5
       async def doit(self, i): print(f"[imp] doit({i})")

   ep = registry.create(Imports())
   asyncio.run(ep.Entry())            # prints: [imp] doit(12)

cocotb testbench
----------------

Because exported actions are just ``async`` Python and ``import target`` calls
are awaited, a model drives a DUT through your bus methods:

.. code-block:: python

   import cocotb
   from pssc import load_pss

   class BusImports:
       def __init__(self, dut): self.dut = dut
       async def write(self, addr, data):
           # await the DUT bus ...
           ...

   @cocotb.test()
   async def run_pss(dut):
       registry = load_pss(MODEL_TEXT)
       ep = registry.create(BusImports(dut), seed=1)
       await ep.Entry()

Ordered program
---------------

.. code-block:: python

   ep = registry.create()
   await ep.program(["Entry", "Reset", "Entry"]).run()

Ship a model (no re-parse)
--------------------------

Emit a self-contained module that embeds the serialized IR and rebuilds the
registry on import — skipping the PSS parse/frontend cost:

.. code-block:: python

   registry = load_pss(MODEL_TEXT, export_actions=["pss_top::Entry"])
   registry.emit_module("gen_model.py", module_doc="My PSS model")

Then, anywhere (no PSS source needed):

.. code-block:: python

   from gen_model import registry
   ep = registry.create(MyImports(), seed=1)
   await ep.Entry()

From a hand-built IR Context
----------------------------

.. code-block:: python

   import zuspec.ir.core as ir
   from zuspec.be.py import build_registry

   go = ir.DataTypeClass(name="Go", super=None,
       fields=[ir.Field(name="addr", datatype=ir.DataTypeInt(bits=8),
                        rand_kind=ir.RandKind.RAND)])
   top = ir.DataTypeComponent(name="Top", super=None)
   ctx = ir.Context(type_m={"Top": top, "Top::Go": go})

   registry = build_registry(ctx, export_actions=["Top::Go"])
   ep = registry.create(seed=1)
   await ep.Go()

.. Zuspec live-Python Backend documentation master file

Zuspec live-Python Backend
==========================

``zuspec-be-py`` is the **live-Python backend** for Zuspec — the Python analogue
of ``zuspec-be-sv``. It consumes a :class:`zuspec.ir.core.Context` and projects
it into executable Python classes built on the ``zuspec.dataclasses`` (zdc)
runtime, so a PSS model can be **loaded and driven directly from Python**.

On top of the class builder, the *export-api projection* runs a model as a live
Python object: build a registry, supply an import-API implementation, then
``await`` exported actions to run their traversals — mirroring the SystemVerilog
``oo_api`` projection.

Version: 0.0.1

**Quick Links:**

* :doc:`quickstart` — Get started in 5 minutes
* :doc:`concepts` — The registry / instance model and import wiring
* :doc:`api` — API Reference
* `GitHub Repository <https://github.com/zuspec/zuspec-be-py>`_

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   quickstart
   concepts
   examples

.. toctree::
   :maxdepth: 2
   :caption: Reference:

   api

Key Features
------------

* **IR → live classes**: turns a ``zuspec.ir.core.Context`` into runnable ``zdc``
  components, actions, structs, and enums — no source generation, all in memory.
* **Export-api projection**: ``registry.create(imports) -> ExportApi`` with one
  ``async`` method per exported action (``pre_solve`` → ``randomize`` →
  ``post_solve`` → ``activity``/``body``).
* **Import wiring**: a model's package-scope ``import target`` / ``import solve``
  calls route outward to a user-supplied object — sync *or* ``async`` (cocotb).
* **PSS-agnostic**: consumes the canonical IR plus an action→component
  ``owner_map``; any IR producer can drive it.
* **API-only**: consumed from a Python environment (standalone, pytest, cocotb).
  There is no CLI.

Getting Started
---------------

Install the package (pulled in transitively by ``pssc``):

.. code-block:: bash

   pip install zuspec-be-py

From PSS source, the easiest entry point is ``pssc.load_pss``, which returns a
``zuspec-be-py`` registry:

.. code-block:: python

   import asyncio
   from pssc import load_pss

   registry = load_pss(open("model.pss").read())   # parse + elaborate once
   ep = registry.create(seed=1)                     # a runnable instance
   asyncio.run(ep.Entry())                          # run the exported action

See :doc:`quickstart` for supplying imports and choosing exported actions.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Concepts
========

This page explains the model behind ``zuspec-be-py``: how a PSS model becomes a
reusable registry, how a registry becomes a runnable instance, and how the model
calls out to your code.

The two layers
--------------

There are two elaboration stages, and only one is per-run:

============================  ====================================  ==========
Stage                         Produces                              Reused?
============================  ====================================  ==========
Parse + translate to IR       ``zuspec.ir.core.Context``            once
Build runtime classes         ``ClassRegistry`` (the *registry*)    once
Structural elaboration        a live component tree + runner        per run
============================  ====================================  ==========

The first two stages are stateless and reusable — this is the **registry**. The
third stage is per-run: running an action mutates the component tree (pool
claims, state transitions, randomized fields), so every run needs its own tree.
That is what ``registry.create()`` produces: an :class:`~zuspec.be.py.ExportApi`.

.. code-block:: python

   registry = load_pss(text)          # stages 1-2: parse once, reusable
   a = registry.create(seed=1)        # stage 3: independent run A
   b = registry.create(seed=2)        # stage 3: independent run B

This mirrors the SystemVerilog factory exactly: the registry is
``pss_top::type_id()``, and ``create(imports)`` is ``factory.create(imports)``.

The registry is also a plain class container
(``registry["pss_top::Entry"]``, ``registry.pss_top``), so lower-level
"build a class and randomize it" usage is unchanged.

The export-api projection
-------------------------

``create()`` performs the per-run wiring:

1. instantiate a fresh root component tree,
2. build a seeded :class:`zuspec.dataclasses.rt.scenario_runner.ScenarioRunner`,
3. install an import resolver from the supplied imports,
4. expose one ``async`` method per exported action.

``await ep.<Action>()`` runs that action's lifecycle against the tree and returns
an :class:`~zuspec.be.py.ActionResult`.

Import wiring (the model calling out)
-------------------------------------

A PSS ``import target`` / ``import solve`` is a call *out* of the model — the
Python analogue of the SV ``import_api_if``. The
:class:`zuspec.dataclasses.rt.import_resolver.ImportResolver` binds each import
name to a method on the object you pass to ``create()`` and is active for the
duration of the run. The interpreter dispatches a model's ``self.<import>()``
call to it; an ``async`` target is awaited.

The PSS-agnostic contract
-------------------------

The builder consumes only the canonical IR — ``Context.type_m`` plus an
action→owning-component ``owner_map`` (derived from ``Comp::Action`` keys when
not supplied). It never imports ``pssc``; any IR producer can drive it. The PSS
frontend (``pssc.load_pss``) is one such producer, forwarding the PSS
``parent_comp_names`` as the ``owner_map``.

Performance
-----------

* **Bodies** that contain no imports compile to native Python (via the
  ``IRCompiler`` fast path); import-bearing or unsupported bodies fall back to
  the interpreter.
* **Constraint problems** are cached per type by the solver backend, so repeated
  ``randomize()`` on the same action re-solves cheaply across runs.
* **Shipping a model:** ``registry.emit_module(path)`` writes a self-contained
  ``.py`` that embeds the serialized IR and rebuilds the registry on import — so
  a model can be distributed and driven without re-parsing the PSS source.

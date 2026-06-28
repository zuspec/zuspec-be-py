API Reference
=============

The public surface is exported from the :mod:`zuspec.be.py` package.

Entry points
------------

.. autofunction:: zuspec.be.py.build_registry

.. autofunction:: zuspec.be.py.build_runtime

The registry
------------

.. autoclass:: zuspec.be.py.ClassRegistry
   :members: create, emit_module, configure_exports, export_actions, import_specs,
             owner_map, action_qnames, root_component_name, ImportApi,
             get, keys, values, items

The export-api projection
-------------------------

.. autoclass:: zuspec.be.py.ExportApi
   :members: actions, runner, program

.. autoclass:: zuspec.be.py.ActionResult

.. autoclass:: zuspec.be.py.ActionRunner
   :members: run

.. autoclass:: zuspec.be.py.ActionProgram
   :members: run

.. autofunction:: zuspec.be.py.build_import_protocol

The builder
-----------

.. autoclass:: zuspec.be.py.IrToRuntimeBuilder
   :members: build

Import wiring
-------------

Re-exported from the ``zuspec.dataclasses`` runtime:

.. autoclass:: zuspec.be.py.ImportSpec

.. autoclass:: zuspec.be.py.ImportResolver
   :members: has, call, call_async, specs

.. autoexception:: zuspec.be.py.PssImportError

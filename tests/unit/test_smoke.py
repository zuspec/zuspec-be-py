"""Smoke tests: the package imports and is wired into the namespace correctly."""


def test_package_imports():
    import zuspec.be.py as bepy

    assert bepy.__version__


def test_namespace_siblings_coexist():
    # zuspec.be is a PEP 420 namespace package shared with the other backends;
    # importing zuspec.be.py must not shadow the shared runtime / IR packages.
    import zuspec.be.py  # noqa: F401
    import zuspec.ir.core  # noqa: F401
    import zuspec.dataclasses  # noqa: F401

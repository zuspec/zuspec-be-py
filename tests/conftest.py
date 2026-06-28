"""Shared test configuration for zuspec-be-py.

No solver backend is pinned: the tests run against the default backend
(native dv-solve when available, else the pure-Python solver), exercising the
out-of-the-box experience.
"""

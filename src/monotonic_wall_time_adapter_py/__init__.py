"""Monotonic Wall Time Adapter.

A single clock function returning a monotonic float with a stable epoch.
"""

from monotonic_wall_time_adapter_py.core import clock, reset, get_epoch_offset

__all__ = ["clock", "reset", "get_epoch_offset"]

# monotonic-wall-time-adapter-py

A single `clock()` function returning a monotonic float in seconds relative to a stable, process-local epoch, hiding the difference between `time.monotonic` and `time.perf_counter`.

## Usage

```python
from monotonic_wall_time_adapter_py import clock

start = clock()
# ... do work ...
elapsed = clock() - start
print(f"elapsed: {elapsed:.6f}s")
```

The first call to `clock()` establishes the epoch (the raw value of the underlying monotonic source at that instant). Every subsequent call returns `source_value - epoch`, so results are always non-negative and monotonically increasing.

## Why

Python provides two monotonic clocks — `time.monotonic` and `time.perf_counter` — with subtly different resolutions and platform availability but the same guarantee (never goes backwards). Choosing between them in library code is a minor but repeated annoyance. This library picks one (`perf_counter`, falling back to `monotonic`), caches the epoch on first use, and presents a single zero-based float API.

The trade-off: the epoch is process-local and established lazily, so the first reported value is approximately zero rather than a meaningful absolute time. This is deliberate — the library is for measuring intervals, not timestamps.

## Edge cases

- The first call to `clock()` returns a value very close to, but not exactly, zero, because the underlying source is read twice (once to cache the epoch, once to produce the result). The gap is one function call, well under a millisecond.
- `reset()` is provided for testing. Calling it in production code will cause the next `clock()` call to establish a new epoch, breaking comparability with earlier values.

## Exports

- `clock()` — returns a monotonic `float` in seconds relative to the stable epoch.
- `get_epoch_offset()` — returns the cached raw epoch offset (`float`), or `None` if `clock()` has not been called yet.
- `reset()` — clears the cached epoch; intended for tests only.

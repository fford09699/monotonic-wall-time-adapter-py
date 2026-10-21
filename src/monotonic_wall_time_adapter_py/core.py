import threading
import time

# Module-level state for the stable epoch offset.
# This is set on the first call to clock() and never changes afterwards.
_epoch_offset = None
_lock = threading.Lock()


def _resolve_epoch():
    """Determine and cache the epoch offset on first call.

    We pick whichever underlying monotonic source is available, preferring
    perf_counter (higher resolution on most platforms) and falling back to
    monotonic. The offset is the value of that source at the moment of the
    first call, so that all subsequent clock() results are relative to a
    stable, process-local epoch.  We guard the resolution with a lock so
    that two concurrent first-calls do not race into computing two different
    offsets.
    """
    global _epoch_offset
    with _lock:
        if _epoch_offset is None:
            source = getattr(time, "perf_counter", None)
            if source is None:
                source = time.monotonic
            _epoch_offset = float(source())
    return _epoch_offset


def clock():
    """Return a monotonic float in seconds relative to a stable epoch.

    The epoch is established on the first call and never changes for the
    lifetime of the process.  Internally we use perf_counter where available
    (falling back to monotonic) because perf_counter has higher resolution on
    most platforms and is itself guaranteed monotonic.
    """
    offset = _epoch_offset if _epoch_offset is not None else _resolve_epoch()
    source = getattr(time, "perf_counter", None)
    if source is None:
        source = time.monotonic
    return float(source()) - offset


def get_epoch_offset():
    """Return the cached epoch offset, or None if clock() has not been called.

    Useful for tests and diagnostics; not normally needed by application code.
    """
    return _epoch_offset


def reset():
    """Clear the cached epoch offset.

    Intended for testing only.  After reset(), the next call to clock()
    will establish a new epoch.
    """
    global _epoch_offset
    with _lock:
        _epoch_offset = None

import unittest

from monotonic_wall_time_adapter_py import core


class TestClock(unittest.TestCase):

    def setUp(self):
        core.reset()

    def test_returns_float(self):
        result = core.clock()
        self.assertIsInstance(result, float)

    def test_first_call_is_zero(self):
        """The first call establishes the epoch, so its result should be ~0.

        We cannot assert exact equality because the underlying source value is
        read twice (once for offset, once for the result).  The difference is
        at most one function-call interval, which we assert is small.
        """
        result = core.clock()
        self.assertGreaterEqual(result, 0.0)
        self.assertLess(result, 1.0)

    def test_monotonic_increasing(self):
        first = core.clock()
        second = core.clock()
        third = core.clock()
        self.assertGreater(second, first)
        self.assertGreater(third, second)

    def test_epoch_stable_across_calls(self):
        core.clock()
        offset1 = core.get_epoch_offset()
        core.clock()
        core.clock()
        offset2 = core.get_epoch_offset()
        self.assertEqual(offset1, offset2)

    def test_epoch_offset_none_before_first_call(self):
        self.assertIsNone(core.get_epoch_offset())

    def test_reset_clears_epoch(self):
        core.clock()
        self.assertIsNotNone(core.get_epoch_offset())
        core.reset()
        self.assertIsNone(core.get_epoch_offset())

    def test_reset_establishes_new_epoch(self):
        core.clock()
        offset1 = core.get_epoch_offset()
        core.reset()
        core.clock()
        offset2 = core.get_epoch_offset()
        self.assertNotEqual(offset1, offset2)


if __name__ == "__main__":
    unittest.main()

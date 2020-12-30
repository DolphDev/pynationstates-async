import unittest

import nationstates_async as core


class ShardTest(unittest.TestCase):

    def test_shard(self):
        self.assertEqual(
            core.Shard("numnations")._get_main_value(),
            "numnations")

    def test_shard_tail_gen(self):
        self.assertEqual(core.Shard("dispatch", dispatchid="1").tail_gen(), {"dispatchid":"1"})

    def test_shard_repr(self):
        self.assertIsInstance(core.Shard("test").__repr__(), str)
        self.assertIsInstance(core.Shard("test", test="test").__repr__(), str)

    def test_shard_ShardError(self):
        self.assertRaises(ValueError, core.Shard, None)

    def test_shard_string(self):
        try:
            str(core.Shard("TEST"))
            core.Shard("TEST").name
        except:
            self.fail()

    def test_shard_eq(self):
        self.assertEqual(core.Shard("TEST"), core.Shard("TEST"))
    
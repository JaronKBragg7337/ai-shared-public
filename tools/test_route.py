"""Focused route selection tests with fake usage meters."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import route


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.unknown = {k: route.unknown("test") for k in ("codex", "reserve", "claude", "grok")}
        self.unknown["deepseek"] = route.unknown("test")

    def test_role_order_and_kind_guess(self):
        self.assertEqual(route.route("make a character asset", fake_meters=self.unknown), "claude-sonnet")
        self.assertEqual(route.route("build multiplayer economy", fake_meters=self.unknown), "codex-sol")
        self.assertEqual(route.route("publish docs", fake_meters=self.unknown), "codex-luna")
        self.assertEqual(route.route("research this", fake_meters=self.unknown), "grok-build")
        self.assertEqual(route.route("decide how to proceed", fake_meters=self.unknown), "claude-opus")

    def test_full_meter_skips_to_next(self):
        meters = dict(self.unknown)
        meters["claude"] = {"used_pct_5h": 90, "used_pct_week": 1}
        self.assertEqual(route.route("visual character", fake_meters=meters), "codex-sol")

    def test_weekly_threshold_skips(self):
        meters = dict(self.unknown)
        meters["codex"] = {"used_pct_5h": 2, "used_pct_week": 91}
        self.assertEqual(route.route("publish docs", fake_meters=meters), "grok-fast")

    def test_unknown_meter_is_reported_but_not_blocked(self):
        self.assertEqual(route.route("publish docs", fake_meters=self.unknown), "codex-luna")

    def test_trading_is_never_routed(self):
        with self.assertRaisesRegex(RuntimeError, "never routed"):
            route.route("review this Polymarket trade", fake_meters=self.unknown)


if __name__ == "__main__":
    unittest.main()

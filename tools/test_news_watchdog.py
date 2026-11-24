import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

import news_watchdog as watchdog


DATE = "2026-10-27"


class Response(io.BytesIO):
    status = 200
    headers = {"Content-Length": "1234"}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def index(episodes):
    return Response(json.dumps({"episodes": episodes}).encode())


class NewsWatchdogTests(unittest.TestCase):
    def test_live_index_and_video(self):
        episode = {"date": DATE, "video": f"{watchdog.BASE}/{DATE}.mp4"}
        with patch.object(watchdog.urllib.request, "urlopen", side_effect=[index([episode]), Response()]):
            self.assertEqual(watchdog.check(DATE)[0], "published")

    def test_missing_index_entry_and_missing_video(self):
        with patch.object(watchdog.urllib.request, "urlopen", return_value=index([])):
            self.assertEqual(watchdog.check(DATE)[0], "missing")
        episode = {"date": DATE, "video": f"{watchdog.BASE}/{DATE}.mp4"}
        missing = HTTPError("https://example.com", 404, "missing", {}, None)
        with patch.object(watchdog.urllib.request, "urlopen", side_effect=[index([episode]), missing]):
            self.assertEqual(watchdog.check(DATE)[0], "missing")

    def test_connection_failure_or_bad_index_is_not_missing(self):
        with patch.object(watchdog.urllib.request, "urlopen", side_effect=URLError("offline")):
            self.assertEqual(watchdog.check(DATE)[0], "unreachable")
        with patch.object(watchdog.urllib.request, "urlopen", return_value=Response(b"not json")):
            self.assertEqual(watchdog.check(DATE)[0], "unreachable")

    def test_failed_send_retries_success_is_remembered(self):
        with tempfile.TemporaryDirectory() as folder:
            state = Path(folder) / "alerts.json"
            with patch.object(watchdog, "check", return_value=("missing", "missing")), \
                 patch.object(watchdog, "send_alert", side_effect=[OSError("private topic"), None]) as send:
                self.assertEqual(watchdog.run(DATE, state_path=state), 2)
                self.assertFalse(state.exists())
                self.assertEqual(watchdog.run(DATE, state_path=state), 1)
                self.assertEqual(watchdog.run(DATE, state_path=state), 1)
                self.assertEqual(send.call_count, 2)

    def test_dry_run_does_not_send_or_save(self):
        with tempfile.TemporaryDirectory() as folder:
            state = Path(folder) / "alerts.json"
            with patch.object(watchdog, "check", return_value=("unreachable", "offline")), \
                 patch.object(watchdog, "send_alert") as send:
                self.assertEqual(watchdog.run(DATE, dry_run=True, state_path=state), 1)
                send.assert_not_called()
                self.assertFalse(state.exists())


if __name__ == "__main__":
    unittest.main()

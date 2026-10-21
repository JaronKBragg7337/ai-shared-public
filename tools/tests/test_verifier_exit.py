"""Fault injection: scheduler must see failures; no network or queue writes."""
import io
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verifier


class VerifierExitTests(unittest.TestCase):
    def invoke(self, failure=None):
        with patch.object(sys, 'argv', ['verifier.py']), \
             patch.object(verifier, 'secrets', return_value={'SUPABASE_URL': 'test', 'SUPABASE_SERVICE_ROLE_KEY': 'test'}), \
             patch.object(verifier, 'log'), \
             patch.object(verifier, 'run_once', side_effect=failure):
            verifier.main()

    def test_success_returns_normally(self):
        self.invoke()

    def test_runtime_failure_is_nonzero(self):
        with self.assertRaises(SystemExit) as result:
            self.invoke(RuntimeError('injected unavailable service'))
        self.assertEqual(result.exception.code, 1)

    def test_http_failure_is_nonzero(self):
        error = urllib.error.HTTPError('https://invalid.test', 503, 'unavailable', {}, io.BytesIO(b'test'))
        with self.assertRaises(SystemExit) as result:
            self.invoke(error)
        self.assertEqual(result.exception.code, 1)


if __name__ == '__main__':
    unittest.main()

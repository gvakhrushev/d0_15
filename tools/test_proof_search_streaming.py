"""Bounded subprocess retrieval regressions."""
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from tools import proof_architecture as proof


class StreamingTextTests(unittest.TestCase):
    def test_reads_stdout_with_large_stderr_without_deadlock(self):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, '-c',
                       'import sys; sys.stderr.write("e" * 200000); '
                       'sys.stderr.flush(); print("first"); print("second")']
            self.assertEqual(list(proof._rg_text_lines(command, pathlib.Path(directory))),
                             ['first\n', 'second\n'])

    def test_reports_non_success_with_original_stderr(self):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, '-c',
                       'import sys; print("error detail", file=sys.stderr); sys.exit(2)']
            with self.assertRaisesRegex(RuntimeError, r'rg text search failed \(2\): error detail'):
                list(proof._rg_text_lines(command, pathlib.Path(directory)))

    def test_batched_search_matches_previous_capture_implementation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            research = root / "02_REGISTRY" / "research"
            research.mkdir(parents=True)
            (research / "alpha.md").write_text("Blue green.\nRed green.\n", encoding="utf-8")
            (research / "blue.md").write_text("Red yellow.\n", encoding="utf-8")
            queries = ["blue green", "red yellow", "no-such-token"]
            actual = proof.full_text_search_many(root, queries)

            def legacy(command, cwd):
                result = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                                        encoding="utf-8", errors="replace")
                if result.returncode not in (0, 1):
                    raise RuntimeError(f"rg text search failed ({result.returncode}): {result.stderr}")
                return iter(result.stdout.splitlines())

            with mock.patch.object(proof, "_rg_text_lines", legacy):
                expected = proof.full_text_search_many(root, queries)
            self.assertEqual(actual, expected)

    def test_ripgrep_no_matches_is_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, '-c', 'import sys; sys.exit(1)']
            self.assertEqual(list(proof._rg_text_lines(command, pathlib.Path(directory))), [])


if __name__ == '__main__':
    unittest.main()

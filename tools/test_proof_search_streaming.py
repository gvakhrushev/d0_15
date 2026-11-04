"""Bounded subprocess retrieval regressions."""
import pathlib
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from unittest import mock

from tools import proof_architecture as proof


# Small subprocess fixture for the two ripgrep operations used by these tests.
# It searches the actual temporary files and emits rg's JSON match-line shape;
# the production streaming and legacy capture paths both run real subprocesses.
_FIXTURE_RG = r'''
import json
import pathlib
import sys

args = sys.argv[1:]
terms, globs, roots = [], [], []
i = 0
while i < len(args):
    arg = args[i]
    if arg in ('-e', '-g'):
        (terms if arg == '-e' else globs).append(args[i + 1])
        i += 2
    else:
        if not arg.startswith('-'):
            roots.append(arg)
        i += 1
paths = sorted(p for root in roots for p in pathlib.Path(root).rglob('*')
               if p.is_file() and any(p.match(g) for g in globs))
found = False
for path in paths:
    if '--files' in args:
        print(path.as_posix())
        found = True
        continue
    for line in path.read_text(encoding='utf-8').splitlines(keepends=True):
        if any(term.lower() in line.lower() for term in terms):
            print(json.dumps({'type': 'match', 'data': {
                'path': {'text': path.as_posix()}, 'lines': {'text': line}}}))
            found = True
sys.exit(0 if found else 1)
'''


@contextmanager
def fixture_rg():
    popen = subprocess.Popen

    def run_fixture(command, *args, **kwargs):
        if isinstance(command, (list, tuple)) and command and command[0] == 'rg':
            command = [sys.executable, '-c', _FIXTURE_RG, *command[1:]]
        return popen(command, *args, **kwargs)

    with mock.patch.object(subprocess, 'Popen', side_effect=run_fixture):
        yield


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
            def legacy(command, cwd):
                result = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                                        encoding="utf-8", errors="replace")
                if result.returncode not in (0, 1):
                    raise RuntimeError(f"rg text search failed ({result.returncode}): {result.stderr}")
                return iter(result.stdout.splitlines())

            with fixture_rg():
                actual = proof.full_text_search_many(root, queries)
                with mock.patch.object(proof, "_rg_text_lines", legacy):
                    expected = proof.full_text_search_many(root, queries)
            self.assertEqual(actual, expected)
            self.assertEqual(actual[0][0]['source'], '02_REGISTRY/research/alpha.md')
            self.assertEqual(actual[1][0]['source'], '02_REGISTRY/research/blue.md')
            self.assertEqual(actual[2], [])

    def test_ripgrep_no_matches_is_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, '-c', 'import sys; sys.exit(1)']
            self.assertEqual(list(proof._rg_text_lines(command, pathlib.Path(directory))), [])


if __name__ == '__main__':
    unittest.main()

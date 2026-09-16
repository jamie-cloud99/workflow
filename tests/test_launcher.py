import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LauncherTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='workflow launcher 中文 ')
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.bin = self.directory / 'bin'
        self.bin.mkdir()
        self.env = dict(os.environ, PATH=str(self.bin))
        self.env.pop('WORKFLOW_PYTHON', None)
        self.target = self.directory / 'new home'

    def interpreter(self, name, supported):
        path = self.bin / name
        # Real Python executes the CLI; only the interpreter-version probe is
        # simulated, so tests run independently of the host's default version.
        import shlex
        path.write_text('#!/bin/sh\n'
                        'if [ "$1" = "-c" ]; then exit ' + ('0' if supported else '1') + '; fi\n'
                        'exec ' + shlex.quote(sys.executable) + ' "$@"\n')
        path.chmod(0o755)
        return path

    def launch(self):
        return subprocess.run([str(ROOT / 'workflow'), 'plan', '--local-only', '--target', str(self.target)],
                              cwd=self.directory, env=self.env, text=True, capture_output=True)

    def test_uses_supported_python3_and_preserves_arguments_from_other_cwd(self):
        self.interpreter('python3', True)
        result = self.launch()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('.codex/AGENTS.md', result.stdout)
        self.assertFalse(self.target.exists())

    def test_skips_old_python3_and_finds_newer_version_without_hardcoded_minor(self):
        self.interpreter('python3', False)
        self.interpreter('python3.19', True)
        result = self.launch()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_explicit_interpreter_path_can_contain_spaces(self):
        self.env['WORKFLOW_PYTHON'] = str(self.interpreter('my python', True))
        result = self.launch()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unsupported_override_explains_installation_without_writing(self):
        self.env['WORKFLOW_PYTHON'] = str(self.interpreter('old-python', False))
        result = self.launch()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Python 3.11+', result.stderr)
        self.assertIn('brew install python', result.stderr)
        self.assertFalse(self.target.exists())


if __name__ == '__main__':
    unittest.main()

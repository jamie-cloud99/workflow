import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/macos/preview-markdown.sh"


class PreviewTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="markdown preview ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.record = self.root / "args.json"
        fake = self.root / "glow"
        fake.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, sys\n"
            "from pathlib import Path\n"
            "Path(os.environ['PREVIEW_TEST_RECORD']).write_text("
            "json.dumps({'args': sys.argv[1:], 'pager': os.environ.get('PAGER')}))\n"
        )
        fake.chmod(0o755)
        self.env = dict(os.environ, PATH=f"{self.root}:{os.environ['PATH']}",
                        PREVIEW_TEST_RECORD=str(self.record))

    def run_preview(self, *args):
        return subprocess.run(["/bin/bash", str(SCRIPT), *map(str, args)],
                              env=self.env, text=True, capture_output=True)

    def test_unicode_spaces_and_shell_characters_are_literal(self):
        path = self.root / "中文 規劃 ' $(touch INJECTED) `id`.md"
        path.write_text("# 中文\n\n- item\n")
        result = self.run_preview(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(self.record.read_text())
        self.assertEqual(data['args'][-2:], ['--', str(path)])
        self.assertIn('-p', data['args'])
        self.assertEqual(data['pager'], '/usr/bin/less -R')
        self.assertFalse((self.root / 'INJECTED').exists())

    def test_missing_file_does_not_launch_reader(self):
        result = self.run_preview(self.root / 'missing.md')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('readable Markdown file', result.stderr)
        self.assertFalse(self.record.exists())

    def test_directory_does_not_launch_reader(self):
        result = self.run_preview(self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('readable Markdown file', result.stderr)
        self.assertFalse(self.record.exists())

    def test_executable_file_is_not_treated_as_markdown(self):
        path = self.root / 'danger.command'
        path.write_text('exit 99\n')
        result = self.run_preview(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('readable Markdown file', result.stderr)
        self.assertFalse(self.record.exists())


if __name__ == '__main__':
    unittest.main()

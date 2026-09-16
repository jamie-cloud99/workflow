import importlib.util
from pathlib import Path
import tempfile
import plistlib
import subprocess
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    'installer', Path(__file__).resolve().parents[1] / 'scripts/macos/install-markdown-preview.py')
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class DefaultsTest(unittest.TestCase):
    def test_bundled_reader_runs_when_source_has_no_execute_permission(self):
        with tempfile.TemporaryDirectory(prefix='preview bundle ') as temp:
            root = Path(temp)
            source = root / 'scripts/macos/preview-markdown.sh'
            source.parent.mkdir(parents=True)
            source.write_text('#!/bin/sh\nprintf "%s\\n" "$1"\n')
            source.chmod(0o644)
            app = root / 'Markdown Preview.app'

            def native_tool(*args):
                if args[0] == '/usr/bin/osacompile':
                    (app / 'Contents/Resources').mkdir(parents=True)
                    (app / 'Contents/Info.plist').write_bytes(plistlib.dumps({}))

            with patch.object(installer, 'ROOT', root), patch.object(installer, 'run', side_effect=native_tool):
                installer.build_app(app)
            reader = app / 'Contents/Resources/preview-markdown.sh'
            result = subprocess.run([str(reader), '中文 design.md'], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), '中文 design.md')

    def test_launch_services_can_return_a_stale_default_after_successful_write(self):
        with patch.object(installer, 'default_app', side_effect=['previous.app', installer.BUNDLE_ID]):
            with patch('time.sleep'):
                self.assertIsNone(installer.verify_default('duti', 'md', installer.BUNDLE_ID))

    def test_persistent_wrong_default_is_not_reported_as_success(self):
        with patch.object(installer, 'default_app', return_value='previous.app'):
            with patch('time.sleep'):
                with self.assertRaisesRegex(RuntimeError, 'verification failed'):
                    installer.verify_default('duti', 'md', installer.BUNDLE_ID)

    def test_reinstallation_preserves_original_backup(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp)
            original = '{"md": "original.app", "markdown": "original.app"}\n'
            (state / 'defaults-before.json').write_text(original)
            with patch.object(installer, 'default_app') as query:
                installer.save_defaults('duti', state)
                query.assert_not_called()
            self.assertEqual((state / 'defaults-before.json').read_text(), original)


if __name__ == '__main__':
    unittest.main()

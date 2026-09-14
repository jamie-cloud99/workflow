import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    'installer', Path(__file__).resolve().parents[1] / 'scripts/macos/install-markdown-preview.py')
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class DefaultsTest(unittest.TestCase):
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

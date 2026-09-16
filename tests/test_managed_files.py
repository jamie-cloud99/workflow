import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('managed', Path(__file__).resolve().parents[1] / 'scripts/managed_files.py')


class ManagedFilesTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='workflow 中文 ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'new home'
        self.state = Path(self.temp.name) / 'state'
        self.module = importlib.util.module_from_spec(SPEC)
        SPEC.loader.exec_module(self.module)
        self.manager = self.module.ManagedFiles(self.root, self.state)
        self.files = {'.codex/AGENTS.md': b'new rules\n', '.config/example': b'config\n'}

    def test_plan_does_not_create_home_or_state(self):
        rows = self.manager.plan(self.files)
        self.assertTrue(all(row['status'] == 'create' for row in rows))
        self.assertFalse(self.root.exists())
        self.assertFalse(self.state.exists())

    def test_conflict_preflight_writes_nothing(self):
        path = self.root / '.codex/AGENTS.md'
        path.parent.mkdir(parents=True)
        path.write_bytes(b'mine')
        with self.assertRaisesRegex(RuntimeError, 'conflict'):
            self.manager.apply(self.files)
        self.assertEqual(path.read_bytes(), b'mine')
        self.assertFalse((self.root / '.config/example').exists())

    def test_repeat_apply_and_restore_preserve_original(self):
        original = self.root / '.codex/AGENTS.md'
        original.parent.mkdir(parents=True)
        original.write_bytes(b'mine')
        original.chmod(0o640)
        self.manager.apply(self.files, replace=True)
        self.manager.apply(self.files)
        self.manager.restore()
        self.assertEqual(original.read_bytes(), b'mine')
        self.assertEqual(original.stat().st_mode & 0o777, 0o640)
        self.assertFalse((self.root / '.config/example').exists())

    def test_edited_managed_file_is_not_replaced_or_removed(self):
        self.manager.apply(self.files)
        path = self.root / '.codex/AGENTS.md'
        path.write_bytes(b'user edits')
        with self.assertRaisesRegex(RuntimeError, 'conflict'):
            self.manager.apply(self.files)
        with self.assertRaisesRegex(RuntimeError, 'conflict'):
            self.manager.restore()
        self.assertEqual(path.read_bytes(), b'user edits')
        self.assertTrue((self.root / '.config/example').exists())

    def test_parent_symlink_never_escapes_target(self):
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        self.root.mkdir()
        (self.root / '.codex').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, 'symlink'):
            self.manager.apply(self.files, replace=True)
        self.assertFalse((outside / 'AGENTS.md').exists())

    def test_existing_leaf_symlink_can_be_backed_up_and_restored(self):
        external = Path(self.temp.name) / 'rules'
        external.write_bytes(b'outside')
        path = self.root / '.codex/AGENTS.md'
        path.parent.mkdir(parents=True)
        path.symlink_to(external)
        self.manager.apply(self.files, replace=True)
        self.manager.restore()
        self.assertTrue(path.is_symlink())
        self.assertTrue(path.samefile(external))
        self.assertEqual(external.read_bytes(), b'outside')

    def test_preexisting_identical_file_is_not_removed_by_restore(self):
        path = self.root / '.codex/AGENTS.md'
        path.parent.mkdir(parents=True)
        path.write_bytes(self.files['.codex/AGENTS.md'])
        self.manager.apply(self.files)
        self.manager.restore()
        self.assertEqual(path.read_bytes(), self.files['.codex/AGENTS.md'])

    def test_restore_rejects_tampered_journal_path(self):
        self.manager.apply(self.files)
        import json
        journal = self.state / 'journal.json'
        data = json.loads(journal.read_text())
        data['files']['../outside'] = data['files']['.codex/AGENTS.md']
        journal.write_text(json.dumps(data))
        with self.assertRaisesRegex(RuntimeError, 'path'):
            self.manager.restore()

    def test_replacing_later_edits_keeps_a_backup_history(self):
        self.manager.apply(self.files)
        path = self.root / '.codex/AGENTS.md'
        path.write_bytes(b'later user edit')
        self.manager.apply(self.files, replace=True)
        import json, base64
        record = json.loads((self.state / 'journal.json').read_text())['files']['.codex/AGENTS.md']
        self.assertIn(b'later user edit', [base64.b64decode(x['data']) for x in record['history'] if x['kind'] == 'file'])

    def test_concurrent_operation_is_rejected(self):
        with self.manager.lock():
            with self.assertRaisesRegex(RuntimeError, 'lock'):
                self.manager.apply(self.files)

    def test_write_failure_is_recoverable(self):
        from unittest.mock import patch
        original = self.module.write_snapshot
        def fail_config(path, value):
            if str(path).endswith('.config/example'):
                raise OSError('disk write failed')
            original(path, value)
        with patch.object(self.module, 'write_snapshot', side_effect=fail_config):
            with self.assertRaises(OSError):
                self.manager.apply(self.files)
        self.manager.restore()
        self.assertFalse((self.root / '.codex/AGENTS.md').exists())


if __name__ == '__main__':
    unittest.main()

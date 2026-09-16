import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location('workflow_cli', SCRIPTS / 'workflow.py')
workflow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workflow)


class MigrationTest(unittest.TestCase):
    def test_interrupted_retirement_is_completed_by_retry(self):
        for deletion_completed in (False, True):
            with self.subTest(deletion_completed=deletion_completed):
                self.check_interrupted_retirement(deletion_completed)

    def check_interrupted_retirement(self, deletion_completed):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp).resolve() / 'home'
            state = Path(temp).resolve() / 'state'
            manager = workflow.ManagedFiles(target, state)
            name = '.agents/skills/ito-search'
            manager.apply({name: {'link': '/old/ito-search'}})
            with patch.object(workflow, 'selected_paths', return_value=({}, [])):
                files, _ = workflow.render(target, state)
            module = sys.modules[workflow.ManagedFiles.__module__]
            write = module.write_snapshot

            def interrupted(path, value):
                if path == target / name:
                    if deletion_completed:
                        write(path, value)
                    raise OSError('interrupted during retirement')
                write(path, value)

            with patch.object(module, 'write_snapshot', side_effect=interrupted):
                with self.assertRaises(OSError):
                    manager.apply(files)
            with patch.object(workflow, 'selected_paths', return_value=({}, [])):
                retry, _ = workflow.render(target, state)
            self.assertTrue(name in retry, 'Interrupted retirement must remain in the next plan.')
            manager.apply(retry)
            self.assertFalse((target / name).is_symlink())
            self.assertNotIn('pending', manager.load()['files'][name])

    def test_only_managed_retired_links_are_removed_on_apply(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp).resolve() / 'home'
            state = Path(temp).resolve() / 'state'
            manager = workflow.ManagedFiles(target, state)
            managed = '.agents/skills/ito-search'
            retained = '.agents/skills/react-best-practices'
            manager.apply({managed: {'link': '/old/ito-search'}, retained: {'link': '/old/react'}})
            user_link = target / '.claude/skills/ito-search'
            user_link.parent.mkdir(parents=True)
            user_link.symlink_to('/user/ito-search')
            with patch.object(workflow, 'selected_paths', return_value=({}, [])):
                files, missing = workflow.render(target, state)
            self.assertEqual(missing, [])
            self.assertIsNone(files[managed])
            self.assertNotIn('.claude/skills/ito-search', files)
            manager.apply(files)
            self.assertFalse((target / managed).is_symlink())
            self.assertEqual(os.readlink(user_link), '/user/ito-search')
            self.assertEqual(os.readlink(target / retained), '/old/react')
            offline, _ = workflow.render(target, state, local_only=True)
            self.assertNotIn(managed, offline)

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('sources', Path(__file__).resolve().parents[1] / 'scripts/skill_sources.py')
sources = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sources)


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.origin = self.root / 'origin'
        self.origin.mkdir()
        self.cache = self.root / 'cache'
        self.manifest = {'sources': [{'repository': 'owner/repo', 'skills': [
            {'name': 'example', 'path': 'skills/example'}]}]}
        self.git('init', '-q')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.invalid')
        self.commit('first')
        self.url_patch = patch.object(sources, 'source_url', return_value=str(self.origin))
        self.url_patch.start()
        self.addCleanup(self.url_patch.stop)

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.origin), *args], check=True,
                              text=True, capture_output=True).stdout.strip()

    def commit(self, text):
        file = self.origin / 'skills/example/SKILL.md'
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text)
        self.git('add', '.')
        self.git('commit', '-qm', text)

    def test_sync_follows_new_upstream_commit_without_changing_catalog(self):
        before = json.dumps(self.manifest)
        sources.sync_sources(self.manifest, self.cache)
        first = sources.selected_paths(self.manifest, self.cache)[0]['example']
        self.assertEqual((first / 'SKILL.md').read_text(), 'first')
        self.commit('second')
        sources.sync_sources(self.manifest, self.cache)
        second = sources.selected_paths(self.manifest, self.cache)[0]['example']
        self.assertNotEqual(first, second)
        self.assertEqual((second / 'SKILL.md').read_text(), 'second')
        self.assertEqual((first / 'SKILL.md').read_text(), 'first')
        self.assertEqual(json.dumps(self.manifest), before)

    def test_failed_refresh_keeps_previous_complete_snapshot(self):
        sources.sync_sources(self.manifest, self.cache)
        state = (self.cache / 'resolved.json').read_bytes()
        with patch.object(sources, 'git', side_effect=RuntimeError('network unavailable')):
            with self.assertRaises(RuntimeError):
                sources.sync_sources(self.manifest, self.cache)
        self.assertEqual((self.cache / 'resolved.json').read_bytes(), state)
        self.assertFalse(sources.selected_paths(self.manifest, self.cache)[1])

    def test_adding_selection_at_same_head_builds_complete_new_checkout(self):
        second = self.origin / 'skills/second/SKILL.md'
        second.parent.mkdir(parents=True)
        second.write_text('second skill')
        self.git('add', '.')
        self.git('commit', '-qm', 'both skills exist upstream')
        sources.sync_sources(self.manifest, self.cache)
        previous = sources.selected_paths(self.manifest, self.cache)[0]['example']
        self.manifest['sources'][0]['skills'].append({'name': 'second', 'path': 'skills/second'})
        sources.sync_sources(self.manifest, self.cache)
        selected, missing = sources.selected_paths(self.manifest, self.cache)
        self.assertEqual(missing, [])
        self.assertEqual((selected['second'] / 'SKILL.md').read_text(), 'second skill')
        self.assertTrue((previous / 'SKILL.md').exists())

    def test_local_edits_are_not_silently_adopted_or_overwritten(self):
        sources.sync_sources(self.manifest, self.cache)
        path = sources.selected_paths(self.manifest, self.cache)[0]['example']
        (path / 'SKILL.md').write_text('local edit')
        with self.assertRaisesRegex(RuntimeError, 'checksum'):
            sources.selected_paths(self.manifest, self.cache)
        with self.assertRaisesRegex(RuntimeError, 'local edits'):
            sources.sync_sources(self.manifest, self.cache)
        self.assertEqual((path / 'SKILL.md').read_text(), 'local edit')

    def test_symbolic_links_in_downloaded_skill_are_rejected(self):
        path = self.root / 'skill'
        path.mkdir()
        (path / 'secret-link').symlink_to('/etc/hosts')
        with self.assertRaisesRegex(RuntimeError, 'symlink'):
            sources.tree_hash(path)

    def test_pinned_revision_and_path_traversal_are_rejected(self):
        with self.assertRaises(RuntimeError):
            sources.validate({'sources': [dict(self.manifest['sources'][0], revision='a' * 40)]})
        self.manifest['sources'][0]['skills'][0]['path'] = '../outside'
        with self.assertRaises(RuntimeError):
            sources.validate(self.manifest)

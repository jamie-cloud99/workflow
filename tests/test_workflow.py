import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'scripts/workflow.py'


class WorkflowTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='workflow 中文 space ')
        self.addCleanup(self.temp.cleanup)
        self.target = (Path(self.temp.name) / 'home').resolve()

    def command(self, command, *args):
        return subprocess.run([sys.executable, str(CLI), command, '--target', str(self.target),
                               '--local-only', *args], capture_output=True, text=True)

    def test_plan_then_apply_twice_and_restore(self):
        result = self.command('plan')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.target.exists())
        for _ in range(2):
            result = self.command('apply')
            self.assertEqual(result.returncode, 0, result.stderr)
        import tomllib
        config = tomllib.loads((self.target / '.codex/config.toml').read_text())
        self.assertEqual(config['mcp_servers']['gitnexus']['command'], str(self.target / '.volta/bin/gitnexus'))
        self.assertTrue((self.target / '.agents/skills/workflow-delivery/SKILL.md').exists())
        self.assertTrue((self.target / '.claude/skills/workflow-delivery/SKILL.md').exists())
        self.assertEqual((self.target / '.zshrc').read_text().count('# workflow:start'), 1)
        git_config = subprocess.run(['git', 'config', '--file', str(self.target / '.gitconfig'),
                                     '--includes', '--get', 'init.defaultBranch'], capture_output=True, text=True)
        self.assertEqual(git_config.returncode, 0, git_config.stderr)
        self.assertEqual(git_config.stdout.strip(), 'main')
        result = self.command('restore')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.target / '.codex/AGENTS.md').exists())

    def test_existing_settings_are_conflicts_not_silently_replaced(self):
        path = self.target / '.claude/settings.json'
        path.parent.mkdir(parents=True)
        path.write_text('{"custom":true}')
        result = self.command('apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(path.read_text()), {'custom': True})
        self.assertFalse((self.target / '.codex/AGENTS.md').exists())

    def test_shell_and_herdr_preserve_local_settings_and_restore(self):
        self.target.mkdir()
        original = '# Local shell settings\nexport LOCAL_SETTING=kept\n'
        (self.target / '.zshrc').write_text(original)
        herdr = self.target / '.config/herdr/config.toml'
        herdr.parent.mkdir(parents=True)
        herdr.write_text('[ui.sound]\nenabled = true\n')
        self.assertNotEqual(self.command('apply').returncode, 0)
        for _ in range(2):
            result = self.command('apply', '--replace')
            self.assertEqual(result.returncode, 0, result.stderr)
        text = (self.target / '.zshrc').read_text()
        self.assertTrue(text.startswith(original))
        self.assertEqual(text.count('# workflow:start'), 1)
        self.assertIn('interactive.zsh', text)
        self.assertEqual(self.command('doctor', '--config-only').returncode, 0)
        self.assertEqual(self.command('restore').returncode, 0)
        self.assertEqual((self.target / '.zshrc').read_text(), original)
        self.assertEqual(herdr.read_text(), '[ui.sound]\nenabled = true\n')
        self.assertFalse((self.target / '.config/workflow/interactive.zsh').exists())

    @unittest.skipUnless(shutil.which('zsh'), 'zsh is required')
    def test_interactive_shell_initializes_tools_once(self):
        self.assertEqual(self.command('apply').returncode, 0)
        prefix = self.target / 'brew'
        for relative, content in {
            'share/powerlevel10k/powerlevel10k.zsh-theme':
                'print theme >> "$HOME/events"\nfunction p10k() { :; }\n',
            'share/zsh-autosuggestions/zsh-autosuggestions.zsh':
                'print suggestions >> "$HOME/events"\nfunction _zsh_autosuggest_start() { :; }\n',
            'bin/fzf': '#!/bin/sh\nprintf "%s\\n" \'print fzf >> "$HOME/events"; function fzf-history-widget() { :; }\'\n',
            'bin/zoxide': '#!/bin/sh\nprintf "%s\\n" \'print zoxide >> "$HOME/events"; function __zoxide_z() { :; }\'\n',
        }.items():
            path = prefix / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            path.chmod(0o755)
        script = '''
function compdef() { :; }
source "$HOME/.config/workflow/interactive.zsh"
source "$HOME/.config/workflow/interactive.zsh"
[[ $POWERLEVEL9K_DIR_BACKGROUND == '#25364A' ]] || exit 3
[[ $POWERLEVEL9K_VCS_BACKGROUND == '#382B46' ]] || exit 4
'''
        env = dict(os.environ, HOME=str(self.target), ZDOTDIR=str(self.target),
                   HOMEBREW_PREFIX=str(prefix), PATH=str(prefix / 'bin') + ':/usr/bin:/bin')
        result = subprocess.run(['zsh', '-f', '-i', '-c', script], env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertCountEqual((self.target / 'events').read_text().splitlines(),
                              ['theme', 'suggestions', 'fzf', 'zoxide'])
        (self.target / 'events').unlink()
        result = subprocess.run(['zsh', '-f', '-c', 'source "$HOME/.zshrc"'], env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.target / 'events').exists())

    def test_doctor_can_limit_itself_to_configuration(self):
        self.assertEqual(self.command('apply').returncode, 0)
        result = self.command('doctor', '--config-only')
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        (self.target / '.codex/config.toml').write_text('invalid = [')
        result = self.command('doctor', '--config-only')
        self.assertNotEqual(result.returncode, 0)

    def test_network_and_tool_installation_are_not_part_of_apply(self):
        result = self.command('install-tools')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('brew update', result.stdout)
        self.assertIn('brew bundle', result.stdout)
        self.assertLess(result.stdout.index('brew update'), result.stdout.index('brew bundle'))
        self.assertIn('cask "gcloud-cli"', (ROOT / 'config/Brewfile').read_text())
        self.assertIn('preview', result.stdout.lower())
        self.assertFalse(self.target.exists())


if __name__ == '__main__':
    unittest.main()

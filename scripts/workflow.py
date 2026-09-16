#!/usr/bin/env python3
"""Portable workflow setup. plan is read-only; apply never installs packages."""
import argparse
import json
import os
import re
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

if sys.version_info < (3, 11):
    sys.exit('Python 3.11+ required. Run ./workflow, or install Python with: brew install python.')
import tomllib

from managed_files import ManagedFiles
from skill_sources import selected_paths, sync_sources

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads(path.read_text())


def block(existing, text):
    start, end = '# workflow:start', '# workflow:end'
    if start in existing or end in existing:
        if existing.count(start) != 1 or existing.count(end) != 1:
            raise RuntimeError('Ambiguous workflow block; edit the file manually.')
        a, b = existing.index(start), existing.index(end)
        if b < a:
            raise RuntimeError('Invalid workflow block.')
        return existing[:a] + start + '\n' + text + '\n' + end + existing[b + len(end):]
    return existing.rstrip('\n') + ('\n\n' if existing else '') + start + '\n' + text + '\n' + end + '\n'


def existing_text(path):
    return path.read_text() if path.is_file() else ''


def render(target, state, local_only=False):
    files = {}
    common = (ROOT / 'agents/common.md').read_bytes()
    files['.codex/AGENTS.md'] = common
    files['.claude/CLAUDE.md'] = common
    mcp = read_json(ROOT / 'config/mcp.json')
    codex = (ROOT / 'config/codex/config.toml').read_text()
    for name, value in mcp.items():
        value = dict(value)
        if value.get('command') == 'gitnexus':
            value['command'] = str(target / '.volta/bin/gitnexus')
        elif value.get('command') == 'npx':
            value['command'] = str(target / '.volta/bin/npx')
        codex += '\n[mcp_servers.' + json.dumps(name) + ']\n'
        for key, item in value.items():
            codex += key + ' = ' + json.dumps(item, ensure_ascii=False) + '\n'
    tomllib.loads(codex)
    files['.codex/config.toml'] = codex.encode()
    files['.claude/settings.json'] = (ROOT / 'config/claude/settings.json').read_bytes()
    files['.config/ghostty/config'] = (ROOT / 'config/ghostty/config').read_bytes()
    files['.config/workflow/gitconfig'] = (ROOT / 'config/git/config').read_bytes()
    files['.config/workflow/env.zsh'] = (ROOT / 'config/shell/env.zsh').read_bytes()
    files['.config/workflow/mcp.json'] = json.dumps({'mcpServers': mcp}, indent=2).encode() + b'\n'
    files['.zshrc'] = block(existing_text(target / '.zshrc'),
                           'source ' + shlex.quote(str(target / '.config/workflow/env.zsh'))).encode()
    files['.gitconfig'] = block(existing_text(target / '.gitconfig'),
                               '[include]\n    path = ' + json.dumps(str(target / '.config/workflow/gitconfig'), ensure_ascii=False)).encode()
    paths = {p.parent.name: p.parent for p in (ROOT / 'skills').glob('*/*/SKILL.md')}
    missing = []
    if not local_only:
        manifest = read_json(ROOT / 'skills/sources.json')
        external, missing = selected_paths(manifest, state / 'skills')
        if set(external) & set(paths):
            raise RuntimeError('Duplicate local/external skill names.')
        paths.update(external)
        # Retire only links installed by this tool. User-owned directories and
        # links without a journal record must not be removed by catalog edits.
        managed = ManagedFiles(target, state).load()['files']
        for name in manifest.get('retired_skills', []):
            for parent in ('.agents/skills', '.claude/skills'):
                relative = parent + '/' + name
                record = managed.get(relative)
                if record and (record['installed']['kind'] == 'link' or
                               (record['installed']['kind'] == 'missing' and
                                record.get('pending', {}).get('kind') == 'link')):
                    files[relative] = None
    for name, path in paths.items():
        files['.agents/skills/' + name] = {'link': str(path)}
        files['.claude/skills/' + name] = {'link': str(path)}
    return files, missing


def tool_commands():
    tools = read_json(ROOT / 'config/tools.json')
    commands = [['brew', 'bundle', '--file', str(ROOT / 'config/Brewfile')],
                ['volta', 'install', 'node@' + tools['node']],
                ['volta', 'install', 'pnpm@' + tools['pnpm']]]
    commands.extend(['volta', 'install', name + '@' + version] for name, version in tools['packages'].items())
    commands.extend(['gh', 'extension', 'install', item['repository'], '--pin', item['revision']]
                    for item in tools['extensions'])
    return commands


def install_tools(execute, target):
    if execute and (sys.platform != 'darwin' or target != Path.home().resolve()):
        raise RuntimeError('Tool installation requires real macOS home; no --target override.')
    print('Execute tools' if execute else 'Preview only; add --execute to install tools.')
    env = dict(os.environ, VOLTA_FEATURE_PNPM='1')
    env['PATH'] = str(Path.home() / '.volta/bin') + ':/opt/homebrew/bin:/usr/local/bin:' + env.get('PATH', '')
    for command in tool_commands():
        print(shlex.join(command), flush=True)
        if execute:
            if command[:3] == ['gh', 'extension', 'install']:
                # gh returns an error for an already installed extension. Verify
                # it rather than upgrading an existing user-managed extension.
                found = subprocess.run(['gh', 'extension', 'list'], env=env, capture_output=True, text=True, check=True)
                matches = [line for line in found.stdout.splitlines() if command[3] in line]
                if matches:
                    if command[-1] not in matches[0].split():
                        raise RuntimeError('Existing gh-stack version differs; inspect gh extension list before upgrading.')
                    print('Already installed at requested version.')
                    continue
            subprocess.run(command, env=env, check=True)
    print('Manual tools/plugins and login steps: config/tools.json and docs/setup.md')


def configure_mcp(execute, target):
    if execute and target != Path.home().resolve():
        raise RuntimeError('Claude MCP registration requires real home; no --target override.')
    existing = read_json(target / '.claude.json').get('mcpServers', {}) if (target / '.claude.json').is_file() else {}
    servers = read_json(ROOT / 'config/mcp.json')
    pending = []
    for name, config in servers.items():
        config = dict(config)
        config['type'] = 'http' if 'url' in config else 'stdio'
        if config.get('command') in ('gitnexus', 'npx'):
            config['command'] = str(target / '.volta/bin' / config['command'])
        if name in existing:
            comparable = dict(existing[name])
            comparable.setdefault('type', 'http' if 'url' in comparable else 'stdio')
            if comparable != config:
                raise RuntimeError(f'Existing Claude MCP conflict: {name}; inspect with claude mcp get {name}.')
        else:
            pending.append(['claude', 'mcp', 'add-json', '--scope', 'user', name, json.dumps(config)])
    print('Execute MCP registration' if execute else 'Preview only; add --execute to register Claude MCP.')
    for command in pending:
        print(shlex.join(command), flush=True)
        if execute:
            subprocess.run(command, check=True)
    print('MCP registration does not prove authentication or service connectivity.')


def doctor(manager, files, missing, config_only=False, online=False):
    problems = []
    for row in manager.plan(files):
        if row['status'] != 'unchanged':
            problems.append(row['status'] + ': ' + row['path'])
    problems.extend('missing skill: ' + name for name in missing)
    for relative, parser in [('.codex/config.toml', tomllib.loads), ('.claude/settings.json', json.loads)]:
        try:
            parser((manager.target / relative).read_text())
        except (ValueError, OSError) as error:
            problems.append(f'invalid config {relative}: {error}')
    for name, value in files.items():
        if isinstance(value, dict) and not Path(value['link']).exists():
            problems.append('broken skill target: ' + name)
    if not config_only:
        for name in ['git', 'gh', 'volta', 'node', 'pnpm', 'codex', 'claude', 'gitnexus', 'playwriter', 'glow', 'duti']:
            resolved = shutil.which(name)
            print('CLI', name, resolved or 'MISSING')
            if not resolved:
                problems.append('missing CLI: ' + name)
        for name, command in [('github', ['gh', 'auth', 'status']), ('codex', ['codex', 'login', 'status']),
                              ('claude', ['claude', 'auth', 'status'])]:
            if online and shutil.which(command[0]):
                result = subprocess.run(command, capture_output=True, timeout=30)
                print('AUTH', name, 'OK' if result.returncode == 0 else 'NEEDS LOGIN')
                if result.returncode:
                    problems.append('login required: ' + name)
            else:
                print('AUTH', name, 'NOT CHECKED (use --online)')
        tools = read_json(ROOT / 'config/tools.json')
        versions = {'node': tools['node'], 'pnpm': tools['pnpm'],
                    'codex': tools['packages']['@openai/codex'],
                    'gitnexus': tools['packages']['gitnexus'], 'playwriter': tools['packages']['playwriter']}
        for name, expected in versions.items():
            if shutil.which(name):
                result = subprocess.run([name, '--version'], capture_output=True, text=True, timeout=30)
                match = re.search(r'\b\d+\.\d+\.\d+\b', result.stdout)
                actual = match.group() if match else 'unknown'
                print('VERSION', name, actual, 'expected', expected)
                if result.returncode or actual != expected:
                    problems.append('CLI version differs: ' + name)
        print('MCP connectivity: NOT CHECKED; validate in each signed-in client.')
    for issue in problems:
        print('ISSUE', issue)
    print('Configuration matches' if not problems else f'{len(problems)} issue(s); not fully configured.')
    return 2 if problems else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['plan', 'apply', 'restore', 'doctor', 'sync-skills', 'install-tools', 'configure-mcp'])
    parser.add_argument('--target', type=Path, default=Path.home())
    parser.add_argument('--state-dir', type=Path)
    parser.add_argument('--local-only', action='store_true', help='Only local skills, no external skill requirements.')
    parser.add_argument('--replace', action='store_true', help='Back up and replace conflicting files/leaf links; never directories.')
    parser.add_argument('--execute', action='store_true', help='Execute tool installs or Claude MCP registration.')
    parser.add_argument('--config-only', action='store_true')
    parser.add_argument('--online', action='store_true', help='Check client login status without printing credentials.')
    args = parser.parse_args()
    target = args.target.expanduser().resolve()
    state = args.state_dir or target / '.local/state/workflow'
    manager = ManagedFiles(target, state)
    if args.command == 'install-tools':
        install_tools(args.execute, target)
        return 0
    if args.command == 'configure-mcp':
        configure_mcp(args.execute, target)
        return 0
    if args.command == 'sync-skills':
        with manager.lock():
            sync_sources(read_json(ROOT / 'skills/sources.json'), manager.state / 'skills')
        return 0
    if args.command == 'restore':
        print('Restored', manager.restore(), 'managed file(s); packages and logins retained.')
        return 0
    files, missing = render(target, manager.state, args.local_only)
    if args.command == 'doctor':
        return doctor(manager, files, missing, args.config_only, args.online)
    if args.command == 'apply':
        if missing:
            raise RuntimeError('Missing skills; run sync-skills first: ' + ', '.join(missing))
        rows = manager.apply(files, args.replace)
    else:
        rows = manager.plan(files)
    for row in rows:
        print(row['status'].ljust(10), row['path'])
    if missing:
        print('Missing external skills; run sync-skills:', ', '.join(missing))
    return 2 if missing or (args.command == 'plan' and any(row['status'] == 'conflict' for row in rows)) else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (RuntimeError, OSError, ValueError, subprocess.SubprocessError) as error:
        print('Error:', error, file=sys.stderr)
        sys.exit(1)

"""Follow upstream HEAD; record resolved commits locally after a complete sync."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


def tree_hash(path):
    digest = hashlib.sha256()
    for file in sorted(path.rglob('*')):
        if file.is_symlink():
            raise RuntimeError(f'Skill contains a symlink; explicit review required: {file}')
        if file.is_file():
            name = str(file.relative_to(path)).encode()
            content = file.read_bytes()
            digest.update(len(name).to_bytes(8, 'big') + name)
            digest.update(len(content).to_bytes(8, 'big') + content)
    return digest.hexdigest()


def validate(manifest):
    names = set()
    for source in manifest['sources']:
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', source['repository']):
            raise RuntimeError('Invalid skill repository.')
        if 'revision' in source:
            raise RuntimeError('Catalog must follow latest; revisions belong in local sync state.')
        for skill in source['skills']:
            if not re.fullmatch(r'[a-z0-9-]+', skill['name']) or skill['name'] in names:
                raise RuntimeError('Invalid or duplicate skill name.')
            names.add(skill['name'])
            path = Path(skill['path'])
            if path.is_absolute() or '..' in path.parts or not path.parts:
                raise RuntimeError('Invalid skill source path.')


def checkout_path(cache, repository, revision, skills):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository) or not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise RuntimeError('Invalid resolved source path.')
    selection = json.dumps(sorted(item['path'] for item in skills)).encode()
    key = hashlib.sha256(selection).hexdigest()[:16]
    return cache / repository.replace('/', '--') / (revision + '-' + key)


def source_url(source):
    return 'https://github.com/' + source['repository'] + '.git'


def git(directory, *args):
    result = subprocess.run(['git', '-C', str(directory), *args],
                            env=dict(os.environ, GIT_TERMINAL_PROMPT='0'),
                            capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or 'Git source download failed.')
    return result.stdout.strip()


def sync_sources(manifest, cache):
    validate(manifest)
    resolved = {'sources': []}
    for source in manifest['sources']:
        url = source_url(source)
        head = git(Path.cwd(), 'ls-remote', url, 'HEAD').split()
        if not head or not re.fullmatch(r'[0-9a-f]{40}', head[0]):
            raise RuntimeError('Could not resolve upstream HEAD: ' + source['repository'])
        revision = head[0]
        destination = checkout_path(cache, source['repository'], revision, source['skills'])
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            print('Fetch latest', source['repository'], revision, flush=True)
            with tempfile.TemporaryDirectory(prefix='.fetch-', dir=destination.parent) as temp:
                work = Path(temp)
                git(work, 'init', '-q')
                git(work, 'remote', 'add', 'origin', url)
                git(work, 'config', 'remote.origin.promisor', 'true')
                git(work, 'config', 'remote.origin.partialclonefilter', 'blob:none')
                git(work, 'sparse-checkout', 'init', '--cone')
                git(work, 'sparse-checkout', 'set', *[s['path'] for s in source['skills']])
                git(work, 'fetch', '--depth=1', '--filter=blob:none', 'origin', revision)
                git(work, 'checkout', '--detach', 'FETCH_HEAD')
                if git(work, 'rev-parse', 'HEAD') != revision:
                    raise RuntimeError('Downloaded Git revision mismatch.')
                work.rename(destination)
        if destination.is_symlink() or git(destination, 'rev-parse', 'HEAD') != revision:
            raise RuntimeError('Cached source revision mismatch.')
        if git(destination, 'status', '--porcelain', '--untracked-files=all', '--ignored'):
            raise RuntimeError('Cached source has local edits: ' + str(destination))
        entry = {'repository': source['repository'], 'revision': revision, 'skills': []}
        for skill in source['skills']:
            path = destination / skill['path']
            if not (path / 'SKILL.md').is_file():
                raise RuntimeError(f'Missing SKILL.md: {skill["name"]}')
            digest = tree_hash(path)
            entry['skills'].append(dict(skill, sha256=digest))
            print('Verified', skill['name'], flush=True)
        resolved['sources'].append(entry)
    # Keep the previous complete snapshot active if any source fails above.
    cache.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.resolved-', dir=cache)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(resolved, stream, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, cache / 'resolved.json')
    finally:
        if os.path.exists(name):
            os.unlink(name)


def selected_paths(manifest, cache):
    validate(manifest)
    result = {}
    missing = []
    state_file = cache / 'resolved.json'
    resolved = json.loads(state_file.read_text()) if state_file.is_file() else {'sources': []}
    records = {item['repository']: item for item in resolved['sources']}
    for source in manifest['sources']:
        record = records.get(source['repository'])
        installed = {item['name']: item for item in record['skills']} if record else {}
        for skill in source['skills']:
            item = installed.get(skill['name'])
            if not item or item['path'] != skill['path']:
                missing.append(skill['name'])
                continue
            path = checkout_path(cache, source['repository'], record['revision'], record['skills']) / skill['path']
            if not (path / 'SKILL.md').is_file():
                missing.append(skill['name'])
            elif tree_hash(path) != item.get('sha256'):
                raise RuntimeError(f'Skill checksum mismatch: {skill["name"]}')
            else:
                result[skill['name']] = path
    return result, missing

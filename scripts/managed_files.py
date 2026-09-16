"""Manage a bounded set of files with conflict detection and a recovery journal."""
import base64
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import tempfile
import time


def snapshot(path):
    if path.is_symlink():
        return {'kind': 'link', 'link': os.readlink(path)}
    if not path.exists():
        return {'kind': 'missing'}
    if not path.is_file():
        return {'kind': 'directory'}
    return {'kind': 'file', 'data': base64.b64encode(path.read_bytes()).decode(),
            'mode': path.stat().st_mode & 0o777}


def fingerprint(value):
    if value['kind'] == 'file':
        return ('file', hashlib.sha256(base64.b64decode(value['data'])).hexdigest(), value['mode'])
    return (value['kind'], value.get('link'))


def desired(value):
    if isinstance(value, bytes):
        return {'kind': 'file', 'data': base64.b64encode(value).decode(), 'mode': 0o600}
    return {'kind': 'link', 'link': str(value['link'])}


def same_content(left, right):
    # Matching pre-existing files are adopted without modifying their permissions.
    if left['kind'] == right['kind'] == 'file':
        return left['data'] == right['data']
    return fingerprint(left) == fingerprint(right)


def write_snapshot(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if value['kind'] == 'missing':
        if path.exists() or path.is_symlink():
            path.unlink()
        return
    fd, name = tempfile.mkstemp(prefix='.workflow-', dir=path.parent)
    temporary = Path(name)
    try:
        if value['kind'] == 'link':
            os.close(fd)
            temporary.unlink()
            temporary.symlink_to(value['link'])
        else:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(base64.b64decode(value['data']))
                stream.flush()
                os.fsync(stream.fileno())
            temporary.chmod(value['mode'])
        os.replace(temporary, path)
    finally:
        if temporary.exists() or temporary.is_symlink():
            temporary.unlink()


class ManagedFiles:
    def __init__(self, target, state):
        self.target = Path(target).expanduser().resolve()
        state = Path(state).expanduser()
        if state.is_symlink():
            raise RuntimeError('State symlink is not allowed.')
        self.state = state.resolve()

    def path(self, relative):
        rel = Path(relative)
        if rel.is_absolute() or not rel.parts or '..' in rel.parts or relative == '.':
            raise RuntimeError(f'Invalid managed path: {relative}')
        path = self.target / rel
        for parent in path.parents:
            if parent == self.target:
                break
            if parent.is_symlink():
                raise RuntimeError(f'Parent symlink is not allowed: {parent}')
            if parent.exists() and not parent.is_dir():
                raise RuntimeError(f'Parent is not a directory: {parent}')
        return path

    def load(self):
        journal = self.state / 'journal.json'
        if not journal.exists():
            return {'target': str(self.target), 'files': {}}
        data = json.loads(journal.read_text())
        if data.get('target') != str(self.target):
            raise RuntimeError('State belongs to a different target path.')
        return data

    def save(self, data):
        value = json.dumps(data, indent=2, ensure_ascii=False).encode()
        write_snapshot(self.state / 'journal.json', desired(value))

    @contextmanager
    def lock(self):
        for path in (self.state, *self.state.parents):
            if path.is_symlink():
                raise RuntimeError(f'State symlink is not allowed: {path}')
        self.state.mkdir(parents=True, exist_ok=True, mode=0o700)
        lock = self.state / '.lock'
        if lock.is_symlink():
            raise RuntimeError('State lock symlink is not allowed.')
        with lock.open('a') as stream:
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise RuntimeError('Another workflow operation holds the lock.')
            try:
                yield
            finally:
                fcntl.flock(stream, fcntl.LOCK_UN)

    def plan(self, files):
        journal = self.load()
        rows = []
        for relative, value in files.items():
            current = snapshot(self.path(relative))
            expected = desired(value)
            record = journal['files'].get(relative)
            if same_content(current, expected):
                status = 'unchanged'
            elif current['kind'] == 'missing' and not record:
                status = 'create'
            elif record and fingerprint(current) == fingerprint(record['installed']):
                status = 'update'
            else:
                status = 'conflict'
            rows.append({'path': relative, 'status': status})
        return rows

    def apply(self, files, replace=False):
        with self.lock():
            rows = self.plan(files)
            conflicts = [row['path'] for row in rows if row['status'] == 'conflict']
            if conflicts and not replace:
                raise RuntimeError('conflict: ' + ', '.join(conflicts))
            # Validate every destination before the first write, even with --replace.
            before = {name: snapshot(self.path(name)) for name in files}
            if any(value['kind'] == 'directory' for value in before.values()):
                raise RuntimeError('Directory conflict: move existing skill directories aside explicitly.')
            journal = self.load()
            for row in rows:
                name = row['path']
                if row['status'] == 'unchanged':
                    continue
                path = self.path(name)
                if fingerprint(snapshot(path)) != fingerprint(before[name]):
                    raise RuntimeError(f'Concurrent edit conflict: {name}')
                record = journal['files'].setdefault(name, {'original': before[name]})
                record.setdefault('history', []).append(before[name])
                record['pending'] = before[name]
                record['installed'] = desired(files[name])
                self.save(journal)  # Recoverable if the process exits before/after replace.
                write_snapshot(path, record['installed'])
                record.pop('pending')
                self.save(journal)
            return rows

    def restore(self):
        with self.lock():
            journal = self.load()
            for name, record in journal['files'].items():
                current = snapshot(self.path(name))
                allowed = [record['original'], record['installed']]
                if 'pending' in record:
                    allowed.append(record['pending'])
                if fingerprint(current) not in [fingerprint(item) for item in allowed]:
                    raise RuntimeError(f'Restore conflict: {name}; user changes retained.')
            count = len(journal['files'])
            if count:
                write_snapshot(self.state / f'restored-{time.time_ns()}.json',
                               desired(json.dumps(journal, ensure_ascii=False).encode()))
            for name in list(journal['files']):
                record = journal['files'][name]
                write_snapshot(self.path(name), record['original'])
                del journal['files'][name]
                self.save(journal)
            return count

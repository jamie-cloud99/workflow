#!/usr/bin/env python3
"""Build a Finder document opener; changing defaults is an explicit operation."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
BUNDLE_ID = 'com.jamiecloud99.workflow.markdown-preview'
APP_NAME = 'Markdown Preview.app'
LSREGISTER = '/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister'
EXTENSIONS = ('md', 'markdown')


def run(*args):
    return subprocess.run([str(arg) for arg in args], check=True)


def find_tool(name):
    path = shutil.which(name)
    if path:
        return path
    for prefix in ('/opt/homebrew/bin', '/usr/local/bin'):
        candidate = Path(prefix) / name
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    raise RuntimeError(f'Missing {name}. Install it before continuing.')


def default_app(duti, extension):
    result = subprocess.run([duti, '-x', extension], text=True, capture_output=True)
    lines = result.stdout.splitlines()
    if result.returncode or len(lines) < 3:
        raise RuntimeError(f'Cannot read current .{extension} default; no defaults changed. '
                           'Run outside a restricted sandbox, or install without --set-default.')
    return lines[-1].strip()


def save_defaults(duti, state):
    backup = state / 'defaults-before.json'
    if backup.exists():
        return
    previous = {ext: default_app(duti, ext) for ext in EXTENSIONS}
    if BUNDLE_ID in previous.values():
        raise RuntimeError('Preview is already default but its original backup is missing.')
    with backup.open('x') as stream:
        json.dump(previous, stream, indent=2)
        stream.write('\n')


def verify_default(duti, extension, expected):
    # LaunchServices can briefly return its old association after a valid write.
    for attempt in range(20):
        actual = default_app(duti, extension)
        if actual == expected:
            return
        if attempt < 19:
            time.sleep(0.5)
    raise RuntimeError(f'.{extension} default verification failed: {actual}')


def restore_defaults(duti, state):
    backup = state / 'defaults-before.json'
    previous = json.loads(backup.read_text())
    current = {ext: default_app(duti, ext) for ext in EXTENSIONS}
    for ext in EXTENSIONS:
        if current[ext] not in (BUNDLE_ID, previous[ext]):
            raise RuntimeError(f'.{ext} was changed since installation; leaving defaults intact.')
    for ext in EXTENSIONS:
        run(duti, '-s', previous[ext], '.' + ext, 'all')
    for ext in EXTENSIONS:
        verify_default(duti, ext, previous[ext])
    print('Restored original effective Markdown defaults. Application and packages retained.')


def build_app(destination):
    run('/usr/bin/osacompile', '-o', destination,
        ROOT / 'config/macos/Markdown Preview.applescript')
    shutil.copy2(ROOT / 'scripts/macos/preview-markdown.sh',
                 destination / 'Contents/Resources/preview-markdown.sh')
    plist_path = destination / 'Contents/Info.plist'
    with plist_path.open('rb') as stream:
        info = plistlib.load(stream)
    info.update({
        'CFBundleIdentifier': BUNDLE_ID,
        'CFBundleName': 'Markdown Preview',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1',
        'LSUIElement': True,
        'CFBundleDocumentTypes': [{
            'CFBundleTypeName': 'Markdown document',
            'CFBundleTypeExtensions': list(EXTENSIONS),
            'CFBundleTypeRole': 'Viewer',
            'LSHandlerRank': 'Alternate',
            'LSItemContentTypes': ['net.daringfireball.markdown',
                                  BUNDLE_ID + '.document'],
        }],
        'UTImportedTypeDeclarations': [{
            'UTTypeIdentifier': 'net.daringfireball.markdown',
            'UTTypeConformsTo': ['public.plain-text'],
            'UTTypeDescription': 'Markdown document',
            'UTTypeTagSpecification': {'public.filename-extension': ['md']},
        }],
        # Another app may export the standard UTI for .md only. Its declaration
        # wins over our import, leaving .markdown dynamic (duti rejects -50).
        'UTExportedTypeDeclarations': [{
            'UTTypeIdentifier': BUNDLE_ID + '.document',
            'UTTypeConformsTo': ['net.daringfireball.markdown', 'public.plain-text'],
            'UTTypeDescription': 'Markdown document',
            'UTTypeTagSpecification': {'public.filename-extension': ['markdown']},
        }],
    })
    with plist_path.open('wb') as stream:
        plistlib.dump(info, stream)
    # osacompile may sign the app; resources and metadata were just changed.
    run('/usr/bin/codesign', '--force', '--sign', '-', destination)
    run('/usr/bin/codesign', '--verify', '--deep', '--strict', destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app-dir', type=Path, default=Path.home() / 'Applications')
    parser.add_argument('--state-dir', type=Path,
                        default=Path.home() / 'Library/Application Support/dev-workflow/markdown-preview')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--set-default', action='store_true')
    mode.add_argument('--restore-defaults', action='store_true')
    args = parser.parse_args()
    if sys.platform != 'darwin':
        raise RuntimeError('This installer requires macOS.')
    state = args.state_dir.expanduser().resolve()
    if args.restore_defaults:
        restore_defaults(find_tool('duti'), state)
        return
    find_tool('glow')
    if not any((root / 'Ghostty.app').is_dir()
               for root in (Path('/Applications'), Path.home() / 'Applications')):
        raise RuntimeError('Install Ghostty in /Applications or ~/Applications first.')
    app_dir = args.app_dir.expanduser().resolve()
    app_dir.mkdir(parents=True, exist_ok=True)
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    duti = find_tool('duti') if args.set_default else None
    if duti:
        save_defaults(duti, state)
    destination = app_dir / APP_NAME
    with tempfile.TemporaryDirectory(prefix='.markdown-preview-', dir=app_dir) as temp:
        built = Path(temp) / APP_NAME
        build_app(built)
        if destination.exists() or destination.is_symlink():
            if destination.is_symlink():
                raise RuntimeError(f'Refusing to replace symlink: {destination}')
            backup_base = state / ('app-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
            # An unpacked .app backup can be discovered as another live handler.
            backup = shutil.make_archive(str(backup_base), 'zip',
                                         root_dir=app_dir, base_dir=APP_NAME)
            shutil.rmtree(destination)
            print(f'Previous application backed up: {backup}')
        shutil.move(str(built), str(destination))
    run(LSREGISTER, '-f', destination)
    if duti:
        for ext in EXTENSIONS:
            run(duti, '-s', BUNDLE_ID, '.' + ext, 'all')
        for ext in EXTENSIONS:
            verify_default(duti, ext, BUNDLE_ID)
            print(f'.{ext} -> {BUNDLE_ID}')
    print(f'Installed: {destination}')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)

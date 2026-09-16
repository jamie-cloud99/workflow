"""Validate repository-owned configuration and documentation without network access."""
import ast
import json
from pathlib import Path
import re
import tomllib

from skill_sources import validate

ROOT = Path(__file__).resolve().parents[1]


def main():
    for path in (ROOT / 'config').rglob('*.json'):
        json.loads(path.read_text())
    for path in (ROOT / 'config').rglob('*.toml'):
        tomllib.loads(path.read_text())
    validate(json.loads((ROOT / 'skills/sources.json').read_text()))
    for path in (ROOT / 'scripts').rglob('*.py'):
        ast.parse(path.read_text(), filename=str(path))
    for path in (ROOT / 'skills').glob('*/*/SKILL.md'):
        text = path.read_text()
        assert text.startswith('---\n'), path
        metadata = text.split('---', 2)[1]
        assert re.search(r'^name: ' + re.escape(path.parent.name) + r'$', metadata, re.M), path
        assert re.search(r'^description: .+', metadata, re.M), path
    for path in [ROOT / 'README.md', *(ROOT / 'docs').glob('*.md'), ROOT / 'skills/README.md']:
        text = path.read_text()
        assert text.count('```') % 2 == 0, f'Unbalanced code fence: {path}'
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if '://' in link or link.startswith('#'):
                continue
            assert (path.parent / link.split('#')[0]).exists(), f'Broken link: {path}: {link}'
    print('Config, Python syntax, skill metadata and documentation links validated.')


if __name__ == '__main__':
    main()

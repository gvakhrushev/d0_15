"""Replay the published checks, keeping the original receipt outside the writable run."""
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def replay(repo, check):
    revision = check['commit']
    directory = Path(check['directory'])

    def blob(path):
        return git(repo, 'cat-file', 'blob', f'{revision}:{path.as_posix()}')

    if 'archive_receipt' in check:
        expected = blob(directory / check['archive_receipt'])
        source = 'original Git receipt'
    else:
        expected = ('\n'.join(check['expected_lines']) + '\n').encode()
        source = 'A88 replay transcript (upstream printed stdout only)'
    if sha256(expected).hexdigest() != check['expected_sha256']:
        raise ValueError(f"Pinned reference differs for {check['id']}")

    with TemporaryDirectory(prefix='d0-a88-owner-') as temp:
        root = Path(temp)
        env = dict(os.environ, PYTHONOPTIMIZE='0')
        if check.get('needs_git_objects'):
            # The B182 owner itself reads an explicit historical object with git show.
            subprocess.run(['git', 'init', '--quiet', str(root)], check=True)
            objects = git(repo, 'rev-parse', '--path-format=absolute', '--git-path', 'objects')
            env.update(GIT_DIR=str(root/'.git'), GIT_WORK_TREE=str(root),
                       GIT_ALTERNATE_OBJECT_DIRECTORIES=objects.decode().strip())
        paths = [directory/name for name in check['files']] + [Path(name) for name in check.get('repository_files', [])]
        for path in paths:
            if path.is_absolute() or '..' in path.parts:
                raise ValueError(f'Unexpected input path {path}')
            destination = root/path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(blob(path))
        actual = subprocess.check_output([sys.executable, '-B', check['entrypoint']], cwd=root/directory, env=env)
    if actual != expected:
        raise ValueError(f"Original program output differs from {source} for {check['id']}")
    return dict(id=check['id'], commit=revision, reference=source, stdout_sha256=check['expected_sha256'])


def main():
    repo = os.environ.get('D0_PILOT_OBJECT_REPO') or git(Path.cwd(),'rev-parse','--show-toplevel').decode().strip()
    cases = json.loads(Path(__file__).with_name('extended_sources.json').read_bytes())
    print(json.dumps([replay(repo, check) for check in cases], indent=2))


if __name__ == '__main__':
    main()

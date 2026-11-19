#!/usr/bin/env python3
"""Restore the 83 immutable v4/v5 source paths, without network or silent overwrite.

The original 82 text files and one v4 ZIP are recovered byte-for-byte. The ZIP
is re-encoded with its original metadata and deflate level; its recorded hash
must match or restoration fails. No code from the capsule is executed here.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import lzma
from pathlib import Path, PurePosixPath
import zipfile

CAPSULE_SHA256 = '91b030d62c93afa6bf2a23be28051d764e54f12a7e5a13cd75ed732427c913be'
JSON_SHA256 = '3062ab678735883022bdc011471ae438d5a30bdcb013acea549bfd572e97564f'
V4_PREFIX = '02_REGISTRY/research/sources/d0_internal_routing_v4_2026-10-14/'
ZIP_PREFIX = 'd0_v4_unconditional_preparation/'
PARTS = 8


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(ok: bool, label: str) -> None:
    if not ok:
        raise ValueError(label)


def safe_path(name: str) -> PurePosixPath:
    p = PurePosixPath(name)
    require(not p.is_absolute() and bool(p.parts), 'UNSAFE_PATH')
    require(all(x not in ('..', '.', '.git', '') for x in p.parts), 'UNSAFE_PATH')
    require('\\' not in name and ':' not in name, 'UNSAFE_PATH')
    require(name.startswith('02_REGISTRY/research/'), 'OUTSIDE_RESEARCH_SCOPE')
    return p


def payload(capsule_dir: Path) -> dict[str, bytes]:
    packed = b''.join((capsule_dir/'parts'/f'{i:02}.xzpart').read_bytes() for i in range(PARTS))
    require(len(packed) == 59272 and digest(packed) == CAPSULE_SHA256, 'CAPSULE_HASH')
    raw = lzma.decompress(packed)
    require(digest(raw) == JSON_SHA256, 'JSON_HASH')
    obj = json.loads(raw)
    require(obj['schema'] == 'd0-byte-preserving-source-capsule/1', 'SCHEMA')
    out = {name: text.encode('utf-8') for name, text in obj['files'].items()}
    require(len(out) == 82, 'TEXT_COUNT')
    patch = ''
    for name in sorted(out):
        safe_path(name)
        if not name.startswith(V4_PREFIX):
            continue
        data = out[name]
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        lines = data.decode('utf-8').splitlines(keepends=True)
        patch += (f'diff --git a/{name} b/{name}\nnew file mode 100644\n'
                  f'index {"0"*40}..{blob}\n--- /dev/null\n+++ b/{name}\n'
                  f'@@ -0,0 +1,{len(lines)} @@\n' + ''.join('+'+line for line in lines))
    recipe = obj['zip_recipe']
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as z:
        z.comment = bytes(recipe['comment'])
        for meta in recipe['entries']:
            name = meta['filename']
            info = zipfile.ZipInfo(name, tuple(meta['date_time']))
            for key, value in meta.items():
                if key not in ('filename', 'date_time'):
                    setattr(info, key, bytes(value) if key in ('comment', 'extra') else value)
            if name.startswith(ZIP_PREFIX):
                data = out[V4_PREFIX+name[len(ZIP_PREFIX):]]
            elif name == 'D0_internal_routing_v4_2026-10-14.patch':
                data = patch.encode('utf-8')
            else:
                data = recipe['extra_texts'][name].encode('utf-8')
            z.writestr(info, data, compresslevel=recipe['compression_level'])
    out[recipe['path']] = stream.getvalue()
    require(len(out) == 83 and set(out) == set(obj['sha256']), 'PATH_SET')
    for name, data in out.items():
        safe_path(name)
        require(digest(data) == obj['sha256'][name], 'RESTORED_HASH:'+name)
    return out


def restore(capsule_dir: Path, destination: Path) -> dict:
    files = payload(capsule_dir)
    root = destination.resolve()
    root.mkdir(parents=True, exist_ok=True)
    # Complete collision and symlink preflight before any file write.
    for name, data in files.items():
        target = root.joinpath(*safe_path(name).parts)
        require(target.resolve().is_relative_to(root), 'ESCAPING_SYMLINK')
        if target.exists():
            require(target.is_file() and target.read_bytes() == data, 'EXISTING_DIFFERENT:'+name)
    for name, data in files.items():
        target = root.joinpath(*safe_path(name).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_bytes(data)
        require(target.read_bytes() == data, 'WRITE_VERIFICATION:'+name)
    return {'status': 'PASS', 'restored_paths': len(files), 'capsule_sha256': CAPSULE_SHA256,
            'all_83_original_files_byte_identical': True}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    if args.verify_only:
        print(json.dumps({'status': 'PASS', 'verified_paths': len(payload(here))}))
    elif args.destination:
        print(json.dumps(restore(here, args.destination), indent=2))
    else:
        parser.error('supply --destination or --verify-only')

if __name__ == '__main__':
    main()

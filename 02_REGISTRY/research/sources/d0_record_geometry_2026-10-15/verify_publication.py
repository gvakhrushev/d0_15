#!/usr/bin/env python3
"""Verify readable preservation; optional comparison against the original ZIP."""
import argparse
import base64
import hashlib
import io
import json
import lzma
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(name):
    p = PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and '\\' not in name,
            'Unsafe path: ' + name)
    return p


def verify(original_zip=None):
    meta = json.loads((HERE / 'TEXT_MANIFEST.json').read_text(encoding='utf8'))
    require(meta['schema'] == 'd0-readable-research-publication/1', 'Schema')
    for name, rec in meta['text_files'].items():
        path = (HERE / safe_path(name)).resolve()
        require(path.is_relative_to(HERE), 'Path escape')
        data = path.read_bytes()
        data.decode('utf8')
        require(len(data) == rec['bytes'] and digest(data) == rec['sha256'],
                'Preserved text differs: ' + name)
    records = meta['occurrences'] + meta['previous_strategy_capsule']
    for rec in records:
        require(meta['text_files'][rec['published']] ==
                {'sha256': rec['sha256'], 'bytes': rec['bytes']},
                'Invalid text alias: ' + rec['source'])
    require(set(meta['text_files']) == {r['published'] for r in records},
            'Unreferenced preserved content')
    require(len({r['source'] for r in meta['occurrences']}) ==
            len(meta['occurrences']), 'Repeated source path')
    outer_unique = {r['sha256'] for r in meta['occurrences']}
    require(len({r['sha256'] for r in meta['text_files'].values()}) ==
            len(meta['text_files']), 'Duplicate stored text content')
    counts = {
        'outer_text_occurrences': len(meta['occurrences']),
        'outer_unique_text_contents': len(outer_unique),
        'nested_archive_occurrences': sum(len(a['sources']) for a in meta['archives'].values()),
        'unique_nested_archives': len(meta['archives']),
        'binary_chunk_occurrences': len(meta['binary_occurrences']),
        'previous_strategy_text_occurrences': len(meta['previous_strategy_capsule']),
        'published_unique_text_contents': len(meta['text_files']),
    }
    require(counts == meta['counts'], 'Count mismatch')
    require(counts == dict(outer_text_occurrences=150, outer_unique_text_contents=77,
                          nested_archive_occurrences=7, unique_nested_archives=4,
                          binary_chunk_occurrences=10, previous_strategy_text_occurrences=21,
                          published_unique_text_contents=78), 'Incomplete source inventory')
    previous = HERE.parent / 'd0_strategy_handoff_2026-10-15'
    old_meta = json.loads((previous / 'INPUT_MANIFEST.json').read_text(encoding='utf8'))
    packed = base64.b64decode(''.join((previous / f'payload.b64.{i:02}').read_text().strip()
                                    for i in range(6)), validate=True)
    require(digest(packed) == old_meta['packed_sha256'], 'Prior packed SHA')
    raw = lzma.decompress(packed)
    require(digest(raw) == old_meta['json_sha256'], 'Prior JSON SHA')
    old_files = json.loads(raw)
    previous_records = {r['source']: r for r in meta['previous_strategy_capsule']}
    require(set(old_files) == set(previous_records) == set(old_meta['files']), 'Prior file set')
    for name, text in old_files.items():
        rec = previous_records[name]
        require(digest(text.encode()) == rec['sha256'] == old_meta['files'][name],
                'Prior plaintext differs: ' + name)
    original_compared = False
    if original_zip is not None:
        data = Path(original_zip).read_bytes()
        require(digest(data) == meta['outer_zip']['sha256'] and
                len(data) == meta['outer_zip']['bytes'], 'Original ZIP differs')
        texts, archives, binaries, chunks = {}, {}, {}, {}

        def walk(blob, prefix):
            with ZipFile(io.BytesIO(blob)) as z:
                for item in z.infolist():
                    if item.is_dir():
                        continue
                    safe_path(item.filename)
                    name = prefix + '!/' + item.filename
                    b = z.read(item)
                    if item.filename.endswith('.zip'):
                        archives[name] = {'sha256': digest(b), 'bytes': len(b)}
                        walk(b, name)
                    else:
                        try:
                            b.decode('utf8')
                        except UnicodeDecodeError:
                            binaries[name] = {'sha256': digest(b), 'bytes': len(b)}
                            chunks[name] = b
                        else:
                            texts[name] = {'sha256': digest(b), 'bytes': len(b)}

        walk(data, meta['outer_zip']['name'])
        expected_text = {r['source']: {'sha256': r['sha256'], 'bytes': r['bytes']}
                         for r in meta['occurrences']}
        expected_archive = {n: {'sha256': h, 'bytes': a['bytes']}
                            for h, a in meta['archives'].items() for n in a['sources']}
        expected_binary = {r['source']: {'sha256': r['sha256'], 'bytes': r['bytes']}
                           for r in meta['binary_occurrences']}
        require(texts == expected_text, 'Original text coverage differs')
        require(archives == expected_archive, 'Original archive coverage differs')
        require(binaries == expected_binary, 'Original binary coverage differs')
        groups = {}
        for name, b in chunks.items():
            groups.setdefault(name.rsplit('/', 1)[0], {})[name.rsplit('.', 1)[-1]] = b
        require(set(groups) == {c['source'] for c in meta['compressed_capsules']},
                'Compressed capsule set differs')
        for cap in meta['compressed_capsules']:
            parts = groups[cap['source']]
            packed = b''.join(parts[k] for k in sorted(parts))
            decoded = lzma.decompress(packed)
            require(digest(packed) == cap['packed_sha256'], 'Compressed SHA')
            require(digest(decoded) == cap['decoded_json_sha256'] and
                    len(decoded) == cap['decoded_json_bytes'], 'Decoded JSON SHA')
            files = json.loads(decoded)
            require(set(files) == {r['source'] for r in cap['files']}, 'Decoded file set')
            for rec in cap['files']:
                require(files[rec['source']].encode() == (HERE / rec['published']).read_bytes(),
                        'Compressed source missing from text: ' + rec['source'])
        original_compared = True
    return {'status': 'PASS_READABLE_RESEARCH_PRESERVATION', 'counts': counts,
            'original_zip_compared': original_compared,
            'scientific_acceptance': False, 'GR_closure': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original-zip', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.original_zip), ensure_ascii=False, indent=2, sort_keys=True))

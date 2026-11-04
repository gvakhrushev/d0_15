#!/usr/bin/env python3
"""Verify split v3 replay bytes and optionally restore the full JSON to a new file."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

base = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--extract', type=Path, help='new destination for full JSON')
args = parser.parse_args()
manifest = json.loads((base / 'manifest.json').read_text(encoding='utf-8'))
def require(condition, message):
    if not condition:
        raise ValueError(message)
def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()
require(manifest['schema'] == 'd0-v3-full-b308-split-archive-v1', 'schema')
summary_path = base / 'summary.json'
require(digest(summary_path) == manifest['summary_sha256'], 'summary digest')
summary = json.loads(summary_path.read_text(encoding='utf-8'))
require(summary['full_output_sha256'] == manifest['full_sha256'], 'source digest binding')
require(summary['search_cases_found_all_sources'] == 50 and summary['search_cases_total'] == 50, 'case totals')
require(summary['discovery_validation'] == 'batched_rerun_same_implementation', 'discovery boundary')
require(sum(c['query_count'] for c in summary['cases']) == 414, 'query total')
require(sum(c['required_source_count'] for c in summary['cases']) == 415, 'source total')
require(all(not c['missing_paths'] for c in summary['cases']), 'missing sources')
require(summary['change_impact_regression']['status'] == 'pass', 'impact control')
with tempfile.TemporaryDirectory(prefix='d0-v3-archive-') as tmp:
    combined = Path(tmp) / 'replay.json.gz'
    with combined.open('xb') as out:
        for i, item in enumerate(manifest['parts']):
            require(item['name'] == 'part-%03d.gzchunk' % i, 'part sequence')
            part = base / 'parts' / item['name']
            require(part.is_file() and not part.is_symlink() and part.stat().st_size == item['bytes'], 'part metadata')
            require(digest(part) == item['sha256'], 'part digest')
            with part.open('rb') as inp:
                shutil.copyfileobj(inp, out, 1024 * 1024)
    require(digest(combined) == manifest['gzip_sha256'], 'gzip digest')
    full_hash = hashlib.sha256()
    if args.extract is not None:
        destination = args.extract.expanduser()
        require(not destination.exists(), 'destination already exists')
        target = destination.open('xb')
    else:
        target = None
    try:
        with gzip.open(combined, 'rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                full_hash.update(block)
                if target is not None:
                    target.write(block)
    finally:
        if target is not None:
            target.close()
    require(full_hash.hexdigest() == manifest['full_sha256'], 'full replay digest')
print(json.dumps({'status':'PASS_ARCHIVE_INTEGRITY', 'cases':50, 'queries':414,
                  'required_sources':415, 'discovery':'same_implementation_rerun',
                  'semantic_review':'manual', 'GR_closed':False}, sort_keys=True))

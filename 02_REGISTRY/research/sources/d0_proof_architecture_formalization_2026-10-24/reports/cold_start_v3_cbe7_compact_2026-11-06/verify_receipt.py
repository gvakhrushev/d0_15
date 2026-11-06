#!/usr/bin/env python3
"""Check the compact historic evidence; this does not replay discovery."""
import argparse
import collections
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

P = Path(__file__).resolve().parent
M = json.loads((P / 'manifest.json').read_text())

def need(ok, what):
    if not ok:
        raise ValueError(what)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verify-git-pins', action='store_true', help='check explicit commit/path/blob triples against available Git objects')
    ap.add_argument('--check-raw', type=Path, help='also hash a separately supplied full producer JSON')
    args = ap.parse_args()
    blobs = {}
    for name, pin in M['files'].items():
        compressed = (P / name).read_bytes()
        need(len(compressed) == pin['compressed_bytes'] and digest(compressed) == pin['compressed_sha256'], name + ': compressed bytes')
        raw = gzip.decompress(compressed)
        need(len(raw) == pin['uncompressed_bytes'] and digest(raw) == pin['uncompressed_sha256'], name + ': uncompressed bytes')
        blobs[name] = raw
    archive = (P / 'archive.json').read_bytes()
    need(digest(archive) == M['archive_manifest_sha256'], 'archive manifest')
    meta = json.loads(archive)
    need(meta['full_sha256'] == M['full_raw']['sha256'] and meta['full_bytes'] == M['full_raw']['bytes'], 'archive binding')
    s = json.loads(blobs['summary.json.gz'])
    need(s['schema'] == 'd0-proof-architecture-cold-start-paged-summary-v3' and s['snapshot_commit'] == M['historical_snapshot'] and s['worktree_dirty'] is False, 'snapshot')
    need(s['corpus_snapshot'] == M['corpus_snapshot'] and s['ranking'] == {'window': 18, 'pages': 2, 'batched_scan_count': 1}, 'corpus/rank')
    need(s['full_output_sha256'] == M['full_raw']['sha256'] and s['discovery_validation'] == 'batched_rerun_same_implementation' and s['semantic_scope_review_is_manual'] is True, 'provenance')
    cases = s['cases']
    need(len(cases) == s['search_cases_total'] == M['case_count'] == 50 and s['search_cases_found_all_sources'] == M['found_all_case_count'] == 50, 'cases')
    need(sum(c['query_count'] for c in cases) == M['query_count'] == 414 and sum(c['required_source_count'] for c in cases) == M['required_rows'] == 415, 'queries/requirements')
    need(all(c['all_required_sources_found'] is True and c['missing_paths'] == [] and c['discovery_unattested_paths'] == [] and len(c['required_sources']) == c['required_source_count'] for c in cases), 'case completeness')
    rows = [r for c in cases for r in c['required_sources'].values()]
    need(all(r['found'] is True and r['status'] == 'found_direct_content' for r in rows), 'source status')
    need(s['benchmark_cases_total'] == 51 and s['change_impact_regression']['status'] == 'pass', 'impact')
    pins = {(r['expected_commit'], r['path'], r['expected_blob']) for r in rows if r.get('expected_commit') and r.get('expected_blob')}
    need(len(pins) == M['unique_explicit_pins_checked'] == 107 and sum(bool(r.get('expected_commit') and r.get('expected_blob')) for r in rows) == M['explicit_pinned_source_rows'] == 112, 'explicit pin counts')
    need(sum(r.get('source_origin') == 'pinned_snapshot' and not (r.get('expected_commit') and r.get('expected_blob')) for r in rows) == M['pinned_snapshot_rows_without_explicit_pair'] == 3, 'unpaired pin count')
    for name in ('producer_progress.jsonl.gz', 'compactor_progress.jsonl.gz'):
        events = [json.loads(line) for line in blobs[name].splitlines()]
        counts = collections.Counter(e.get('proof_search_progress') for e in events)
        need(counts['corpus_snapshot_complete'] == 2 and counts['search_started'] == 1 and counts['candidate_query_complete'] == 414, name + ': progress')
        if name.startswith('producer'):
            need(counts['verified_paged_query_ready'] == 414, name + ': pages')
    if args.verify_git_pins:
        ordered = sorted(pins)
        need(all('\n' not in c+p+b for c, p, b in ordered), 'invalid pin')
        data = ''.join(c + ':' + p + '\n' for c, p, _ in ordered).encode()
        result = subprocess.run(['git', '-C', str(P), 'cat-file', '--batch-check=%(objectname) %(objecttype)'], input=data, stdout=subprocess.PIPE, check=True)
        lines = result.stdout.decode().splitlines()
        need(len(lines) == len(ordered) and all(line == blob + ' blob' for (_, _, blob), line in zip(ordered, lines)), 'Git pins')
        for path, expected in s['authority_source_digests'].items():
            raw = subprocess.check_output(['git', '-C', str(P), 'show', M['historical_snapshot'] + ':' + path])
            need(digest(raw) == expected, 'authority source: ' + path)
        for path, pin in M['historical_tools'].items():
            ref = M['historical_snapshot'] + ':' + path
            raw = subprocess.check_output(['git', '-C', str(P), 'show', ref])
            actual = subprocess.check_output(['git', '-C', str(P), 'rev-parse', ref]).decode().strip()
            need(actual == pin['blob'] and digest(raw) == pin['sha256'], 'historical tool: ' + path)
    if args.check_raw:
        h = hashlib.sha256()
        count = 0
        with args.check_raw.open('rb') as f:
            for chunk in iter(lambda: f.read(1024*1024), b''):
                h.update(chunk)
                count += len(chunk)
        need(count == M['full_raw']['bytes'] and h.hexdigest() == M['full_raw']['sha256'], 'raw producer file')
    print('PASS: compact summary and progress evidence; 50 cases, 414 queries, 415 direct-content rows')
    print('Discovery reran the same implementation; source semantics remain manual; verify full archive separately.')
    if args.verify_git_pins:
        print('PASS: 107 unique explicitly paired Git pins, 7 authority sources and 4 historic tools; 3 pinned-origin rows have no explicit commit/blob pair.')
    if args.check_raw:
        print('PASS: separately supplied raw producer file matches the recorded size and SHA-256.')

if __name__ == '__main__':
    main()

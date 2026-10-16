#!/usr/bin/env python3
"""Verify the complete immutable local-intake snapshot, including both original ZIPs."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/'MANIFEST.json').read_text())
expected={x['path'] for x in m['files']}
actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
if expected!=actual:raise AssertionError(('FILE_SET_CHANGED',sorted(actual-expected),sorted(expected-actual)))
for item in m['files']:
 p=ROOT/item['path']
 if p.is_symlink() or not p.is_file():raise AssertionError(('NOT_REGULAR_FILE',item['path']))
 b=p.read_bytes()
 if len(b)!=item['bytes'] or hashlib.sha256(b).hexdigest()!=item['sha256']:
  raise AssertionError(('BYTE_MISMATCH',item['path']))
print('PASS_FULL_INTAKE_MANIFEST',len(expected),'files')

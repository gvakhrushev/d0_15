#!/usr/bin/env python3
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent
n=0
for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
    expected,name=line.split('  ',1)
    path=ROOT/name
    if not path.is_file():raise SystemExit('MISSING '+name)
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=expected:raise SystemExit('HASH_MISMATCH '+name)
    n+=1
print('PASS_ARCHIVE_MANIFEST',n,'files')

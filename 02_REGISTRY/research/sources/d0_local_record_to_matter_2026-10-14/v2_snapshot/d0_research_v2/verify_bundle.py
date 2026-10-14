"""Verify the exact published local snapshot, no network and no file rewriting."""
import hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
n=0
for line in (R/'SHA256SUMS.txt').read_text().splitlines():
    expected,relative=line.split('  ',1)
    p=(R/relative).resolve()
    if not p.is_relative_to(R) or not p.is_file():raise AssertionError(('UNSAFE_OR_MISSING_PATH',relative))
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    if got!=expected:raise AssertionError(('CONTENT_MISMATCH',relative,expected,got))
    n+=1
print('PASS_LOCAL_V2_MANIFEST',n,'files')

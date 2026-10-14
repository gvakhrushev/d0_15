#!/usr/bin/env python3
"""Verify the immutable Lean receipt for the fixed-carrier trace tangent."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
BASE = Path('02_REGISTRY/research/certificates/a4d_rank_volume_tangent')
RESULTS = Path(str(BASE) + '_lean_results.json')
SOURCE = Path(str(BASE) + '.lean')
OUTPUT = Path(str(BASE) + '_lean_output.txt')
THEOREM = 'D0.Research.RankVolumeTangent.idempotent_tangent_trace_zero'


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main():
    result = json.loads((ROOT / RESULTS).read_text())
    source = (ROOT / SOURCE).read_text()
    output = (ROOT / OUTPUT).read_text()
    assert result['status'] == 'PASS' and result['compiler_exit_code'] == 0
    assert result['source_sha256'] == sha(SOURCE)
    assert result['output_sha256'] == sha(OUTPUT)
    assert result['theorem'] == THEOREM
    assert f'#print axioms idempotent_tangent_trace_zero' in source
    assert 'sorry' not in source
    actual = re.search(r"'" + re.escape(THEOREM) + r"' depends on axioms: \[([^\]]*)\]", output)
    assert actual, 'Lean output lacks the theorem axiom report'
    axioms = [item.strip() for item in actual.group(1).split(',') if item.strip()]
    assert axioms == result['axioms']
    assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
    print('PASS_RANK_VOLUME_TANGENT theorem=%s axioms=%d' % (THEOREM, len(axioms)))


if __name__ == '__main__':
    main()

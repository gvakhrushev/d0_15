#!/usr/bin/env python3
"""Execute four changed source programs; never rewrite committed evidence."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

P = Path(__file__).resolve().parent
MUTATIONS = [
    ('erase_logical_term', 'D.T*J[r]*D,', '2*(G*h)[r]*s.eye(4),', 'full_source_pullback_0'),
    ('drop_one_syndrome', 'W=s.Matrix.hstack(*VV)', 'VV[3]=s.zeros(16,4)\n    W=s.Matrix.hstack(*VV)', 'full_sixteen_dimensional_decoder_unitary'),
    ('freeze_encoding_normalizer', '-V0*(t0/(1+t0*t0))', '', 'moving_source_encoding_full_normalizer'),
    ('amplitude_recurrence_for_density', '*(tt*tt-2*(2*rr*rr-1)*tt+1)', '*tt**2', 'five_state_density_recurrence'),
]


def run():
    path = P / 'check_memory_source_code.py'
    text = path.read_text(encoding='utf-8')
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = json.loads((P / 'validation.json').read_text(encoding='utf-8'))
    if before != expected['source_sha256']:
        raise ArithmeticError('source differs from validated packet')
    results = []
    with tempfile.TemporaryDirectory(prefix='d0-memory-code-mutants-') as tmp:
        for label, old, new, failure in MUTATIONS:
            if text.count(old) != 1:
                raise ValueError('nonunique mutation: ' + label)
            changed = Path(tmp) / (label + '.py')
            changed.write_text(text.replace(old, new), encoding='utf-8')
            proc = subprocess.run([sys.executable, str(changed)], capture_output=True,
                                  text=True, timeout=150, check=False)
            if proc.returncode == 0 or 'ArithmeticError: ' + failure not in proc.stderr:
                raise ArithmeticError('unexpected mutation result: ' + label + '\n' + proc.stderr)
            results.append({'mutation': label, 'failed_at': failure,
                            'result': 'REJECTED_MATHEMATICALLY', 'actual_program_changed': True})
    if hashlib.sha256(path.read_bytes()).hexdigest() != before:
        raise ArithmeticError('original source was changed')
    if results != expected['mutations']:
        raise ArithmeticError('mutations differ from committed validation')
    return {'mutations': results, 'source_unchanged': True, 'expected_evidence_rewritten': False}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))

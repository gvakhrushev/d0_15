#!/usr/bin/env python3
"""Changed finite calculations; immutable source and receipts stay untouched."""
from pathlib import Path
import hashlib
import json

HELPER = Path(__file__).with_name('check_gauge_span.py')
PIN = '6ce1983a9b437dba3d49c30f290d934f9b0caa3a6cac54f758fb11fd33cfd8c5'
CHANGES = (
    ('wrong_LC_covector_sign', 'actual = [C[r]*lift(-Gamma[r].T) for r in range(4)]',
     'actual = [C[r]*lift(Gamma[r].T) for r in range(4)]',
     'gauge_has_only_named_offdiagonal_pair_0100'),
    ('drop_coefficient_one_outputs', 'for coefficient in range(2):',
     'for coefficient in range(1):', 'complete32_rows_have19_zero_and13_nonzero_baselines'),
    ('wrong_right_root_projector', 'R0 = [I+(b-1)*(I-n) for n in N]',
     'R0 = [I+(b-1)*n for n in N]', 'right_root_square_0'),
    ('nongauge_probe_called_gauge', '(qp, (E4[:, i]-E4[:, j])/s.sqrt(2))',
     '(qp, (E4[:, i]+E4[:, j])/s.sqrt(2))', 'genuine_gauge_tangency_012'),
)


def run():
    data = HELPER.read_bytes()
    if hashlib.sha256(data).hexdigest() != PIN:
        raise ArithmeticError('gauge_mutation_input_changed')
    source = data.decode()
    results = []
    for name, old, new, failure in CHANGES:
        if source.count(old) != 1:
            raise ArithmeticError('gauge_mutation_target_not_unique:' + name)
        scope = {'__file__': str(HELPER), '__name__': 'changed_gauge_calculation'}
        exec(compile(source.replace(old, new), str(HELPER) + ':' + name, 'exec'), scope)
        try:
            scope['run']()
        except ArithmeticError as error:
            if str(error) != 'gauge_span:' + failure:
                raise ArithmeticError('gauge_mutation_wrong_failure:' + name) from error
            results.append({'mutation': name, 'rejected_at': failure})
        else:
            raise ArithmeticError('gauge_mutation_survived:' + name)
    return {'status': 'PASS', 'helper_sha256': PIN, 'rejected_mutations': results,
            'input_files_changed': False, 'old_run_entrypoints_executed': False}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))

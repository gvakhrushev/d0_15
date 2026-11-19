#!/usr/bin/env python3
"""Four changed calculations; never modify the frozen helper or its inputs."""
from pathlib import Path
import hashlib
import json

HELPER = Path(__file__).with_name('check_principal.py')
EXPECTED = '7f57f6e325defd8fda3e85667cf040f061ef8dba6a0897a127385ed8de49380d'
MUTATIONS = (
    ('wrong_connection_sign', 'M = [-g.T for g in connection]',
     'M = [g.T for g in connection]', 'actual_covector_LC_firstjet_0'),
    ('erase_label_coherence', 'detector = label_v*label_v.T',
     'detector = s.eye(3)/3', 'coherent_three_label_detector_is_projector'),
    ('wrong_coherent_normalization', 'jv = sum(chi_J, O.copy())/s.sqrt(3)',
     'jv = sum(chi_J, O.copy())/s.sqrt(2)',
     'coherent_detector_recovers_EH_principal_all_three_cones'),
    ('omit_second_golden_port',
     'actual_effect = port0.H*retained_projector*port0+port1.H*retained_projector*port1',
     'actual_effect = port0.H*retained_projector*port0',
     'two_actual_golden_ports_coherent_final_history_effect'),
)


def run():
    data = HELPER.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED:
        raise ArithmeticError('mutation_helper_input_changed')
    source = data.decode()
    results = []
    for label, old, new, expected_failure in MUTATIONS:
        if source.count(old) != 1:
            raise ArithmeticError('mutation_target_not_unique:' + label)
        namespace = {'__file__': str(HELPER), '__name__': 'changed_principal_calculation'}
        exec(compile(source.replace(old, new), str(HELPER) + ':' + label, 'exec'), namespace)
        try:
            namespace['run']()
        except ArithmeticError as error:
            if str(error) != 'causal_principal:' + expected_failure:
                raise ArithmeticError('unexpected_mutation_failure:' + label) from error
            results.append({'mutation': label, 'rejected_at': expected_failure})
        else:
            raise ArithmeticError('mutation_survived:' + label)
    return {'status': 'PASS', 'helper_sha256': EXPECTED, 'rejected_mutations': results,
            'old_entrypoints_executed': False, 'input_files_modified': False}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))

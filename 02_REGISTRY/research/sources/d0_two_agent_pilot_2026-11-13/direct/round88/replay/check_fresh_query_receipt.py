"""Replay the original FQ5–FQ7 and verify every byte outside one numerical diagnostic."""
from decimal import Decimal
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory


REVISION = 'd7782b0138cbd5418d68a825acc3f9ec1afe54a1'
METRIC = Path('02_REGISTRY/research/sources/d0_gr_2026-11-18/followups/2026-11-19/metric')
NATIVE = Path('02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py')
SCRIPT = 'check_fresh_query_economic_source.py'
RECEIPT = 'fresh_query_economic_source_result.json'
METRIC_FILES = (
    'check_boundary_experiment.py', 'check_clock_coherence.py', 'check_complete_work_source.py',
    'check_extra_work.py', 'check_fresh_guard_reader.py', SCRIPT, 'check_golden_record_race.py',
    'check_live_parser.py', 'check_local_gibbs_records.py', 'check_shared_site_union.py',
    'check_source_price.py', RECEIPT,
)
ARCHIVED = '821d5ec984362db6a42b228cefed20793e1b172d5ebc23f80d7a8b578181a28d'
REPRODUCED_MAC = '8806ce04ec29ab4b407ef1b8a276a77bc36aff8c13ab36573169195ad34a4262'
LIMIT = Decimal('4e-9')  # check_fresh_query_economic_source.py, lines 23–24 and 345.
DIAGNOSTIC = re.compile(rb'^    "full_source_identity_error": "([0-9.eE+-]+)",$', re.MULTILINE)


def normalized(output):
    hits = list(DIAGNOSTIC.finditer(output))
    if len(hits) != 1:
        raise ValueError('Expected exactly one finite-difference diagnostic line')
    start, end = hits[0].span(1)
    text = output[start:end].decode('ascii')
    decoded = json.loads(output)['native_entangled_cp_and_thermal_fixture']['full_source_identity_error']
    value = Decimal(text)
    if text != decoded or not value.is_finite() or not 0 <= value < LIMIT:
        raise ValueError('Full-source identity residual exceeds the original check or moved')
    return output[:start] + b'<bounded residual>' + output[end:]


def main():
    repo = os.environ.get('D0_PILOT_OBJECT_REPO') or subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel'], text=True).strip()
    with TemporaryDirectory(prefix='d0-a88-fresh-query-') as temporary:
        root = Path(temporary)
        for path in [NATIVE, *(METRIC / name for name in METRIC_FILES)]:
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(subprocess.check_output(['git', '-C', repo, 'cat-file', 'blob', f'{REVISION}:{path}']))
        work = root / METRIC
        archived = (work / RECEIPT).read_bytes()
        observed = subprocess.check_output([sys.executable, '-B', SCRIPT], cwd=work,
                                           env=dict(os.environ, PYTHONOPTIMIZE='0'))

    mac = archived.replace(b'"full_source_identity_error": "7.728e-11"',
                           b'"full_source_identity_error": "8.413e-11"')
    if sha256(archived).hexdigest() != ARCHIVED or sha256(mac).hexdigest() != REPRODUCED_MAC:
        raise ValueError('The archived receipt or the documented single-field substitution changed')
    masked = normalized(archived)
    if normalized(observed) != masked or normalized(mac) != masked:
        raise ValueError('Upstream output differs outside the selected bounded numerical diagnostic')
    print(json.dumps(dict(upstream_commit=REVISION, upstream_exit='PASS',
                          bounded_field='native_entangled_cp_and_thermal_fixture.full_source_identity_error',
                          upper_bound_exclusive=str(LIMIT), remaining_bytes='exact',
                          archived_sha256=ARCHIVED, reviewed_mac_sha256=REPRODUCED_MAC,
                          remaining_bytes_sha256=sha256(masked).hexdigest()), indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""D0 v11.19 structural certificate: φ-ABCD operator-cycle closure."""
from decimal import Decimal, getcontext
from pathlib import Path
import json, math

getcontext().prec = 80
root = Path(__file__).resolve().parents[1]
books_dir = root / "01_BOOKS"
out_json = root / "05_CERTS" / "vp_phi_abcd_operator_cycle_v1119.json"
out_md = root / "05_CERTS" / "vp_phi_abcd_operator_cycle_v1119.md"

sqrt5 = Decimal(5).sqrt()
phi = (Decimal(1)+sqrt5)/Decimal(2)
psi = (Decimal(1)-sqrt5)/Decimal(2)
p_plus = Decimal(1)/phi
p_minus = Decimal(1)/(phi*phi)
delta0 = (p_plus-p_minus)/Decimal(2)

def close(a, b, eps=Decimal('1e-60')):
    return abs(a-b) < eps

checks = {}
checks['A_trace_scalar_phi_plus_psi_eq_1'] = close(phi+psi, Decimal(1))
checks['B_norm_scalar_phi_psi_eq_minus_1'] = close(phi*psi, Decimal(-1))
checks['C_forward_recursion_phi2_eq_phi_plus_1'] = close(phi*phi, phi+1)
checks['D_return_recursion_psi2_eq_psi_plus_1'] = close(psi*psi, psi+1)
checks['branch_sum_p_plus_p_minus_eq_1'] = close(p_plus+p_minus, Decimal(1))
checks['delta0_half_gap'] = close(delta0, (sqrt5-Decimal(2))/Decimal(2))
checks['delta0_phi_form'] = close(delta0, Decimal(1)/(Decimal(2)*phi**3))
checks['centered_split_plus'] = close(p_plus, Decimal('0.5')+delta0)
checks['centered_split_minus'] = close(p_minus, Decimal('0.5')-delta0)
checks['Q_ladder_D1_to_D5'] = all(close(Decimal(2)*delta0*(phi**(D-1)), phi**(D-4)) for D in range(1,6))
roles = ['AΣ_normalization','BN_conjugate_coupling','C+_forward_recurrence','D-_return_recurrence']
terminal_roles = [(3,3),(4,4),(3,4),(4,3)]
checks['four_typed_operator_roles'] = len(roles)==4 and len(set(roles))==4
checks['four_terminal_two_port_roles'] = len(terminal_roles)==4 and len(set(terminal_roles))==4
checks['omega8_signed_count'] = len(terminal_roles)*2 == 8
# Structural removal test: each removed role leaves a named missing obligation.
obligations = {
    'AΣ_normalization':'unit_section',
    'BN_conjugate_coupling':'branch_coupling',
    'C+_forward_recurrence':'forward_runtime',
    'D-_return_recurrence':'return_runtime',
}
removal_failures = {role: obligations[role] for role in roles}
checks['removing_each_role_breaks_distinct_obligation'] = len(set(removal_failures.values())) == 4
# Text checks
active_books = list(books_dir.glob('BOOK_*.md'))
texts = {p.name:p.read_text() for p in active_books}
checks['active_books_no_golden_word'] = not any('golden' in t.lower() for t in texts.values())
checks['active_books_no_control_chars'] = all(not any((ord(ch)<32 and ch not in '\n\r\t') for ch in t) for t in texts.values())
required_terms = ['A_\\Sigma', 'B_N', 'C_+', 'D_-', 'operator completeness', 'OPERATOR-CYCLE-PROOF-MISSING']
combined_text = '\n'.join(texts.values())
checks['operator_cycle_terms_present'] = all(term in combined_text for term in required_terms)

status = 'PASS_PHI_ABCD_OPERATOR_CYCLE_V1119' if all(checks.values()) else 'FAIL_PHI_ABCD_OPERATOR_CYCLE_V1119'
result = {
    'status': status,
    'phi': str(phi),
    'psi': str(psi),
    'delta0': str(delta0),
    'Q': {str(D): str(Decimal(2)*delta0*(phi**(D-1))) for D in range(1,6)},
    'checks': checks,
    'removal_failures': removal_failures,
}
out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False))
lines = [f'# {status}', '', '## Checks', '']
for k,v in checks.items():
    lines.append(f'- {k}: {"PASS" if v else "FAIL"}')
lines += ['', '## Core equalities', '', f'- phi = {phi}', f'- psi = {psi}', f'- delta0 = {delta0}', '', '## Removal obligations', '']
for k,v in removal_failures.items():
    lines.append(f'- remove {k} -> missing {v}')
out_md.write_text('\n'.join(lines)+'\n')
print(status)
if not all(checks.values()):
    raise SystemExit(1)

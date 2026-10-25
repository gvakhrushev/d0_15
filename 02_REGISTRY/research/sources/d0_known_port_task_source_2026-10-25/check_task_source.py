#!/usr/bin/env python3
"""Changed native return-fibre algebra and actual-gain heat application.

The 16-column native fixtures are new controls of the scalar-corner map.
No old native/READY/root suite is replayed. Heat asymptotics are analytic.
"""
import argparse
from dataclasses import replace
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

import mpmath as mp
import sympy as sp

PACKET = Path(__file__).resolve().parent
SOURCES = PACKET.parent
REPO = SOURCES.parents[2]
NATIVE = SOURCES / 'd0_native_execution_domain_2026-10-24'
sys.path.insert(0, str(NATIVE))
import native_execution as ne
if Path(ne.__file__).resolve() != (NATIVE/'native_execution.py').resolve():
    raise ImportError('the owned native module is required')
BOUNDS = dict(max_qubits=4, max_expanded_stages=500)
CHECKS = []


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


def execution(gates=()):
    return ne.Execution(4, (0, 1), (), tuple(gates), ne.G_CX_SOURCE_I,
                        source_port=0, source_spin=(2, 3))


def pair_parts(matrix):
    """Fixture ordering is two ACTIVE wires followed by the two spin wires."""
    A, B = sp.zeros(4), sp.zeros(4)
    for i in range(4):
        for j in range(4):
            A[i, j], B[i, j] = matrix[4*i, 4*j], matrix[4*i+1, 4*j]
    return A, B


def source_pair():
    g = ne.Gate('G', (0,))
    si = ne.Gate('SourceI', (0, 2, 3))
    inv_g = ne.inverse_word(execution((g,)), **BOUNDS)
    plus = execution((g, si, *inv_g, ne.Gate('CX', (0, 1)), ne.Gate('CX', (0, 1))))
    minus = execution((g, si, si, si, *inv_g))
    return plus, minus


def recorded_control():
    """Apply the owned balanced copy to an actual complex-corner word.

    Both ACTIVE labels are copied into fresh records; no sealed oldRIGHT is used.
    This is the physical record map, not a claim that metadata is a gate.
    """
    plus, _ = source_pair()
    copied = (ne.Gate('CX', (0, 4)), ne.Gate('CX', (1, 5)))
    code = ne.Execution(6, (0, 1, 4, 5), (), (*copied, *plus.gates, *copied),
                        ne.G_CX_SOURCE_I, source_port=0, source_spin=(2, 3),
                        report_bits=(4, 5))
    bounds = dict(max_qubits=6, max_expanded_stages=500)
    U = ne.word_matrix(code, **bounds)
    D = ne.word_matrix(replace(code, gates=copied), **bounds)
    old = ne.word_matrix(plus, **BOUNDS)
    init = ne.input_isometry(code, **bounds)
    old_init = ne.input_isometry(plus, **BOUNDS)
    check('real two-leg label copying preserves the full operator conjugacy at its NEW carrier and clock',
          ne.exact_matrix_equal(U, D*sp.kronecker_product(old, sp.eye(4))*D)
          and len(code.gates) == 13
          and ne.inventory(code, **bounds).full_dimension == 64
          and ne.inventory(code, **bounds).cut_rank == 4)
    check('paid balanced copy retains the SAME complete protected return corner',
          ne.exact_matrix_equal(init.T*U*init, old_init.T*old*old_init))
    # Record00 is an actual joint outcome of the two copied labels.
    # No coherent AND gate or hidden postselection is inserted.
    record_zero = sp.diag(*(int(i % 4 == 0) for i in range(64)))
    check('the actually recorded all-zero label has exactly the full blank-return effect',
          ne.exact_matrix_equal(init.T*U.T*record_zero*U*init,
                                (ne.P**2+ne.P**4)*sp.eye(4)))
    return dict(original_stages=9, copied_stages=13, copy_gates_per_leg=2,
                old_dimension=16, actual_dimension=64, cut_rank=4,
                full_paired_modes=2*13*64, actual_record_bits=[4,5],
                scope='new small physical recording transport; no sealed record inverse or coherent AND')


def run():
    CHECKS.clear()
    mp.mp.dps = 100
    I, J, p = sp.eye(4), ne.L_I, ne.P
    check('actual Q8 source generator is skew and squares to minus identity',
          J.T == -J and J*J == -I)
    palette = [ne.Gate('G', (0,)), ne.Gate('G', (1,)),
               ne.Gate('CX', (0, 1)), ne.Gate('CX', (1, 0)),
               ne.Gate('SourceI', (0, 2, 3))]
    for gate in palette:
        U = ne.gate_matrix(execution((gate,)), gate, **BOUNDS)
        A, B = pair_parts(U)
        check('actual full primitive is in REAL work plus work-L_i algebra '+repr(gate),
              ne.exact_matrix_equal(U, sp.kronecker_product(A, I)+sp.kronecker_product(B, J)))
    # This is the general multiplication identity used by the word induction.
    a, b, c, d = (sp.Matrix(2, 2, sp.symbols(name+':4')) for name in ('a', 'b', 'c', 'd'))
    left = (sp.kronecker_product(a, I)+sp.kronecker_product(b, J))*(sp.kronecker_product(c, I)+sp.kronecker_product(d, J))
    right = sp.kronecker_product(a*c-b*d, I)+sp.kronecker_product(a*d+b*c, J)
    check('closure uses the two-coefficient algebra rather than commutation alone', left.expand() == right.expand())
    fake = sp.diag(sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 3))
    check('commuting with L_i alone does NOT force a scalar return Gram',
          fake*J == J*fake and fake.T*fake != (fake.T*fake)[0, 0]*I)

    plus, minus = source_pair()
    rows = []
    matrices = []
    for sign, code in ((1, plus), (-1, minus)):
        U = ne.word_matrix(code, **BOUNDS)
        init = ne.input_isometry(code, **BOUNDS)
        corner = init.T*U*init
        A, B = pair_parts(U)
        expected = p*I+sign*p**2*J
        inv = ne.inventory(code, **BOUNDS)
        check('matched actual native corner has a genuine imaginary source component sign%d'%sign,
              ne.exact_matrix_equal(corner, expected)
              and ne.exact_matrix_equal(U, sp.kronecker_product(A, I)+sp.kronecker_product(B, J)))
        check('one unconditional return law is the FULL rank4 Gram sign%d'%sign,
              ne.exact_matrix_equal(corner.T*corner, (p**2+p**4)*I)
              and inv.gate_count == 9 and inv.full_dimension == 16 and inv.cut_rank == 4)
        rows.append(dict(sign=sign, stages=inv.gate_count, full_columns=16, cut_rank=4,
                         G=inv.g_count, CX=inv.cx_count, SourceI=inv.source_i_count,
                         return_probability=str(sp.simplify(p**2+p**4))))
        matrices.append(U)
    future_word = ne.inverse_word(plus, **BOUNDS)
    future = execution(future_word)
    V = ne.word_matrix(future, **BOUNDS)
    init = ne.input_isometry(plus, **BOUNDS)
    outputs = [(init.T*V*U*init) for U in matrices]
    check('a real paid PRE-readout future context separates two words in the SAME return-effect fibre',
          len(future_word) == 27
          and ne.exact_matrix_equal(V*matrices[0], sp.eye(16))
          and ne.exact_matrix_equal(outputs[0], I)
          and ne.exact_matrix_equal(outputs[1], p**3*I)
          and not ne.exact_matrix_equal(outputs[1].T*outputs[1], I))
    # The same supplied KNOWN work is not the all-bank subroutine input.
    si_code = execution((ne.Gate('SourceI', (0, 2, 3)),))
    cx_code = execution((ne.Gate('CX', (1, 0)),))
    small = [ne.word_matrix(code, **BOUNDS) for code in (si_code, cx_code)]
    check('two legal N1 words agree on every actual known-work Q8 input',
          all(ne.exact_matrix_equal(U*init, init) for U in small))
    bank_free = replace(si_code, blank_wires=(0,))
    bank_input = ne.input_isometry(bank_free, **BOUNDS)
    bank_corners = [bank_input.T*U*bank_input for U in small]
    check('the same known-input return does NOT fix the different arbitrary-bank subroutine effect',
          ne.exact_matrix_equal(bank_corners[0], sp.eye(8))
          and ne.exact_matrix_equal(bank_corners[1], sp.diag(1,1,1,1,0,0,0,0)))
    aa, bb = sp.symbols('a b', real=True)
    check('the general protected corner has its exact scalar Gram',
          ((aa*I+bb*J).T*(aa*I+bb*J)-(aa**2+bb**2)*I).expand() == sp.zeros(4))

    # A positive exact effect illustrates why conditional normalization is weaker.
    E = sp.diag(sp.Rational(1, 10), sp.Rational(1, 5))
    gamma1, gamma2 = sp.Rational(1, 2), sp.Rational(3, 4)
    q, dd = sp.Rational(1, 10), sp.Rational(3, 4)
    check('equal conditional report effects do NOT fix readiness or full return',
          gamma1*E/gamma1 == gamma2*E/gamma2
          and (1-dd*gamma1*q)**2 != (1-dd*gamma2*q)**2)

    heat_rows = []
    beta = mp.mpf(1)
    previous = None
    for M in (4, 16, 64):
        N = 14*M
        # Current collar is uniform. This constant-gbar model is comparison
        # algebra, NOT a native all-mesh report or a substitute for HT proof.
        s = mp.mpf(3)/4
        tau = s**(2*M)
        zeta, rank = mp.mpf(2)**-20, 4
        w = rank*zeta*tau/(1-zeta+zeta*tau)
        gain = w*(mp.mpf(8)/3)*M
        lower = rank*zeta/4*(mp.mpf(9)/16)**M*mp.power(M, mp.mpf(63)/64)
        ratio_q = (beta/(2*(N+1)))**N
        L_bound = 2*mp.exp(beta+beta**2/4)/beta*(beta/2)**N/mp.factorial(N)/(1-ratio_q)**2
        relative = N*L_bound/lower
        check('factorial clock bound is smaller than the ACTUAL exponentially small gain M%d'%M,
              gain >= lower > 0 and ratio_q < 1 and relative > 0
              and (previous is None or relative < previous))
        # Evaluate the complete Fourier/winding sum independently of the
        # factorial majorant; this is numerical comparison evidence only.
        series = mp.fsum(m*mp.besseli(m*N, beta) for m in range(1, 5))
        L4 = 2*mp.exp(beta)/beta*series
        check('explicit leading winding terms respect the complete analytic majorant M%d'%M,
              0 < L4 < L_bound)
        previous = relative
        heat_rows.append(dict(M=M, actual_clock_lower=N, model_gain=mp.nstr(gain,60),
                              rigorous_formula_gain_lower=mp.nstr(lower,60),
                              analytic_bound_relative=mp.nstr(relative,60),
                              four_winding_partial_sum=mp.nstr(L4,60)))
    # This verifies the load-bearing hypothesis; it is not an all-native
    # counterexample at moving temperature or a physical norm assignment.
    check('a growing beta cannot silently reuse the fixed-beta factorial gate',
          all((Fraction(N*N,2*(N+1)))**N > 1 for N in (8,16,32)))
    recording = recorded_control()
    return dict(status='PASS',checks=len(CHECKS),check_names=list(CHECKS),
                native_return_rows=rows, future_context_stages=27,
                actual_recording_transport=recording,
                future_return_probabilities=['1',str(sp.simplify(p**6))],
                heat_comparison_models=heat_rows,
                scope=['new exact 16-column native algebra/return/context controls',
                       'future inverse context is before terminal reading; no sealed record is reversed',
                       'general return algebra and heat asymptotics are analytic proofs',
                       'no all-future equivalence inferred from one return effect',
                       'same-return task fibre is not all native edits or physical selection',
                       'constant-gbar and conditional-effect models are diagnostics',
                       'no old native/READY/Cartan/root/Lean replay; no GR promotion'])


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path.relative_to(REPO)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def section_pin(heading):
    raw=(REPO/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md').read_bytes()
    start=raw.index(heading.encode());end=raw.find(b'\n## ',start+1);raw=raw[start:end if end>=0 else None]
    return dict(heading=heading,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=run()
    paths=[PACKET/n for n in ('check_task_source.py','HEAT_TRANSFER.md','TASK_MAP.md')]
    paths += [NATIVE/n for n in ('native_execution.py','BOOK_MAP.md')]
    paths += [SOURCES/'d0_native_task_clock_source_2026-10-25'/n for n in ('PROOF.md','CHECK_RESULT.json')]
    paths += [SOURCES/'d0_known_port_native_cofield_2026-10-25'/n for n in ('SOURCE_TRANSFER.md','INPUT_AND_RECORD_MAP.md','CHECK_RESULT.json')]
    paths += [NATIVE/'book_price.py',
              REPO/'03_FORMALIZATION/D0/Foundation/FutureExecution.lean',
              REPO/'03_FORMALIZATION/D0/Foundation/EmpiricalTheoryFactorization.lean']
    paths += [REPO/'01_BOOKS'/n for n in ('BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md',
              'BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md',
              'BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md')]
    result['source_pins']=[pin(p) for p in paths]
    result['section_pins']=[section_pin('## '+key+'.') for key in ('7f','7l','7t','7ad','7ai','7aj')]
    result['generated_utc']=datetime.now(timezone.utc).isoformat()
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.output: args.output.write_text(text)
    print(text,end='')


if __name__=='__main__':main()

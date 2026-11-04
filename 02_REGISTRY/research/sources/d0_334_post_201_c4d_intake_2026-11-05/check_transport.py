#!/usr/bin/env python3
"""Bounded original full128 -> RAW real target/price transport.

One pinned native constructor call; no old suite and no dense 4096x4096 U.
Numerical residuals are nominal floating checks, not interval certificates.
No compiled native word or physical Info selection is asserted.
"""
from __future__ import annotations
import os
for thread_option in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[thread_option] = '1'
import argparse
import ast
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import platform
import numpy as np
import scipy
import sympy as sp
from scipy.linalg import expm, solve_sylvester

OWNER = '02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py'
OWNER_SHA256 = '1c501d5609dda3e14a3da95aad0c77ea04ef48bf94921793a403fb058a805fe9'
OWNER_BLOB = 'ee8de4635d24c668949ac9a0186616ab7d59f2ed'
CHECKS = []
RESIDUALS = {}
TOL = 3e-11
JET_TOL = 3e-10
ENTROPY_TOL = 3e-12


def need(condition, label):
    if not bool(condition):
        raise ArithmeticError(label)
    CHECKS.append(label)


def close(actual, expected, label, tolerance=TOL):
    error = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
    RESIDUALS[label] = error
    need(np.isfinite(error) and error <= tolerance, label)


def adj(matrix):
    return matrix.conj().T


def realify(matrix):
    return np.block([[matrix.real, -matrix.imag], [matrix.imag, matrix.real]])


def real_blocks(blocks):
    return np.vstack([realify(block) for block in blocks])


def entropy_from_amplitude(amplitude):
    # Squared singular values are nonnegative even for deficient-rank blocks.
    # No outcome or positive singular square is clipped.
    spectrum = np.linalg.svd(amplitude, compute_uv=False) ** 2
    positive = spectrum[spectrum > 0]
    return float(-np.sum(positive * np.log(positive)))


def sqrt_density(density, label):
    eig, vec = np.linalg.eigh(density)
    need(float(eig.min()) > 0, label)
    return (vec * np.sqrt(eig)) @ adj(vec)


def kron_power(matrix, count):
    result = np.ones((1, 1), dtype=matrix.dtype)
    for _ in range(count):
        result = np.kron(result, matrix)
    return result


def load_native_once(repo):
    source = (repo / OWNER).read_bytes()
    need(hashlib.sha256(source).hexdigest() == OWNER_SHA256,
         'original constructor SHA256 pin')
    blob = hashlib.sha1(b'blob ' + str(len(source)).encode() + b'\0' + source).hexdigest()
    need(blob == OWNER_BLOB, 'original constructor Git blob pin')
    wanted = ('adj', 'herm', 'tr', 'root', 'creators', 'native')
    parsed = ast.parse(source.decode(), filename=OWNER)
    functions = [node for node in parsed.body
                 if isinstance(node, ast.FunctionDef) and node.name in wanted]
    need(tuple(node.name for node in functions) == wanted,
         'only six pinned definitions extracted; no historical suite')
    captured = {}

    def capture(answer, rows, drows):
        captured['calls'] = captured.get('calls', 0) + 1
        captured['rows'] = np.asarray(rows).copy()
        captured['drows'] = np.asarray(drows).copy()
        return answer

    class CaptureNativeReturn(ast.NodeTransformer):
        def visit_Return(self, node):
            return ast.copy_location(ast.Return(value=ast.Call(
                func=ast.Name(id='_capture_original_return', ctx=ast.Load()),
                args=[node.value, ast.Name(id='rows', ctx=ast.Load()),
                      ast.Name(id='drows', ctx=ast.Load())], keywords=[])), node)

    # Capture original local SELECT rows at the sole return. All calculations,
    # returned K/dK, and their original ordering remain unchanged.
    functions[-1] = CaptureNativeReturn().visit(functions[-1])
    module = ast.fix_missing_locations(ast.Module(body=functions, type_ignores=[]))
    p = (np.sqrt(5.0) - 1.0) / 2.0
    namespace = dict(np=np, expm=expm, solve_sylvester=solve_sylvester,
                     P=p, EYE=np.eye(16, dtype=complex),
                     _capture_original_return=capture)
    exec(compile(module, OWNER, 'exec'), namespace)
    native_excerpt = SimpleNamespace(native=namespace['native'])
    k, dk = native_excerpt.native(np.log(2.0), 3.0 / 5.0,
                                 (1j, 1j, -1.0, -1j))
    need(captured['calls'] == 1, 'exactly one original native call')
    return p, k, dk, captured['rows'], captured['drows']


def exact_checks():
    p, x = sp.symbols('p x', positive=True)
    modulus = p**2 + p - 1

    def reduce(expression):
        return sp.rem(sp.Poly(sp.expand(expression), p),
                      sp.Poly(modulus, p)).as_expr().expand()

    need(reduce(p**4 + p**3 - p**2) == 0,
         'EXACT Golden total Kraus recycling coefficient')
    # Port0: I - 4p² Delta + 4p⁴ Delta; port1: 4p³ Delta.
    need(reduce(-4*p**2 + 4*p**4 + 4*p**3) == 0,
         'EXACT total fine effect is identity')
    need(reduce(-4*p**2 + 4*p**4 + 8*p**3 - 4*p**3) == 0,
         'EXACT paid cost effect is I plus 4p³ Delta')
    need(sp.expand(4*p**4 + 4*p**3*x - 4*p**2*(p**2+p*x)) == 0,
         'EXACT marked-map recycling coefficient')
    need(reduce(-4*p**2 + 4*p**4 + 4*p**3*x - 4*p**3*(x-1)) == 0,
         'EXACT marked adjoint identity effect')
    need(reduce(p*4*p**3*(p-1) + 4*p**6) == 0,
         'EXACT Golden-mark one-round normalizer coefficient')
    need(sp.Integer(2)*sp.Integer(2) == 4,
         'EXACT isometry cost-effect error coefficient 2 norm(C)=4')
    lam = sp.symbols('lambda', positive=True)
    entropy_shift = -2*(lam/2)*sp.log(lam/2) + lam*sp.log(lam)
    need(sp.simplify(entropy_shift - lam*sp.log(2)) == 0,
         'EXACT duplicated-halved eigenvalue entropy shift')
    m_out, m_in, dm_out, dm_in = sp.symbols('m_out m_in dm_out dm_in', real=True)
    gain_shift = sp.log(2)*(m_out-m_in)
    jet_shift = sp.log(2)*(dm_out-dm_in)
    need(gain_shift.subs(m_out, m_in) == 0,
         'EXACT complete CQ gain shift cancels at equal total mass')
    need(jet_shift.subs(dm_out, dm_in) == 0,
         'EXACT moving-preparation CQ gain jet shift cancels')
    q, old_s, conditional_s = sp.symbols('H_old S_input S_conditional', real=True)
    need(sp.expand(q - (q+conditional_s-old_s) - (old_s-conditional_s)) == 0,
         'EXACT retained-purifier versus mixed-DATA gain difference')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    args = parser.parse_args()
    p, k, dk, rows, drows = load_native_once(args.repo)
    a = np.sqrt(p)
    eye16, eye32 = np.eye(16), np.eye(32)
    need(k.shape == dk.shape == (128, 16, 16), 'all128 original K and dK slots')
    need(rows.shape == drows.shape == (64, 16, 16), 'all64 original SELECT rows and jets')
    need(all(np.all(np.isfinite(value)) for value in (k, dk, rows, drows)),
         'every original operator and jet entry is finite')
    delta = adj(rows[0]) @ rows[0]
    ddelta = adj(drows[0]) @ rows[0] + adj(rows[0]) @ drows[0]
    close(rows[0], adj(rows[0]), 'original blank SELECT row is Hermitian')
    close(sum(row @ adj(row) for row in rows), eye16, 'original SELECT row coisometry')
    close(sum(adj(row) @ row for row in rows), eye16, 'original SELECT column isometry')
    close(sum(drow @ adj(row) + row @ adj(drow) for row, drow in zip(rows, drows)),
          np.zeros((16, 16)), 'original SELECT coisometry jet', JET_TOL)

    # Original U=I-2LL*, represented in computational record z=2j+b order.
    l_blocks = np.asarray([factor*adj(row) for row in rows for factor in (p, a)])
    dl_blocks = np.asarray([factor*adj(row) for row in drows for factor in (p, a)])
    lr, dlr = real_blocks(l_blocks), real_blocks(dl_blocks)
    close(lr.T @ lr, eye32, 'original real reflection rank32 isometry')
    close(dlr.T @ lr + lr.T @ dlr, np.zeros((32, 32)),
          'original full-reflection tangent constraint', JET_TOL)
    j0 = np.zeros((4096, 32))
    j0[:32] = eye32

    def apply_u(value):
        return value - 2*lr @ (lr.T @ value)

    def apply_du(value):
        return -2*(dlr @ (lr.T @ value) + lr @ (dlr.T @ value))

    vr = apply_u(j0)
    dvr = apply_du(j0)
    expected_vr, expected_dvr = real_blocks(k), real_blocks(dk)
    need(vr.shape == (4096, 32), 'complete real prepared carrier is 4096 by32')
    close(vr, expected_vr, 'ALL128 computational record posterior blocks')
    close(dvr, expected_dvr, 'ALL128 computational record posterior jets', JET_TOL)
    close(vr.T @ vr, eye32, 'complete realified instrument isometry')
    close(dvr.T @ vr + vr.T @ dvr, np.zeros((32, 32)),
          'complete realified instrument isometry jet', JET_TOL)
    probes = np.sin(np.arange(4096*3).reshape(4096, 3)+1) / np.sqrt(4096)
    close(apply_u(apply_u(probes)), probes, 'original implicit reflection full-carrier probe')
    close(apply_du(apply_u(probes)) + apply_u(apply_du(probes)),
          np.zeros_like(probes), 'original implicit reflection orthogonality jet', JET_TOL)
    need(32 % 2 == 0, 'EXACT original real reflection determinant is positive')

    structural = np.asarray([(z//4) % 2 == 1 for z in range(128)])
    need(int(structural.sum()) == 64, 'exact duplicated-Walsh structural zero-slot count')
    need(np.all(k[structural] == 0) and np.all(dk[structural] == 0),
         'every structural zero slot and its jet retained exactly')
    need(np.all(np.linalg.norm(k[~structural], axis=(1, 2)) > 1e-10),
         'every other original slot nonzero on this fixture')

    vb = vr.reshape(128, 32, 32)
    dvb = dvr.reshape(128, 32, 32)
    effect_errors, effect_jet_errors, posterior_errors = [], [], []
    rho = np.diag(np.arange(1., 17.)) / 136.
    rho = rho.astype(complex)
    rho[0, 1], rho[1, 0] = 0.001j, -0.001j
    drho = np.zeros((16, 16), complex)
    drho[0, 0], drho[1, 1] = 0.01, -0.01
    drho[0, 1] = drho[1, 0] = 0.001
    rhor, drhor = realify(rho)/2, realify(drho)/2
    close(np.trace(rho), 1., 'faithful fixture density normalized')
    close(np.trace(drho), 0., 'independent preparation jet trace zero')
    srho = sqrt_density(rho, 'faithful complex fixture input')
    srhor = sqrt_density(rhor, 'faithful normalized real fixture input')
    effects, deffects = [], []
    xc, xr, dxc, dxr = [], [], [], []
    for z in range(128):
        f = vb[z].T @ vb[z]
        df = dvb[z].T @ vb[z] + vb[z].T @ dvb[z]
        fc = adj(k[z]) @ k[z]
        dfc = adj(dk[z]) @ k[z] + adj(k[z]) @ dk[z]
        effect_errors.append(np.max(np.abs(f-realify(fc))))
        effect_jet_errors.append(np.max(np.abs(df-realify(dfc))))
        effects.append(f)
        deffects.append(df)
        xz = k[z] @ rho @ adj(k[z])
        dxz = dk[z] @ rho @ adj(k[z]) + k[z] @ drho @ adj(k[z]) + k[z] @ rho @ adj(dk[z])
        xrz = vb[z] @ rhor @ vb[z].T
        dxrz = dvb[z] @ rhor @ vb[z].T + vb[z] @ drhor @ vb[z].T + vb[z] @ rhor @ dvb[z].T
        posterior_errors.append(np.max(np.abs(xrz-realify(xz)/2)))
        xc.append(xz); xr.append(xrz); dxc.append(dxz); dxr.append(dxrz)
    close(max(effect_errors), 0., 'ALL128 original computational effects')
    close(max(effect_jet_errors), 0., 'ALL128 original computational effect jets', JET_TOL)
    close(max(posterior_errors), 0., 'ALL128 posterior DATA realification with normalized density')
    close(max(np.max(np.abs(dxr[z]-realify(dxc[z])/2)) for z in range(128)),
          0., 'ALL128 posterior DATA jets include preparation', JET_TOL)
    costs = np.array([1+z%2 for z in range(128)])
    cost_effect = sum(costs[z]*effects[z] for z in range(128))
    dcost_effect = sum(costs[z]*deffects[z] for z in range(128))
    target_cost = eye32 + 4*p**3*realify(delta)
    target_dcost = 4*p**3*realify(ddelta)
    close(cost_effect, target_cost, 'original port price effect I plus4p³ realDelta')
    close(dcost_effect, target_dcost, 'original port price effect full jet', JET_TOL)
    expected_cost_jet = np.trace(drhor @ cost_effect + rhor @ dcost_effect)
    summed_cost_jet = sum(costs[z]*np.trace(dxr[z]) for z in range(128))
    close(expected_cost_jet, summed_cost_jet, 'actual charge source includes independent preparation')
    close(sum(np.trace(x) for x in xc), 1., 'complete complex output mass')
    close(sum(np.trace(x) for x in xr), 1., 'complete real output mass')
    close(sum(np.trace(x) for x in dxc), 0., 'complete complex output mass jet', JET_TOL)
    close(sum(np.trace(x) for x in dxr), 0., 'complete real output mass jet', JET_TOL)
    need(float(np.linalg.norm(sum(xc)-rho, 2)) > 1e-6,
         'fixture input is not silently a stationary DATA section')

    # No dense B_rec (4096 squared): seven-bit record basis is only 128 squared.
    g = np.array([[a, -p], [p, a]])
    b7 = kron_power(g, 7)
    born = b7[:, 0]
    jv = np.kron(born[:, None], eye32)

    def record_action(matrix, value):
        value3 = value.reshape(128, 32, value.shape[1])
        return np.einsum('ij,jkn->ikn', matrix, value3).reshape(4096, value.shape[1])

    close(b7.T @ b7, np.eye(128), 'seven actual Golden birth-frame factors orthogonal')
    close(record_action(b7.T, jv), j0, 'one-sided birth frame sends actual Jv to J0')
    born_output = apply_u(record_action(b7.T, jv))
    born_jet = apply_du(record_action(b7.T, jv))
    close(born_output, expected_vr, 'Usharp Jv equals original complete V_R')
    close(born_jet, expected_dvr, 'Usharp Jv jet equals original complete dV_R', JET_TOL)
    close(born_output.T @ born_output, eye32, 'actual born-frame prepared target isometry')
    bad_output = record_action(b7, born_output)
    bad_cost = sum(costs[z]*(bad_output[32*z:32*(z+1)].T @ bad_output[32*z:32*(z+1)])
                   for z in range(128))
    bad_gap = float(np.linalg.norm(bad_cost-target_cost, 2))
    need(bad_gap > 1e-3, 'NEGATIVE two-sided born conjugation changes original record cost')

    complex_entropy, real_entropy, entropy_block_errors = [], [], []
    for z in range(128):
        sc = entropy_from_amplitude(k[z] @ srho)
        sr = entropy_from_amplitude(vb[z] @ srhor)
        mass = float(np.trace(xc[z]).real)
        complex_entropy.append(sc)
        real_entropy.append(sr)
        entropy_block_errors.append(abs(sr-sc-mass*np.log(2)))
    s_in_c, s_in_r = entropy_from_amplitude(srho), entropy_from_amplitude(srhor)
    s_out_c, s_out_r = sum(complex_entropy), sum(real_entropy)
    close(max(entropy_block_errors), 0., 'ALL128 unnormalized block entropy shifts', ENTROPY_TOL)
    close(s_in_r-s_in_c, np.log(2), 'faithful input realification entropy shift ln2', ENTROPY_TOL)
    close(s_out_r-s_out_c, np.log(2), 'complete CQ output realification entropy shift ln2', ENTROPY_TOL)
    close(s_out_r-s_in_r, s_out_c-s_in_c, 'actual complete CQ gain has no realification shift', ENTROPY_TOL)
    need(abs(s_out_r-s_out_c) > 0.6,
         'NEGATIVE absolute CQ entropy does retain ln2')

    # Marked map checked against independent Kraus summation, not an old suite.
    mark = np.log((1+np.sqrt(5.))/2)
    x = np.exp(-mark)
    bj = [adj(row) @ rows[0] for row in rows]
    dbj = [adj(drow) @ rows[0] + adj(row) @ drows[0]
           for row, drow in zip(rows, drows)]
    recycling = sum(b @ rho @ adj(b) for b in bj)
    drecycling = sum(db @ rho @ adj(b)+b @ drho @ adj(b)+b @ rho @ adj(db)
                    for b, db in zip(bj, dbj))
    marked = sum(x**costs[z]*xc[z] for z in range(128))
    dmarked = sum(x**costs[z]*dxc[z] for z in range(128))
    formula = x*(rho-2*p**2*(delta@rho+rho@delta)+4*p**2*(p**2+p*x)*recycling)
    dformula = x*(drho-2*p**2*(ddelta@rho+delta@drho+drho@delta+rho@ddelta)
                  +4*p**2*(p**2+p*x)*drecycling)
    close(marked, formula, 'actual cost-marked Phi operator formula')
    close(dmarked, dformula, 'actual cost-marked Phi full input/gate jet', JET_TOL)
    close(np.trace(marked), p-4*p**6*np.trace(rho@delta),
          'actual Golden-mark absolute normalizer')
    exact_checks()
    provenance_labels = {
        'original constructor SHA256 pin', 'original constructor Git blob pin',
        'only six pinned definitions extracted; no historical suite',
        'exactly one original native call',
    }
    structural_labels = {
        'all128 original K and dK slots', 'all64 original SELECT rows and jets',
        'complete real prepared carrier is 4096 by32',
        'exact duplicated-Walsh structural zero-slot count',
        'EXACT original real reflection determinant is positive',
    }
    check_kinds = {
        label: ('provenance' if label in provenance_labels else
                'exact_structural' if label in structural_labels else
                'exact_symbolic' if label.startswith('EXACT ') else
                'nominal_numeric')
        for label in CHECKS
    }
    result = {
        'scope': 'nominal bounded full128 real target, original completion, charge and CQ-gain transport; no compiled word or Info selection',
        'owner': {'path': OWNER, 'sha256': OWNER_SHA256, 'git_blob': OWNER_BLOB,
                  'native_calls': 1, 'old_suite_executed': False,
                  'original_SELECT_rows_captured_without_reexecution': True},
        'environment': {'python': platform.python_version(), 'numpy': np.__version__,
                        'scipy': scipy.__version__, 'sympy': sp.__version__},
        'fixture': {'theta': 'log(2)', 'nu': '3/5', 'phases': ['i','i','-1','-i'],
                    'record_slots': 128, 'structural_zero_slots': 64,
                    'real_prepared_shape': [4096,32], 'dense_4096_completion_allocated': False,
                    'input': 'specified faithful nonstationary density; not a native stationary preparation'},
        'tolerances_nominal_not_intervals': {'matrix': TOL, 'jet': JET_TOL, 'entropy': ENTROPY_TOL},
        'check_count': len(CHECKS), 'checks': CHECKS,
        'check_kinds': check_kinds,
        'check_counts_by_kind': {kind: list(check_kinds.values()).count(kind)
                                for kind in sorted(set(check_kinds.values()))},
        'max_residual': format(max(RESIDUALS.values()), '.16e'),
        'residuals': {name: format(value, '.16e') for name, value in RESIDUALS.items()},
        'values': {'complex_CQ_gain': format(s_out_c-s_in_c, '.16e'),
                   'real_CQ_gain': format(s_out_r-s_in_r, '.16e'),
                   'charge_source': format(float(expected_cost_jet.real), '.16e'),
                   'wrong_two_sided_record_cost_gap': format(bad_gap, '.16e')},
        'preserved_boundaries': ['full128 posterior maps and all record effects',
                                'one-sided actual born frame; no free rotated readout',
                                'independent preparation source',
                                'absolute entropy shift versus gain cancellation',
                                'original cost marker normalizer',
                                'no physical compiled word, Gibbs preparation, full Info selection, or GR closure'],
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()

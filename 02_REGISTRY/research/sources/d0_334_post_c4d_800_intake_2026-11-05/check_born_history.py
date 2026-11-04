#!/usr/bin/env python3
"""One pinned full128 call, actual born input, two full fine histories.

Numerics are nominal, never intervals. The smooth output controls are an
explicit comparison family, not a claimed continuously adjustable native gate.
No compiled-word cost or physically selected Info is supplied by this checker.
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
import platform
from types import SimpleNamespace
import numpy as np
import scipy
import sympy as sp
from scipy.linalg import expm, solve_sylvester

OWNER = '02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py'
OWNER_SHA256 = '1c501d5609dda3e14a3da95aad0c77ea04ef48bf94921793a403fb058a805fe9'
OWNER_BLOB = 'ee8de4635d24c668949ac9a0186616ab7d59f2ed'
PREDECESSOR_SHA256 = 'cf48fa4229eb610c47e6a9dae6730ea417701b9d7a40ed4d27a0aa6ff3edb80c'
PRIMARY = '02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
TOL = 4e-11
JET_TOL = 4e-10
CHECKS = []
RESIDUALS = {}


def need(condition, label, kind='structural'):
    if not bool(condition):
        raise ArithmeticError(label)
    if label in ('original constructor SHA256 pin', 'original constructor Git blob pin'):
        kind = 'provenance'
    CHECKS.append({'label': label, 'kind': kind})


def close(actual, expected, label, tolerance=TOL):
    error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
    RESIDUALS[label] = error
    need(np.isfinite(error) and error <= tolerance, label, 'nominal_numeric')


def adj(matrix):
    return matrix.conj().T


def realify(matrix):
    return np.block([[matrix.real, -matrix.imag], [matrix.imag, matrix.real]])


def tensor_power(value, count):
    result = np.ones(1)
    for _ in range(count):
        result = np.kron(result, value)
    return result


def pinned_loader(repo):
    previous = PRIMARY+':7fh.G1/check_transport.py'
    primary = (repo/PRIMARY).read_text()
    sections = primary.split('#### 7fh.G1. check_transport.py\n')
    opening = '\n```python\n'
    need(len(sections) == 2 and sections[1].startswith(opening),
         'unique published 7fh.G1 Python block in repository primary', 'provenance')
    source = (sections[1][len(opening):].split('\n```', 1)[0]+'\n').encode()
    need(hashlib.sha256(source).hexdigest() == PREDECESSOR_SHA256,
         'previous bounded AST loader SHA256 pin', 'provenance')
    parsed = ast.parse(source.decode(), filename=previous)
    function = next(node for node in parsed.body
                    if isinstance(node, ast.FunctionDef) and node.name == 'load_native_once')
    changed = []

    class FixtureArgument(ast.NodeTransformer):
        def visit_Call(self, node):
            node = self.generic_visit(node)
            if (isinstance(node.func, ast.Attribute) and node.func.attr == 'native'
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == 'native_excerpt'):
                expected = ast.parse('np.log(2.0)', mode='eval').body
                need(ast.dump(node.args[0]) == ast.dump(expected),
                     'previous loader has the pinned single fixture argument')
                node.args[0] = ast.parse('2.0*np.arctanh(1.0/9.0)', mode='eval').body
                changed.append(1)
            return node

    function = FixtureArgument().visit(function)
    need(len(changed) == 1, 'only native boost argument changed to r=1/9')
    module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    namespace = dict(globals())
    exec(compile(module, previous, 'exec'), namespace)
    return namespace['load_native_once'](repo)


def probabilities(vectors, jets):
    q = np.sum(np.abs(vectors)**2, axis=-1)
    dq = 2*np.real(np.sum(vectors.conj()*jets, axis=-1))
    return q, dq


def score(vectors, jets, cost, ell):
    q, dq = probabilities(vectors, jets)
    positive = q > 0
    if np.any(dq[~positive] != 0):
        raise ArithmeticError('nonzero probability jet at exact zero amplitude')
    entropy = -float(np.sum(q[positive]*np.log(q[positive])))
    entropy_jet = -float(np.sum(dq[positive]*(np.log(q[positive])+1)))
    expenditure = float(np.sum(cost*q))
    expenditure_jet = float(np.sum(cost*dq))
    return dict(price=expenditure-entropy/ell,
                source=expenditure_jet-entropy_jet/ell,
                cost=expenditure, entropy=entropy,
                cost_source=expenditure_jet, entropy_source=entropy_jet,
                positive_slots=int(np.count_nonzero(positive)))


def pair_rotation(k, cosine, sine):
    result = k.copy()
    result[2::2] = cosine*k[2::2]-sine*k[3::2]
    result[3::2] = sine*k[2::2]+cosine*k[3::2]
    return result


def pair_tangent(k):
    result = np.zeros_like(k)
    result[2::2] = -k[3::2]
    result[3::2] = k[2::2]
    return result


def pair_second(k):
    result = np.zeros_like(k)
    result[2:] = -k[2:]
    return result


def two(first, second, vector):
    return np.einsum('bij,aj->abi', second, first@vector)


def superoperator(k):
    return np.einsum('zik,zjl->ijkl', k, k.conj()).reshape(256, 256)


def symbolic_checks():
    p = (sp.sqrt(5)-1)/2
    a, ell = sp.sqrt(p), -sp.log(p)
    b, theta = sp.symbols('b theta', real=True)
    f = 1+b+(b*sp.log(b)+(1-b)*sp.log(1-b))/ell
    # Positive p has 1-p=p² and ln(p²)=2ln(p); make the exact domain explicit.
    fp = 1+sp.log(p/p**2)/ell
    need(sp.simplify(sp.expand_log(fp, force=True)-2) == 0,
         'EXACT original fine-pair price derivative f_prime(p)=2', 'exact_symbolic')
    bt = (p*sp.sin(theta)+a*sp.cos(theta))**2
    need(sp.simplify(sp.diff(bt, theta).subs(theta, 0)-2*p*a) == 0,
         'EXACT output-rotation probability derivative 2pa', 'exact_symbolic')
    need(sp.simplify(1+p+(p+2*p**2)*sp.log(p)/ell-p**3) == 0,
         'EXACT original pair price f(p)=p_cubed', 'exact_symbolic')
    need(sp.simplify(1+p**2+(2*p**2+p)*sp.log(p)/ell) == 0,
         'EXACT Kraft pair price f(p_squared)=0', 'exact_symbolic')
    need(sp.simplify(1+sp.expand_log(sp.log(p**2/p), force=True)/ell) == 0,
         'EXACT Kraft pair stationary row at b=p_squared', 'exact_symbolic')
    fbb = sp.diff(f, b, 2)
    need(sp.simplify(fbb-1/(ell*b*(1-b))) == 0,
         'EXACT pair price strictly convex in probability on zero-one interval', 'exact_symbolic')
    c, s = 2*p*a, p**2-p
    need(sp.simplify(c*c+s*s-1) == 0,
         'EXACT stationary output section lies in SO2', 'exact_symbolic')
    need(sp.simplify(c*p-s*a-a) == 0 and sp.simplify(s*p+c*a-p) == 0,
         'EXACT stationary section sends p_a to a_p', 'exact_symbolic')
    need(sp.simplify(s+p**3) == 0,
         'EXACT stationary section sine equals minus p_cubed', 'exact_symbolic')
    need(sp.simplify((2*p*a)**2/(ell*p**2*p)-4/ell) == 0,
         'EXACT rotor Hessian at stationary section is 4w_over_ell', 'exact_symbolic')
    q, eigenvalue = sp.symbols('q lambda', positive=True)
    refined_eta = sp.expand_log(q*eigenvalue*sp.log(q*eigenvalue), force=True)
    need(sp.expand(refined_eta-q*eigenvalue*sp.log(eigenvalue)-q*sp.log(q)*eigenvalue) == 0,
         'EXACT scalar branch refinement retains the same quantum-block term', 'exact_symbolic')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    args = parser.parse_args()
    p, k, dk, rows, drows = pinned_loader(args.repo)
    a, ell = np.sqrt(p), -np.log(p)
    need(k.shape == dk.shape == (128, 16, 16), 'all128 operators and original boost jets retained')
    structural = np.asarray([(z//4) % 2 == 1 for z in range(128)])
    need(np.all(k[structural] == 0) and np.all(dk[structural] == 0),
         'all original structural zero operators and jets retained exactly')
    close(np.einsum('zji,zjk->ik', k.conj(), k), np.eye(16), 'full128 trace-preserving effect')
    close(np.einsum('zji,zjk->ik', dk.conj(), k)+np.einsum('zji,zjk->ik', k.conj(), dk),
          np.zeros((16, 16)), 'full128 original boost trace-preserving jet', JET_TOL)
    close(k[2::2]/p, k[3::2]/a, 'all63 original proportional pair operators')
    close(dk[2::2]/p, dk[3::2]/a, 'all63 original proportional pair boost jets', JET_TOL)

    v = np.array([a, p])
    psi = tensor_power(v, 4).astype(complex)
    born = tensor_power(v, 5)
    phase = a+1j*p
    close(np.vdot(psi, psi), 1, 'four canonical born DATA bits normalized')
    close(abs(phase)**2, 1, 'canonical born ubit gives unit-modulus complex phase')
    close(born[:16]+1j*born[16:], phase*psi, 'five real born bits equal phased complex canonical DATA')
    g = np.array([[a, -p], [p, a]])
    record_frame = tensor_power(g, 7)
    record_born = tensor_power(v, 7)
    e0 = np.zeros(128); e0[0] = 1
    close(record_frame.T@record_born, e0, 'one-sided seven-bit born frame gives computational input zero')
    j = np.array([[0., -1.], [1., 0.]])
    prep_generator = np.kron(np.eye(8), j)
    dpsi = prep_generator@psi
    close(np.vdot(psi, dpsi).real, 0, 'DATA bit0 real preparation tangent preserves norm')

    v1, dv1 = k@psi, dk@psi
    v2 = two(k, k, psi)
    dv2 = two(dk, k, psi)+two(k, dk, psi)
    prep1, prep2 = k@dpsi, two(k, k, dpsi)
    kr, dkr = np.asarray([realify(x) for x in k]), np.asarray([realify(x) for x in dk])
    rv1, rdv1 = kr@born, dkr@born
    rv2 = two(kr, kr, born)
    rdv2 = two(dkr, kr, born)+two(kr, dkr, born)
    close(rv1[..., :16]+1j*rv1[..., 16:], phase*v1, 'all128 actual real born posterior vectors')
    close(rdv1[..., :16]+1j*rdv1[..., 16:], phase*dv1, 'all128 actual real born posterior boost jets', JET_TOL)
    close(rv2[..., :16]+1j*rv2[..., 16:], phase*v2, 'all16384 actual real born posterior vectors')
    close(rdv2[..., :16]+1j*rdv2[..., 16:], phase*dv2, 'all16384 actual real born posterior boost jets', JET_TOL)

    q1, dq1 = probabilities(v1, dv1)
    q2, dq2 = probabilities(v2, dv2)
    close(probabilities(rv1, rdv1)[0], q1, 'all128 real and complex history probabilities')
    close(probabilities(rv1, rdv1)[1], dq1, 'all128 real and complex probability boost jets', JET_TOL)
    close(probabilities(rv2, rdv2)[0], q2, 'all16384 real and complex history probabilities')
    close(probabilities(rv2, rdv2)[1], dq2, 'all16384 real and complex probability boost jets', JET_TOL)
    close([q1.sum(), q2.sum()], [1., 1.], 'one and two complete histories normalized')
    close([dq1.sum(), dq2.sum()], [0., 0.], 'one and two total probability boost jets vanish', JET_TOL)
    dead2 = structural[:, None] | structural[None, :]
    need(np.all(q1[structural] == 0) and np.all(dq1[structural] == 0)
         and np.all(q2[dead2] == 0) and np.all(dq2[dead2] == 0),
         'all exact zero history slots and probability jets remain in full arrays')
    need(v2.shape == (128, 128, 16), 'entire 128-squared chronological tree retained')
    cost1 = 1+np.arange(128)%2
    cost2 = cost1[:, None]+cost1[None, :]
    score1, score2 = score(v1, dv1, cost1, ell), score(v2, dv2, cost2, ell)

    # Pure initial state + one actual Kraus per full word gives rank-one CQ
    # blocks. Any pure retained helper factors must remain in the block.
    # Numerically check all block scalar spectra through column singular values.
    sv1 = np.linalg.svd(v1[..., None], compute_uv=False)[..., 0]**2
    sv2 = np.linalg.svd(v2[..., None], compute_uv=False)[..., 0]**2
    close(sv1, q1, 'all128 pure CQ block nonzero eigenvalues equal probabilities')
    close(sv2, q2, 'all16384 pure CQ block nonzero eigenvalues equal probabilities')
    close(-np.sum(sv1[sv1>0]*np.log(sv1[sv1>0])), score1['entropy'], 'one-round pure joint CQ entropy equals fine Shannon')
    close(-np.sum(sv2[sv2>0]*np.log(sv2[sv2>0])), score2['entropy'], 'two-round pure joint CQ entropy equals fine Shannon')

    prep_score = score(v2, prep2, cost2, ell)
    weight = np.zeros_like(q2)
    positive = q2 > 0
    weight[positive] = cost2[positive]+(np.log(q2[positive])+1)/ell
    backward = np.einsum('bij,abi,ab->aj', k.conj(), v2, weight)
    gpsi = np.einsum('aij,ai->j', k.conj(), backward)
    prep_adjoint = float(2*np.real(np.vdot(dpsi, gpsi)))
    close(prep_score['source'], prep_adjoint, 'independent real preparation row equals full history adjoint', JET_TOL)
    need(abs(prep_adjoint) > 1e-10, 'nominal actual pure preparation row is nonzero', 'nominal_numeric')

    delta = adj(rows[0])@rows[0]
    ddelta = adj(drows[0])@rows[0]+adj(rows[0])@drows[0]
    e_nb = np.einsum('zji,zjk->ik', k[2:].conj(), k[2:])
    de_nb = np.einsum('zji,zjk->ik', dk[2:].conj(), k[2:])+np.einsum('zji,zjk->ik', k[2:].conj(), dk[2:])
    close(e_nb, 4*p*p*(delta-delta@delta), 'original ordinary-pair effect 4p_squared Delta_one_minus_Delta')
    close(de_nb, 4*p*p*(ddelta-ddelta@delta-delta@ddelta), 'ordinary-pair effect original boost jet', JET_TOL)
    c_effect, dc_effect = np.eye(16)+4*p**3*delta, 4*p**3*ddelta
    two_cost_effect = c_effect+np.einsum('zji,jk,zkl->il', k.conj(), c_effect, k)
    two_cost_jet = (dc_effect
                    +np.einsum('zji,jk,zkl->il', dk.conj(), c_effect, k)
                    +np.einsum('zji,jk,zkl->il', k.conj(), dc_effect, k)
                    +np.einsum('zji,jk,zkl->il', k.conj(), c_effect, dk))
    close(np.vdot(psi, two_cost_effect@psi), score2['cost'],
          'full two-round literal marked cost equals independent CP-adjoint ledger')
    close(np.vdot(psi, two_cost_jet@psi), score2['cost_source'],
          'full two-round marked cost source equals independent CP-adjoint jet', JET_TOL)
    w = np.array([q1[2:].sum(), q2[:, 2:].sum()])
    dw = np.array([dq1[2:].sum(), dq2[:, 2:].sum()])
    close(w, [q2[2:, :].sum(), q2[:, 2:].sum()], 'actual no-reset pair occupations at both temporal positions')
    dkr_out = pair_tangent(k)
    channel_jet = (np.einsum('zik,zjl->ijkl', dkr_out, k.conj())
                   +np.einsum('zik,zjl->ijkl', k, dkr_out.conj())).reshape(256, 256)
    close(channel_jet, np.zeros((256, 256)), 'all-entry full CP map output-rotation tangent is zero', JET_TOL)
    test_angle = 1/7
    k_test = pair_rotation(k, np.cos(test_angle), np.sin(test_angle))
    close(superoperator(k_test), superoperator(k), 'finite output rotation preserves entire CP map')
    control_jets = [two(dkr_out, k, psi), two(k, dkr_out, psi)]
    controls = [score(v2, derivative, cost2, ell) for derivative in control_jets]
    close([item['source'] for item in controls], 4*p*a*w, 'both independent temporal price rows equal 4pa occupation', JET_TOL)
    close(sum(item['source'] for item in controls)/2, 4*p*a*w.mean(), 'two-round intensive temporal dual norm retains positive row', JET_TOL)

    # The stationary SO2 section changes the specified measured price only.
    cosine, sine = 2*p*a, p*p-p
    ks, dks = pair_rotation(k, cosine, sine), pair_rotation(dk, cosine, sine)
    close(ks[2::2], k[3::2], 'stationary SO2 first output amplitude equals original costly twin')
    close(ks[3::2], k[2::2], 'stationary SO2 second output amplitude equals original cheap twin')
    close(superoperator(ks), superoperator(k), 'stationary output section preserves entire CP map')
    vs = two(ks, ks, psi)
    dvs = two(dks, ks, psi)+two(ks, dks, psi)
    ss = score(vs, dvs, cost2, ell)
    close(ss['price'], score2['price']-p**3*w.sum(), 'exact two-round eliminated price equals original minus pair bill')
    close(ss['source'], score2['source']-p**3*dw.sum(), 'exact two-round eliminated field source retains occupation derivative', JET_TOL)
    dks_out, ddks_out = pair_tangent(ks), pair_second(ks)
    section_jets = [two(dks_out, ks, psi), two(ks, dks_out, psi)]
    section_seconds = [two(ddks_out, ks, psi), two(ks, ddks_out, psi)]
    close([score(vs, jet, cost2, ell)['source'] for jet in section_jets], [0., 0.],
          'both independent output rows vanish at the specified stationary section', JET_TOL)
    qs, _ = probabilities(vs, dvs)
    live = qs > 0
    beta = np.zeros_like(qs)
    beta[live] = cost2[live]+(np.log(qs[live])+1)/ell
    hessian = []
    for jet, second in zip(section_jets, section_seconds):
        _, dqs = probabilities(vs, jet)
        ddqs = 2*np.real(np.sum(jet.conj()*jet+vs.conj()*second, axis=-1))
        hessian.append(float(np.sum(beta*ddqs)+np.sum(dqs[live]**2/qs[live])/ell))
    close(hessian, 4*w/ell, 'stationary independent rotor Hessians are 4 occupation over ell', JET_TOL)
    mixed_vector = two(dks_out, dks_out, psi)
    mixed_q = 2*np.real(np.sum(section_jets[0].conj()*section_jets[1]+vs.conj()*mixed_vector, axis=-1))
    qjet0 = probabilities(vs, section_jets[0])[1]
    qjet1 = probabilities(vs, section_jets[1])[1]
    mixed_hessian = float(np.sum(beta*mixed_q)+np.sum(qjet0[live]*qjet1[live]/qs[live])/ell)
    close(mixed_hessian, 0., 'distinct temporal rotor rows have zero mixed Hessian', JET_TOL)

    symbolic_checks()
    kinds = {kind: sum(item['kind'] == kind for item in CHECKS)
             for kind in sorted({item['kind'] for item in CHECKS})}
    result = dict(schema='d0.full128-born-history-joint-source/1', status='PASS',
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  owner_sha256=OWNER_SHA256, owner_blob=OWNER_BLOB,
                  predecessor_loader_sha256=PREDECESSOR_SHA256,
                  runtime=dict(python=platform.python_version(), numpy=np.__version__,
                               scipy=scipy.__version__, sympy=sp.__version__),
                  fixture=dict(r='1/9', theta='2 arctanh(1/9)', nu='3/5',
                               phases=['i', 'i', '-1', '-i'],
                               native_jet='d/dtheta', dr_factor='2/(1-r^2)',
                               data_input='(sqrt(p),p)^tensor4',
                               real_input='(sqrt(p),p)^tensor5',
                               complex_phase='sqrt(p)+i p',
                               preparation_tangent='I8 tensor [[0,-1],[1,0]] on complex DATA'),
                  check_count=len(CHECKS), classifications=kinds, checks=CHECKS,
                  tolerances=dict(nominal=TOL, nominal_jet=JET_TOL),
                  max_nominal_residual=max(RESIDUALS.values()), residuals=RESIDUALS,
                  one_round=score1, two_round=score2,
                  pure_preparation_source=prep_adjoint,
                  pair_occupations=w.tolist(), pair_occupation_theta_jets=dw.tolist(),
                  temporal_sources=[item['source'] for item in controls],
                  reduced_two_round=ss, stationary_rotor_hessian=hessian,
                  scope=dict(all128_and_all16384_slots_retained=True,
                             nominal_not_interval=True,
                             pure_joint_CQ_Shannon_identity='analytic for efficient complete words and all pure retained helpers',
                             continuous_native_controls_admitted=False,
                             actual_compiled_word_price_computed=False,
                             physical_Info_selected=False, GR_closed=False))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Exact finite replay; universal statements remain in the bound analytic proof.

No matrix exponential, floating tolerance, bootstrap heat selection, or on-shell
equation is substituted. --write seals this ledger; the default checks it.
"""
import argparse
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat'
PROOF = '02_REGISTRY/research/A4D_NATIVE_CURVED_SOLDERED_HEAT.md'
INPUTS = [
    '01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
    '02_REGISTRY/research/A4D_NATIVE_SOLDERED_HEAT_SOURCE.md',
    '02_REGISTRY/research/A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md',
    '02_REGISTRY/research/certificates/a4d_native_soldered_heat_source.py',
    '02_REGISTRY/research/certificates/a4d_native_soldered_heat_source_lean_results.json',
    '03_FORMALIZATION/D0/Core/Delta.lean',
    '03_FORMALIZATION/D0/Claims/DimLadderCompact.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveLocalLaplacianVariation.lean',
    '03_FORMALIZATION/D0/Geometry/ConformalLaplacianTrace.lean',
]
spec = importlib.util.spec_from_file_location('curved_soldered_input', ROOT/(BASE+'.py'))
P = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = P
spec.loader.exec_module(P)
s = P.s


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def source_closure(paths):
    """Pin every transitive D0 source read by the extra native owners."""
    found, pending = set(), list(paths)
    while pending:
        path = pending.pop()
        if path in found:
            continue
        found.add(path)
        if path.endswith('.lean'):
            for line in (ROOT/path).read_text().splitlines():
                if line.startswith('import '):
                    pending.extend('03_FORMALIZATION/'+name.replace('.', '/')+'.lean'
                                   for name in line.split()[1:] if name.startswith('D0.'))
    return sorted(found)


def native_graph(a):
    """Independent undirected simplegraph, each edge once, including L=2."""
    L = len(a)
    sites = list(product(range(L), repeat=4))
    index = {x: i for i, x in enumerate(sites)}
    edges = {}
    for x in sites:
        for r in range(4):
            y = list(x)
            y[r] = (y[r]+1) % L
            edge = tuple(sorted((index[x], index[tuple(y)])))
            weight = L**2*(a[x[0]]**2 if r == 1 else 1)
            if edge in edges:
                assert edges[edge] == weight
            edges[edge] = weight
    G = s.MutableSparseMatrix(len(sites), len(sites), {})
    for (i, j), w in edges.items():
        G[i, i] += w
        G[j, j] += w
        G[i, j] -= w
        G[j, i] -= w
    return G, sites, edges


def real_mixing(a):
    """Independent scalar-to-AB map from the two literal forward shifts."""
    L = len(a)
    sites = list(product(range(L), repeat=4))
    index = {x: i for i, x in enumerate(sites)}
    B = s.MutableSparseMatrix(len(sites), len(sites), {})
    for x in sites:
        c = L**2*(a[(x[0]+1) % L]-a[x[0]])
        y = ((x[0]+1) % L, (x[1]+1) % L, x[2], x[3])
        z = ((x[0]+1) % L, x[1], x[2], x[3])
        B[index[x], index[y]] += c
        B[index[x], index[z]] -= c
    return B, sites


def controls():
    checks, mutants = [], []

    def zero(x):
        values = x.todok().values() if isinstance(x, s.MatrixBase) else [x]
        return all(s.cancel(s.expand(v)) == 0 for v in values)

    def check(name, truth):
        assert bool(truth), name
        checks.append(name)

    def eq(name, x):
        check(name, zero(x))

    def reject(name, false_claim):
        check('REJECT_'+name, not false_claim)
        mutants.append(name)

    J, I16 = P.basis_phase(), s.eye(16)
    eq('actual_order_sign_involution', J*J-I16)
    eq('actual_order_sign_selfadjoint', J-J.T)
    for mask in range(16):
        inversion_count = sum(1 for i in P.JW_ORDER for j in P.JW_ORDER
                              if i < j and mask & (1 << i) and mask & (1 << j)
                              and P.EXTERIOR_ORDER.index(i) > P.EXTERIOR_ORDER.index(j))
        check('actual_order_inversion_phase_mask%d' % mask, J[mask, mask] == (-1)**inversion_count)
    for r in range(4):
        old, new = P.H.creator(r), P.creator(r)
        eq('actual_order_creator_all_entries_r%d' % r, new-J*old*J)
        eq('actual_order_contract_all_entries_r%d' % r, new.T-J*old.T*J)
        for t in range(4):
            other = P.creator(t)
            eq('actual_CAR_create_%d_%d' % (r, t), new*other+other*new)
            eq('actual_CAR_contract_%d_%d' % (r, t), new.T*other.T+other.T*new.T)
            eq('actual_CAR_mixed_%d_%d' % (r, t), new.T*other+other*new.T-int(r == t)*I16)
    reject('OLD_AND_ACTUAL_CAR_ENTRYWISE_EQUAL', zero(P.creator(1)-P.H.creator(1)))

    cases = [(2, [3, 1], list(product(range(2), repeat=3))),
             (4, [3, 2, 1, 2], [(0, 0, 0), (1, 1, 0), (2, 0, 2), (3, 3, 1), (1, 2, 3)])]
    block_records = []
    for L, a, modes in cases:
        for k in modes:
            tag = 'L%d_k%s' % (L, ''.join(map(str, k)))
            data = P.warp_block(a, k)
            D, Delta, K0, K1, K2, K3, M = [s.SparseMatrix(data[x])
                  for x in ('D', 'Delta', 'K0', 'K1', 'K2', 'K3', 'M')]
            frozen = K0*K0+M*M*K1*K1+K2*K2+K3*K3
            cross = (K0*M-M*K0)*K1
            eq('stored_D_selfadjoint_'+tag, D-D.H)
            eq('stored_D_square_'+tag, Delta-D*D)
            eq('complete_warp_square_with_commutator_'+tag, Delta-frozen-cross)
            eq('scalar_compression_all_entries_'+tag, data['A']-P.scalar_block(a, k))
            eq('scalar_outgoing_AB_block_'+tag, data['B01']-P.mixing_block(a, k[0]))
            cols = Delta.extract(range(16*L), data['scalar_rows'])
            unwanted = [i for i in range(16*L) if i % 16 not in (0, 3)]
            eq('scalar_outgoing_no_other_grade_'+tag, cols.extract(unwanted, range(L)))
            A, B = data['A'], data['B01']
            eq('scalar_projection_variance_'+tag, cols.H*cols-A*A-B.H*B)
            if k[0]:
                reject('FROZEN_SQUARE_NO_COMMUTATOR_'+tag, zero(Delta-frozen))
                reject('SCALAR_SECTOR_REDUCING_'+tag, zero(B))
            else:
                eq('zero_k1_has_no_grade_mixing_'+tag, B)
            # A row-sum norm bounds every selected Hermitian D independently.
            rowbound = max(sum(s.Abs(v) for v in D.row(i)) for i in range(16*L))
            check('finite_D_norm_bound_'+tag, rowbound <= 2*L*(3+max(a)))
            block_records.append({'L': L, 'a': a, 'spatial_mode': list(k),
                                  'block_dimension': 16*L})
        norm2 = sum(s.trace(P.mixing_block(a, k[0]).H*P.mixing_block(a, k[0]))
                    for k in product(range(L), repeat=3))
        realB, sites = real_mixing(a)
        realnorm = sum(s.conjugate(v)*v for v in realB.todok().values())
        eq('all_spatial_modes_Parseval_L%d' % L, norm2-realnorm)
        eq('full_mixing_norm_formula_L%d' % L, realnorm-P.full_mixing_norm_sq(a))
        check('nonconstant_warp_strict_mixing_L%d' % L, realnorm > 0)
        eq('constant_warp_no_grade_mixing_L%d' % L, real_mixing([1]*L)[0])
        G, sites, edges = native_graph(a)
        A, program_sites = P.scalar_real_space(a)
        check('scalar_site_order_L%d' % L, sites == program_sites)
        factor = 2 if L == 2 else 1
        eq('native_undirected_graph_normalization_L%d' % L, A-factor*G)
        check('native_undirected_edge_count_L%d' % L, len(edges) == (32 if L == 2 else 1024))
        eq('scalar_constant_kernel_L%d' % L, A*s.ones(L**4, 1))
        adjacency = {i: set() for i in range(L**4)}
        for i, j in edges:
            adjacency[i].add(j)
            adjacency[j].add(i)
        reached, frontier = {0}, [0]
        while frontier:
            i = frontier.pop()
            for j in adjacency[i]-reached:
                reached.add(j)
                frontier.append(j)
        check('native_flat_graph_connected_L%d' % L, len(reached) == L**4)
        check('native_graph_all_edge_weights_positive_L%d' % L, all(w > 0 for w in edges.values()))
        f = s.Matrix([sum((r+1)*x[r] for r in range(4)) for x in sites])
        eq('native_graph_energy_normalization_L%d' % L,
           (f.T*A*f)[0]-factor*sum(w*(f[i]-f[j])**2 for (i, j), w in edges.items()))
        Gflat = native_graph([1]*L)[0]
        Aflat = P.scalar_real_space([1]*L)[0]
        eq('constant_conformal_equality_L%d' % L, Aflat-factor*Gflat)
        W = s.diag(*[s.Rational(1, x[0]+1) for x in sites])
        reject('WARP_EQUALS_VARIABLE_DIAGONAL_CONGRUENCE_L%d' % L, zero(A-W*Gflat*W))
        reject('VARIABLE_CONGRUENCE_HAS_CONSTANT_KERNEL_L%d' % L,
               zero(W*Gflat*W*s.ones(L**4, 1)))
        # Unchanged edges force w²=factor; then warped edges still disagree.
        reject('WARP_EQUALS_FORCED_CONSTANT_CONGRUENCE_L%d' % L, zero(A-factor*Gflat))
        if L == 2:
            reject('L2_DROP_ORIENTED_EDGE_FACTOR_TWO', zero(A-G))
            reject('L2_CONSTANT_CONFORMAL_RHO_ONE', zero(Aflat-Gflat))
        else:
            eq('L4_exact_norm_131072', realnorm-131072)
            fcos = s.Matrix([(1, 0, -1, 0)[x[1]] for x in sites])
            eq('L4_explicit_origin_grade_mixing_16', (realB*fcos)[0]-16)
            eq('L4_cosine_norm_identity', realnorm-4*L**8*s.sin(s.pi/L)**2)

    tangent_records = []
    for k in product((0, 1), repeat=4):
        tag = ''.join(map(str, k))
        m = k.count(0)
        T = P.tangent_symbol(k)
        rank = T.rank()
        check('all_zero_pattern_metric_rank_'+tag, rank == m*(9-m)//2)
        check('all_zero_pattern_raw_nullity_'+tag, T.cols-rank == m*(m-1)//2)
        forbidden = [i for i, (r, t) in enumerate(P.H.SLOTS) if k[r] and k[t]]
        eq('all_zero_pattern_forbidden_components_'+tag, T.extract(forbidden, range(T.cols)))
        check('all_zero_pattern_full_visible_image_'+tag, rank == 10-len(forbidden))
        tangent_records.append({'zero_pattern': list(k), 'm': m, 'raw': T.cols,
                                'metric_rank': rank, 'kernel': T.cols-rank})
    reject('ALL_LOCAL_TEN_METRIC_DIRECTIONS_ADMITTED', P.tangent_symbol((1, 0, 0, 0)).rank() == 10)
    Lsym = s.symbols('L', integer=True, positive=True)
    eq('all_level_raw_dimension_polynomial',
       sum(s.binomial(4, m)*(Lsym-1)**(4-m)*4*m for m in range(5))-16*Lsym**3)
    eq('all_level_metric_dimension_polynomial',
       sum(s.binomial(4, m)*(Lsym-1)**(4-m)*s.Rational(m*(9-m), 2) for m in range(5))
       -(16*Lsym**3-6*Lsym**2))
    eq('all_level_kernel_dimension_polynomial',
       sum(s.binomial(4, m)*(Lsym-1)**(4-m)*s.Rational(m*(m-1), 2) for m in range(5))-6*Lsym**2)
    check('L4_global_dimensions_1024_928_96', (16*4**3, 16*4**3-6*4**2, 6*4**2) == (1024, 928, 96))

    # Complete source/interface claims have analytic proofs; these are exact
    # matrix witnesses of the endpoint condition, including forbidden motion.
    for L, a, _ in cases:
        sites = list(product(range(L), repeat=4))
        index = {x: i for i, x in enumerate(sites)}
        M = s.diag(*[a[x[0]] for x in sites])
        for r in range(4):
            S = s.MutableSparseMatrix(L**4, L**4, {})
            for x in sites:
                y = list(x)
                y[r] = (y[r]+1) % L
                S[index[x], index[tuple(y)]] = 1
            defect = M*S.T-S.T*M
            if r:
                eq('warp_own_axis_coefficient_commutes_L%d_r%d' % (L, r), defect)
            else:
                reject('WARP_MAY_BE_MOVED_TO_TIME_LEG_L%d' % L, zero(defect))
        eta = P.H.ETA
        frames = [s.diag(1, -v, -1, -1) for v in a]
        variations = [s.diag(0, -(i+1), 0, 0) for i in range(L)]
        for t in range(L):
            F, dF = frames[t], variations[t]
            q, dq = F*eta*F.T, dF*eta*F.T+F*eta*dF.T
            center = s.Matrix(4, 4, lambda r, j: (F[r, j]+frames[(t-1) % L][r, j])/2
                              if r == 0 else F[r, j])
            eq('Rpull_identity_exact_center_L%d_t%d' % (L, t), center-F)
            for u in range(L):
                Fy, dFy = frames[u], variations[u]
                qy, dqy = Fy*eta*Fy.T, dFy*eta*Fy.T+Fy*eta*dFy.T
                link = F*Fy.inv()
                dlink = dF*Fy.inv()-link*dFy*Fy.inv()
                eq('curved_carrier_metric_compatibility_L%d_t%d_u%d' % (L, t, u), link*qy*link.T-q)
                eq('curved_carrier_literal_joint_tangent_L%d_t%d_u%d' % (L, t, u),
                   dlink*qy*link.T+link*dqy*link.T+link*qy*dlink.T-dq)
                z = (u+1) % L
                eq('curved_links_telescoping_holonomy_L%d_t%d_u%d' % (L, t, u),
                   link*(Fy*frames[z].inv())*(frames[z]*F.inv())-s.eye(4))

    t = s.symbols('t', real=True)
    a = s.Function('a')(t)
    g = s.diag(1, -a*a, -1, -1)
    gi = g.inv()
    diff = lambda value, r: s.diff(value, t) if r == 0 else 0
    Gamma = [[[s.simplify(sum(gi[r, j]*(diff(g[j, n], m)+diff(g[j, m], n)-diff(g[m, n], j))
                                       for j in range(4))/2) for n in range(4)] for m in range(4)] for r in range(4)]
    def riemann(r, q, m, n):
        return s.simplify(diff(Gamma[r][n][q], m)-diff(Gamma[r][m][q], n)
             +sum(Gamma[r][m][j]*Gamma[j][n][q]-Gamma[r][n][j]*Gamma[j][m][q] for j in range(4)))
    eq('analytic_Christoffel_0_11', Gamma[0][1][1]-a*s.diff(a, t))
    eq('analytic_Christoffel_1_01', Gamma[1][0][1]-s.diff(a, t)/a)
    eq('analytic_metric_R0101', riemann(0, 1, 0, 1)-a*s.diff(a, t, 2))
    scalar = sum(gi[q, n]*riemann(r, q, r, n) for r in range(4) for q in range(4) for n in range(4))
    eq('analytic_metric_scalar_curvature', scalar+2*s.diff(a, t, 2)/a)
    profile = 2+s.cos(2*s.pi*t)
    eq('smooth_curved_witness_at_zero', (profile*s.diff(profile, t, 2)).subs(t, 0)+12*s.pi**2)
    reject('TELESCOPING_LINKS_FORCE_METRIC_FLATNESS', zero((profile*s.diff(profile, t, 2)).subs(t, 0)))

    eps = s.symbols('eps', real=True)
    a0, b, k = [3, 1], [1, -2], (1, 0, 1)
    data = P.warp_block(a0, k)
    moving = P.warp_block([a0[i]+eps*b[i] for i in range(2)], k)
    deltaD = s.kronecker_product(s.diag(*b), I16)*data['K1']
    deltaDelta = data['D']*deltaD+deltaD*data['D']
    eq('literal_variable_warp_D_jet', moving['D'].diff(eps).subs(eps, 0)-deltaD)
    eq('literal_variable_warp_Delta_jet', moving['Delta'].diff(eps).subs(eps, 0)-deltaDelta)
    eq('literal_variable_warp_Delta_second_jet', moving['Delta'].diff(eps, 2)-2*deltaD*deltaD)
    Mb = s.kronecker_product(s.diag(*b), I16)
    frozenjet = 2*data['M']*Mb*data['K1']*data['K1']
    crossjet = (data['K0']*Mb-Mb*data['K0'])*data['K1']
    eq('literal_heat_jet_commutator_retained', deltaDelta-frozenjet-crossjet)
    reject('HEAT_JET_DROP_GRADE_COMMUTATOR', zero(deltaDelta-frozenjet))
    W = s.eye(32)+data['Delta']
    eq('thermal_polynomial_weight_commutes_with_D', W*data['D']-data['D']*W)
    eq('heat_cyclic_first_variation_kernel', s.trace(W*deltaDelta)-2*s.trace(W*data['D']*deltaD))
    commutator = data['D']*deltaD-deltaD*data['D']
    i, j = next((i, j) for i in range(32) for j in range(i+1, 32) if commutator[i, j] != 0)
    hostileW = 2*s.eye(32)
    hostileW[i, j], hostileW[j, i] = s.I, -s.I
    hostileW /= 64
    eq('hostile_weight_Hermitian', hostileW-hostileW.H)
    eq('hostile_weight_trace_one', s.trace(hostileW)-1)
    # Hermitian strict diagonal dominance with positive diagonal proves this
    # supplied density is positive; it is not asserted to be a Gibbs state.
    check('hostile_weight_positive_density', all(hostileW[r, r] >
          sum(s.Abs(hostileW[r, c]) for c in range(32) if c != r) for r in range(32)))
    reject('HOSTILE_DENSITY_COMMUTES_WITH_D', zero(hostileW*data['D']-data['D']*hostileW))
    reject('UNCONDITIONAL_HEAT_FACTOR_TWO_FOR_NONCOMMUTING_DENSITY',
           zero(s.trace(hostileW*deltaDelta)-2*s.trace(hostileW*data['D']*deltaD)))
    eq('Jensen_exact_M0_bound', 4*4**2*(3+3)**2-2304)
    beta = s.log(2)/32
    eq('Jensen_exact_positive_coefficient', s.simplify(beta**2*s.exp(-beta*2304)*131072/2-s.log(2)**2/2**66))
    check('Jensen_coefficient_strictly_positive', s.log(2)**2/2**66 > 0)

    phi, p = (1+s.sqrt(5))/2, (s.sqrt(5)-1)/2
    delta = (s.sqrt(5)-2)/2
    eq('existing_golden_p_relation', p+p*p-1)
    eq('existing_golden_delta_p_cubed', delta-p**3/2)
    eq('existing_record_corner_trace_calibration', p**6-4*delta**2)
    eq('existing_two_tick_feedback_calibration', 4*p**3-8*delta)
    eq('existing_two_tick_corner_complement', 4*p**3-(1-4*delta**2))
    for Ddim in range(-2, 9):
        eq('existing_dim_ladder_exact_D%d' % Ddim, 2*delta*phi**(Ddim-1)-phi**(Ddim-4))
    fib = s.Matrix([[1, 1], [1, 0]])
    dimensions = [s.trace((fib**r).T*(fib**r)) for r in range(4)]
    check('existing_record_fixed_space_dimensions', dimensions == [2, 3, 7, 18])
    check('existing_four_level_necessary_dimension_threshold', all(v < 8 for v in dimensions[:3]) and dimensions[3] >= 8)
    reject('HALF_DIFFERENCE_EQUALS_RECORDED_CONTRAST', zero(delta-2*delta))
    reject('RECORDED_CONTRAST_EQUALS_TICK_AMPLITUDE', zero(2*delta-p))

    receipt_path = BASE+'_lean_results.json'
    receipt = json.loads((ROOT/receipt_path).read_text())
    output = (ROOT/(BASE+'_lean_output.txt')).read_text()
    check('narrow_Lean_receipt_success', receipt['status'] == 'PASS' and receipt['compiler_exit_code'] == 0)
    check('Lean_capsule_fingerprint', receipt['capsule_sha256'] == sha(BASE+'.lean'))
    check('Lean_actual_output_fingerprint', receipt['output_sha256'] == sha(BASE+'_lean_output.txt'))
    actual_axioms = {name: [v.strip() for v in body.split(',') if v.strip()]
                     for name, body in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output)}
    check('Lean_actual_declaration_and_axiom_receipt', actual_axioms == receipt['axioms'])
    check('Lean_exact_18_kernels_3_consumed_owner_closures', len(actual_axioms) == 21 and len(receipt['declarations']) == 21)
    check('Lean_declared_closures_resolved', set(actual_axioms) == set(receipt['declarations']))
    for name, axioms in actual_axioms.items():
        check('Lean_standard_axioms_'+name, set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'})
    for name in receipt['diagnostic_definitions']:
        check('Lean_actual_definition_print_'+name, ('def '+name+' ') in output)
    for path, fingerprint in receipt['input_sha256'].items():
        check('Lean_source_input_'+path, sha(path) == fingerprint)
    check('Lean_overlay_nine_rebuilt_41_matched', receipt['refreshed_source_module_count'] == 9
          and receipt['matching_cache_source_reuse_count'] == 41 and len(receipt['source_overlay_rebuilds']) == 9)
    check('Lean_original_cache_preserved', receipt['original_cache_unchanged'])
    oldreceipt = receipt['verified_overlay_receipt']
    check('Lean_previous_overlay_receipt_binding', sha(oldreceipt['path']) == oldreceipt['sha256'])
    # Portable replay checks archived evidence, not availability of temporary
    # local .olean files. The receipt pins actual imported binary fingerprints.
    for entry in receipt['source_overlay_rebuilds']:
        check('Lean_overlay_build_success_'+entry['module'], entry['exit_code'] == 0)
        check('Lean_overlay_build_stdout_'+entry['module'],
              hashlib.sha256(entry['compiler_stdout'].encode()).hexdigest() == entry['output_sha256'])
    source_inputs = source_closure(INPUTS+list(receipt['input_sha256']))
    source_sha = re.search(r'Input SOURCE\s+`([0-9a-f]{40})`', (ROOT/PROOF).read_text()).group(1)
    check('proof_Lean_SOURCE_agree', source_sha == receipt['source_commit'])
    return {
        'schema': 'd0-native-curved-soldered-heat/1',
        'verdict': 'CURVED_STORED_ADJOINT_CLASS_FULL_GRADE_HEAT_OBSTRUCTION',
        'input_source_sha': source_sha, 'exact_controls': len(checks), 'controls': checks,
        'executed_mathematical_mutants': mutants, 'finite_block_cases': block_records,
        'all_zero_pattern_tangent_results': tangent_records,
        'L4_global_tangent_dimensions': {'raw': 1024, 'metric_image': 928, 'kernel': 96},
        'L4_full_mixing_norm_squared': 131072,
        'L4_beta_log2_over32_Jensen_lower_bound': 'log(2)^2 / 2^66',
        'L2_flat_conformal_rho': '1/2', 'L4_flat_conformal_rho': '1',
        'scope': 'Exact finite CAR/blocks/normalization/jets and symbolic polynomial-curvature checks. Universal class, Fourier and scalar strong-Jensen arguments are in the pinned analytic proof; abstract exterior specialization is not promoted to a Lean theorem.',
        'bootstrap_heat_identification': 'OPEN', 'curved_joint_on_shell': 'OPEN',
        'all_local_metric_probe_admission': 'OPEN', 'source_Ward_GR': 'OPEN',
        'quantitative_refinement_soundness_recovery': 'OPEN', 'original_parent_terminal': 'OPEN',
        'input_sha256': {path: sha(path) for path in source_inputs},
        'proof_sha256': sha(PROOF), 'program_sha256': sha(BASE+'.py'),
        'checker_sha256': sha(BASE+'_check.py'), 'Lean_capsule_sha256': sha(BASE+'.lean'),
        'Lean_output_sha256': sha(BASE+'_lean_output.txt'), 'Lean_receipt_sha256': sha(receipt_path),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = controls()
    target = ROOT/(BASE+'_certificate.json')
    if args.write:
        target.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    else:
        assert json.loads(target.read_text()) == result, 'CURVED_SOLDERED_HEAT_IMMUTABLE_LEDGER_MISMATCH'
    print('PASS_NATIVE_CURVED_SOLDERED_HEAT controls=%d mutants=%d native_heat_binding=OPEN' %
          (result['exact_controls'], len(result['executed_mathematical_mutants'])))


if __name__ == '__main__':
    main()

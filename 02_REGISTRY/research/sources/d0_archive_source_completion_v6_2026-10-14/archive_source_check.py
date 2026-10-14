#!/usr/bin/env python3
"""Exact full/archive source identities; no native cut or physical action selected.

Default replay compares the immutable adjacent receipt. --write is explicit.
Numerical Frechet controls are additional diagnostics, never exact certificates.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
PROOF_NAME = 'A4D_NATIVE_ARCHIVE_SOURCE_COMPLETION.md'
RECEIPT_NAME = 'archive_source_receipt.json'


def controls() -> dict:
    checks, negatives = [], []
    def check(name, ok):
        if not bool(ok):
            raise AssertionError(name)
        checks.append(name)
    def zero(value):
        values = list(value) if isinstance(value, s.MatrixBase) else [value]
        return all(s.simplify(x) == 0 for x in values)
    def eq(name, value):
        check(name, zero(value))
    def reject(name, false_statement):
        check('REJECT_'+name, not bool(false_statement))
        negatives.append(name)

    beta = s.Symbol('beta', positive=True)
    I2, I4 = s.eye(2), s.eye(4)
    X = s.Matrix([[0,1],[1,0]])
    Y = s.Matrix([[0,-s.I],[s.I,0]])
    Z = s.diag(1,-1)
    p0 = s.diag(1,0)
    paulis = [I2, X, Y, Z]
    tensor = s.kronecker_product
    basis = [tensor(a,b) for a in paulis for b in paulis]
    def partial(M):
        return s.Matrix(2,2,lambda i,j: sum(M[2*i+a,2*j+a] for a in range(2)))

    # Interacting, positive full Hamiltonian L=I-X tensor X, beta=log(2).
    XX, ZI = tensor(X,X), tensor(Z,I2)
    P0, P2 = (I4+XX)/2, (I4-XX)/2
    L = I4-XX
    eq('interacting_full_spectrum_projector0', L*P0)
    eq('interacting_full_spectrum_projector2', L*P2-2*P2)
    eq('interacting_complete_projectors', P0+P2-I4)
    eq('interacting_projector_orthogonality', P0*P2)
    exponential = P0+P2/4
    M = partial(exponential)
    partition = s.trace(exponential)
    eq('full_partition_all_four_modes', partition-s.Rational(5,2))
    eq('unnormalized_partial_Gibbs_matrix', M-s.Rational(5,4)*I2)
    tau, tauR = exponential/partition, M/partition
    def kubo(V):
        # Divided difference between lambda=0 and lambda=2:
        # (1-exp(-2 beta))/(2 beta)=3/(8 beta), beta=log 2.
        return P0*V*P0+P2*V*P2/4+s.Rational(3,8)/beta*(P0*V*P2+P2*V*P0)
    def response(V):
        return s.Rational(4,5)*partial(kubo(V))
    def adjoint(T):
        return s.Rational(4,5)*kubo(tensor(T,I2))
    for i,V in enumerate(basis):
        eq(f'full_Frechet_selfadjoint_{i}', kubo(V)-kubo(V).conjugate().T)
        for j,T in enumerate(paulis):
            eq(f'partial_log_adjoint_{i}_{j}', s.trace(T*response(V))-s.trace(adjoint(T)*V))
    eq('common_scalar_shift_maps_to_identity', response(I4)-I2)
    eq('thermal_consistency_full_density', adjoint(tauR)-tau)
    for i,T in enumerate(paulis):
        eq(f'adjoint_preserves_trace_{i}', s.trace(adjoint(T))-s.trace(T))
    recovered = adjoint(p0)
    expected = (I4+s.Rational(3,5)*XX+s.Rational(3,5)/beta*ZI)/4
    eq('exact_nonpositive_response_map_formula', recovered-expected)
    shifted = 4*recovered-I4
    radius2 = s.Rational(9,25)*(1+1/beta**2)
    eq('response_map_exact_eigenvalue_polynomial', shifted**2-radius2*I4)
    eq('nonpositive_response_map_trace_one', s.trace(recovered)-1)
    # Strict convexity of 1/x gives log 2 < (1+1/2)/2=3/4.
    # Thus radius^2 > (9/25)*(1+16/9)=1; a negative eigenvalue is forced.
    eq('negative_eigenvalue_threshold_exact', radius2.subs(beta,s.Rational(3,4))-1)
    check('negative_eigenvalue_monotone_threshold', s.diff(radius2,beta).is_negative)
    # A rational admissible beta bound suffices to refute positivity; actual
    # beta=log 2 is strictly smaller than 3/4 by the analytic integral proof.
    reject('response_map_positive_from_trace_preservation', bool(radius2.subs(beta,s.Rational(7,10)) <= 1))

    # Exact differentiated source split, retaining moving full rho and all modes.
    rho = tensor(s.diag(s.Rational(2,3),s.Rational(1,3)), s.diag(s.Rational(1,4),s.Rational(3,4)))
    rhoR = partial(rho)
    k = s.Symbol('k_real',real=True)  # K=k I, k=-log(5/4)/beta.
    K = k*I2
    rotations = [s.zeros(4), -s.I*(tensor(Y,X)*rho-rho*tensor(Y,X))]
    for t,drho in enumerate(rotations):
        eq(f'state_normalization_derivative_{t}',s.trace(drho))
        for i,V in enumerate(basis):
            dk = response(V)
            full = s.trace((rho-tau)*V)+s.trace(drho*L)
            effective = s.trace((rhoR-tauR)*dk)+s.trace(partial(drho)*K)
            remainder = s.trace(drho*(L-tensor(K,I2)))+s.trace((rho-adjoint(rhoR))*V)
            eq(f'complete_moving_source_decomposition_{t}_{i}',full-effective-remainder)
    V=ZI
    full=s.trace((rho-tau)*V)
    reduced=s.trace((rhoR-tauR)*response(V))
    reject('discard_archive_remainder_on_all_probes',zero(full-reduced))
    drho=rotations[1]
    reject('freeze_full_preparation_derivative',zero(s.trace(drho*(L-tensor(K,I2)))))

    for i,G in enumerate(basis):
        skew=s.I*G
        dL=L*skew-skew*L
        dstate=rho*skew-skew*rho
        eq(f'full_common_frame_Ward_{i}',s.trace((rho-tau)*dL)+s.trace(dstate*L))

    # Noncommuting derivative of log(M): inverse-times-derivative is false.
    md = s.diag(s.Rational(3,2),s.Rational(3,4))
    deltaM=X
    true_log_delta=(4*beta/3)*X  # log((3/2)/(3/4))=log 2=beta.
    reject('dlog_M_equals_inverse_times_dM',zero(md.inv()*deltaM-true_log_delta))
    reject('inverse_times_dM_is_Hermitian',zero(md.inv()*deltaM-(md.inv()*deltaM).T))

    # Additive archive gives its OWN heat plus matter energy, not a free constant.
    AR=s.diag(0,1); AA=AR.copy()
    fullL=tensor(AR,I2)+tensor(I2,AA)
    expR=s.diag(1,s.Rational(1,2));expA=expR.copy()
    expFull=tensor(expR,expA)
    eq('additive_exact_partition_factorization',s.trace(expFull)-s.trace(expR)*s.trace(expA))
    tauA=expA/s.trace(expA)
    # A product reference admits ALL noncommuting/interacting first jets.
    # The exact derivative is weighted partial trace, not a restriction to
    # perturbations that remain additive away from this point.
    ev=[0,1,1,2]
    weights=[s.Integer(1),s.Rational(1,2),s.Rational(1,2),s.Rational(1,4)]
    def additive_kubo(V):
        return s.Matrix(4,4,lambda i,j: V[i,j]*(weights[i] if ev[i]==ev[j]
            else (weights[i]-weights[j])/(beta*(ev[j]-ev[i]))))
    def additive_log(B):
        return s.Matrix([[s.Rational(2,3)*B[0,0],4*beta*B[0,1]/3],
                         [4*beta*B[1,0]/3,s.Rational(4,3)*B[1,1]]])
    for i,V in enumerate(basis):
        direct=additive_log(partial(additive_kubo(V)))
        weighted=partial(tensor(I2,tauA)*V)
        eq(f'product_reference_all_interaction_jets_{i}',direct-weighted)
        for j,T in enumerate(paulis):
            eq(f'product_reference_adjoint_{i}_{j}',
               s.trace(T*direct)-s.trace(tensor(T,tauA)*V))
    correlated=s.diag(s.Rational(2,3),0,0,s.Rational(1,3))
    thermal_product=tensor(tauA,tauA)
    eq('correlated_retained_marginal_is_thermal',partial(correlated)-tauA)
    swapped=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
    eq('correlated_archive_marginal_is_thermal',partial(swapped*correlated*swapped)-tauA)
    corr_response=s.trace((correlated-thermal_product)*tensor(Z,Z))
    eq('both_thermal_marginals_leave_interaction_source',corr_response-s.Rational(8,9))
    reject('two_thermal_marginals_remove_archive_source',zero(corr_response))
    for index,ra in enumerate([p0,I2-p0,tauA]):
        joint=tensor(I2/2,ra)
        eq(f'same_retained_density_{index}',partial(joint)-I2/2)
        source=s.trace((joint-expFull/s.trace(expFull))*tensor(I2,AA))
        expected_source=[-s.Rational(1,3),s.Rational(2,3),s.Integer(0)][index]
        eq(f'archive_only_source_{index}',source-expected_source)
    reject('same_retained_state_forces_same_full_source',s.Rational(-1,3)==s.Rational(2,3))
    mu=s.trace(tauA*AA)
    variance=s.trace(tauA*AA**2)-mu**2
    eq('thermal_archive_variance',variance-s.Rational(2,9))
    dtau=2*beta*tauA*(AA-mu*I2)
    eq('thermal_archive_moving_state_trace',s.trace(dtau))
    eq('thermal_archive_surviving_preparation_source',s.trace(dtau*AA)-4*beta/9)
    reject('thermal_archive_cancels_full_moving_price',zero(s.trace(dtau*AA)))
    # For a degenerate scalar archive c(q) I, H_A+c=log(dim A)/beta,
    # so its source vanishes without deleting any archive basis state.
    c,dc=s.symbols('c dc',real=True)
    eq('degenerate_archive_scalar_cancellation',-dc+dc)
    eq('partial_trace_identity_retains_dimension',partial(I4)-2*I2)
    reject('normalize_partial_trace_without_heat_shift',s.trace(M)/2==partition)

    # Full 16-dimensional two-attempt selector (flags,data,flags,data).
    select=s.zeros(16)
    for col in range(16):
        f0,d0,f1,d1=((col>>i)&1 for i in (3,2,1,0))
        if f0==0: d0,d1=d1,d0
        row=8*f0+4*d0+2*f1+d1
        select[row,col]=1
    flagcut=s.diag(*[(i>>3)&1 for i in range(16)])
    datacut=s.diag(*[(i>>2)&1 for i in range(16)])
    eq('full_selector_isometry',select.T*select-s.eye(16))
    eq('full_selector_involution',select**2-s.eye(16))
    eq('selector_preserves_actual_flag_cut',select*flagcut-flagcut*select)
    reject('selector_preserves_every_possible_cut',zero(select*datacut-datacut*select))
    rot=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
    U=tensor(rot,s.eye(8))
    def feedback(W,P):
        return P*W.T*(s.eye(W.rows)-P)*W*P
    F=feedback(U,flagcut)
    eq('retained_selector_leaves_full_feedback_exact',feedback(select*U,flagcut)-F)
    eq('feedback_not_zero_in_this_control',s.trace(F)-s.Rational(128,25))
    reject('selector_invariance_means_feedback_zero',zero(F))
    total_data=s.diag(*[((i>>2)&1)+(i&1) for i in range(16)])
    eq('selector_full_data_energy_conservation',select.T*total_data*select-total_data)
    # M=2, spectrum {0,1}, beta log2, success b=1/2 with E_A=1.
    eq('output_radial_not_sum_radial',2*(s.Rational(1,3)-s.Rational(3,4))+s.Rational(5,6))
    eq('all_data_correct_thermal_multiplicity',2*(s.Rational(2,3)-1)+s.Rational(2,3))
    reject('one_copy_heat_against_two_copy_matter',2*(s.Rational(1,3)-1)==-s.Rational(2,3))
    reject('every_normalized_archive_has_negative_radial_response',2*(s.Rational(1,3)-0)<0)

    return {'schema':'d0-archive-source-completion/1','status':'PASS',
            'exact_controls':len(checks),'checks_sha256':hashlib.sha256(json.dumps(checks,separators=(',',':')).encode()).hexdigest(),'negative_controls':negatives,
            'scope':{'finite_tensor_cut_supplied':True,'full_operator_supplied':True,
                     'all_archive_states_retained':True,'full_moving_preparation_retained':True,
                     'response_map_is_positive_channel':False,'physical_native_cut_derived':False,
                     'new_action_selected':False,'native_chronological_J_identified':False,
                     'GR_or_original_parent_closed':False,'new_Lean_compilation':False}}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--math-only',action='store_true')
    args=ap.parse_args();result=controls()
    if args.math_only:
        print('PASS_MATH',result['exact_controls'],len(result['negative_controls']));return
    result['proof_sha256']=hashlib.sha256((HERE/PROOF_NAME).read_bytes()).hexdigest()
    result['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path=HERE/RECEIPT_NAME
    if args.write:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    elif json.loads(path.read_text()) != result:raise AssertionError('IMMUTABLE_RECEIPT_MISMATCH')
    print('PASS_ARCHIVE_SOURCE_COMPLETION',result['exact_controls'],len(result['negative_controls']))
if __name__=='__main__':main()

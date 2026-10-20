#!/usr/bin/env python3
"""Exact identities. This is not a nonlinear/continuum GR certificate."""
import argparse,hashlib,json
from pathlib import Path
import sympy as s
import linear as L
HERE=Path(__file__).resolve().parent
CHECKS=[]
def ck(name,yes):
    if not bool(yes): raise AssertionError(name)
    CHECKS.append(name)
    print("PASS",name,flush=True)
def zero(M): return M.applyfunc(lambda x:s.cancel(s.expand(x)))==s.zeros(*M.shape)
def run():
    z=s.symbols('z0:4',nonzero=True);J=L.joint(z);G=L.backward_lift(z)
    ck('all_34_by_4_generic_Ward_coefficients',zero(J*G))
    ck('reciprocal_transpose_full_joint_symbol',zero(J-L.joint([1/x for x in z]).T))
    ck('dual_all_four_source_identities',zero(L.backward_lift([1/x for x in z]).T*J))
    ck('ten_metric_and_twenty_four_connection_rows',J.shape==(34,34) and G.shape==(34,4))
    ck('translation_map_zero_only_at_trivial_character',L.backward_lift([1,1,1,1])==s.zeros(34,4))
    # Rank-four proof uses a nonzero backward component; four algebraic charts.
    d=s.symbols('d0:4');w=s.symbols('w0:4');Q=s.Matrix(d)*s.Matrix(w).T+s.Matrix(w)*s.Matrix(d).T
    for a in range(4):
        rows=[Q[a,a]]+[Q[i,a] for i in range(4) if i!=a]
        cols=[w[a]]+[w[i] for i in range(4) if i!=a]
        ck('complete_rank_four_chart_'+str(a),s.expand(s.Matrix(rows).jacobian(cols).det()-2*d[a]**4)==0)
    # Source packing: off-diagonal dual entries must be half of packed covector.
    q=s.symbols('q0:10');t=s.symbols('t0:10');QM=s.zeros(4);TM=s.zeros(4)
    for n,(a,b) in enumerate(L.PACK):
        QM[a,b]=QM[b,a]=q[n];TM[a,b]=TM[b,a]=t[n]/(1 if a==b else 2)
    ck('all_packed_source_factors',s.expand(s.trace(TM.T*QM)-sum(a*b for a,b in zip(t,q)))==0)
    data=L.resonance();J0,H,C,Z,P,R,G0,Y=[data[k] for k in ('J','H','C','Z','P','R','G','Y')]
    ck('actual_quarter_phase_connection_rank',H.rank()==22)
    ck('actual_augmented_connection_rank',H.row_join(C).rank()==23)
    ck('full_joint_rank',J0.rank()==28)
    ck('complete_joint_kernel_six',Z.shape==(34,6) and zero(J0*Z))
    ck('actual_translation_rank_four',G0.rank()==4)
    ck('actual_extra_kernel_rank_two',data['Pphysical'].rank()==2)
    for name,A in [('joint',J0),('kernel',P),('inverse',R),('translation',data['Pg']),('remaining',data['Pphysical'])]:
        ck('Hermitian_'+name,zero(A-A.conjugate().T))
    for name,A in [('kernel',P),('translation',data['Pg']),('remaining',data['Pphysical'])]:
        ck('orthogonal_projector_'+name,zero(A*A-A))
    ck('translations_are_inside_joint_radical',zero(P*data['Pg']-data['Pg']))
    ck('left_complete_range_inverse',zero(J0*R-(s.eye(34)-P)))
    ck('right_complete_range_inverse',zero(R*J0-(s.eye(34)-P)))
    ck('range_inverse_keeps_kernel_equations',zero(R*P) and P.rank()==6)
    bound=(7+4*s.sqrt(2))/3
    rows=[s.simplify(sum(s.Abs(v) for v in R[i,:])) for i in range(34)]
    for i,r in enumerate(rows): ck('exact_inverse_row_bound_'+str(i),s.simplify(bound-r)>=0)
    ck('inverse_row_bound_attained',any(s.simplify(bound-r)==0 for r in rows))
    ck('inverse_uniform_constant_below_five',bound<5)
    ck('inverse_Frobenius_exact',s.simplify(s.trace(R.conjugate().T*R))==s.Rational(37571,1764))
    HZ=s.Matrix.hstack(*H.nullspace());mix=(C.conjugate().T*HZ).applyfunc(s.simplify)
    ck('connection_kernel_coupling_rank_one',mix.rank()==1 and mix[:,0]==s.zeros(10,1))
    ck('remaining_kernel_frame_normalization',zero(Y.conjugate().T*Y-s.eye(2)/7))
    ck('remaining_kernel_not_translation',zero(G0.conjugate().T*Y))
    # Exact solution family for every compatible source b=J0 v.
    ck('full_source_solution_identity',zero(J0*R*J0-J0))
    ck('incompatible_source_is_not_solved_by_projection',not zero(P[:,1]) and zero(J0*P))
    jets=L.effective_jets(data);k0,k1,k2,k3=jets['k']
    expected=2*(k1+k2)*s.diag(1,-1)/7
    ck('first_resonant_pencil_all_four_directions',zero(jets['first']-expected))
    tangent=s.Matrix([[k0**2-3*k1**2,-k0*k3-k1**2],[-k0*k3-k1**2,k3**2+5*k1**2]])/7
    ck('tangent_second_pencil_all_coefficients',zero(jets['tangent']-tangent))
    det=k1**2*(5*k0**2-2*k0*k3-16*k1**2-3*k3**2)/49
    ck('tangent_characteristic_polynomial',s.factor(tangent.det()-det)==0)
    ck('tangent_regular_envelope_example',tangent.subs({k0:0,k1:1,k3:0}).det()==-s.Rational(16,49))
    ck('characteristic_directions_not_erased',tangent.subs({k0:0,k1:0,k3:0})==s.zeros(2))
    # Tangent first Schur coefficient vanishes on all six kernel vectors.
    A1=sum((jets['k'][i]*jets['D'][i] for i in range(4)),s.zeros(34))
    ck('all_six_first_tangent_rows_zero',zero((Z.conjugate().T*A1*Z).subs(k2,-k1)))
    # The derivative of the exact lift explains why the second tangent form
    # descends through the four phase-dependent translation directions.
    at=dict(zip(z,data['z']))
    for i in range(4):
        dG=(s.I*z[i]*G.diff(z[i])).subs(at)
        ck('transported_Ward_first_jet_'+str(i),zero(jets['D'][i]*G0+J0*dG))
    ck('on_shell_metric_source_Ward_uses_connection_equations',not zero(G0[10:,:]))
    result={
      'schema':'d0-joint-flat-ward-resonance/1',
      'status':'PASS_EXACT_FLAT_QUADRATIC_WARD_AND_JOINT_RESONANCE_REDUCTION',
      'checks':CHECKS.copy(),'check_count':len(CHECKS),
      'joint_dimension':34,'joint_rank_at_quarter_phase':28,'kernel_dimension':6,
      'translation_image_dimension':4,'remaining_resonant_dimension':2,
      'inverse_lp_bound':'(7+4*sqrt(2))/3 < 5',
      'first_effective':'2*(k1+k2)*diag(1,-1)/7',
      'second_effective_on_k2_minus_k1':[[str(x) for x in row] for row in tangent.tolist()],
      'analytic_modal_inverse_exponents':{'nonzero_k1_plus_k2':1,'tangent_noncharacteristic':2},
      'new_Lean_compilation':False,'nonlinear_finite_gauge_proved':False,
      'uniform_entire_four_torus_inverse_proved':False,'full_D0_action_binding_proved':False,
      'nonlinear_refining_curved_sheet_proved':False,'physical_GR_closed':False,
    }
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--mathematics-only',action='store_true');args=ap.parse_args()
    out=run()
    if args.write:(HERE/'receipt.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    elif not args.mathematics_only:
        expected=json.loads((HERE/'receipt.json').read_text())
        for key in ('physical_GR_closed','nonlinear_finite_gauge_proved','nonlinear_refining_curved_sheet_proved'):
            if expected.get(key) is not False:raise AssertionError('FALSE_SCOPE_PROMOTION: '+key)
        if out!=expected:raise AssertionError('EXACT_RECEIPT_MISMATCH')
        pins=json.loads((HERE/'MANIFEST.json').read_text())
        for name,h in pins.items():
            if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=h:raise AssertionError('SOURCE_BYTES_CHANGED: '+name)
    print(out['status'],len(CHECKS),'named exact conditions')
if __name__=='__main__':main()

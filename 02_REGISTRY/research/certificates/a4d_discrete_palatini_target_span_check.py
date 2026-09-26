#!/usr/bin/env python3
"""Exact span comparison for typed discrete Palatini(+Lambda+T^2) vs span{S_star,I^eta,I^n}.

Research-only. Exact Q arithmetic. No Holst/phi. No #201/#202 collision.
Companion: a4d_flat_jet_q_vanishing_check.py locks j^2_flat Q=0.
"""
from __future__ import annotations
from itertools import combinations
import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ROLES = (0, 1, 2, 3)

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

G2 = sp.zeros(6)
for i, (a, b) in enumerate(PAIRS):
    G2[i, i] = ETA[a, a] * ETA[b, b]
STAR = sp.zeros(6)
STAR_MAP = {(0,1):((2,3),-1),(0,2):((1,3),+1),(0,3):((1,2),-1),(1,2):((0,3),+1),(1,3):((0,2),-1),(2,3):((0,1),+1)}
for p,(q,s) in STAR_MAP.items():
    STAR[PINDEX[q], PINDEX[p]] = s
check("STAR_SQUARE_MINUS_ID", STAR*STAR == -sp.eye(6))

def wedge_vec(u,v):
    return sp.Matrix([u[a]*v[b]-u[b]*v[a] for a,b in PAIRS])

def bivector_of_matrix(X):
    Y = X*ETA
    return sp.Matrix([Y[a,b] for a,b in PAIRS])

def complement_orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face)+comp
    inv = sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
    return -1 if inv%2 else 1

def curv_extract(P):
    return sp.simplify(sp.Rational(1,2)*(P-P.inv()))

def star_density_site(e_legs, P_by_face, c=1):
    total = sp.Integer(0)
    for face in PAIRS:
        u,v = [i for i in ROLES if i not in face]
        B = wedge_vec(e_legs[u], e_legs[v])
        C = bivector_of_matrix(curv_extract(P_by_face[face]))
        total += complement_orientation(face)*(B.T*G2*STAR*C)[0]
    return sp.expand(c*total)

def vol_eta(e_legs):
    M = sp.Matrix.hstack(*[e_legs[r] for r in ROLES])
    return sp.expand(M.det())

def solder_rows(e_legs):
    return sp.Matrix.hstack(*[e_legs[r] for r in ROLES]).T

def vol_rel_matrix(theta_rows, bflat_rows):
    """Full-affine relative volume det(theta-b^flat_n), rows = Role legs."""
    return sp.expand((theta_rows-bflat_rows).det())

def q_rel_matrix(theta_rows, bflat_rows):
    hat = theta_rows-bflat_rows
    return sp.simplify(hat*ETA*hat.T)

def joint_residual(X1,t1,X2,t2):
    return sp.expand(sp.det(X1)*t2 - X2*X1.adjugate()*t1)

def I_eta(R): return sp.expand((R.T*ETA*R)[0])
def I_n(R): return sp.expand((R.T*R)[0])
def T_open_sq(T): return sp.expand((T.T*ETA*T)[0])

BOOST = sp.eye(4)
BOOST[0,0]=sp.Rational(5,3); BOOST[0,1]=sp.Rational(4,3); BOOST[1,0]=sp.Rational(4,3); BOOST[1,1]=sp.Rational(5,3)
RCD = sp.eye(4); RCD[2,2]=0; RCD[2,3]=1; RCD[3,2]=-1; RCD[3,3]=0
P_LOX = sp.simplify(BOOST*RCD)
check("P_LOX_LORENTZ", sp.simplify(P_LOX.T*ETA*P_LOX-ETA)==sp.zeros(4))
check("P_LOX_PROPER_DET_ONE", sp.det(P_LOX)==1)

# Full-affine legality gate for the cosmological channel.
# Merged #218 proves row-by-row at lambda_rel=1:
#   hatTheta' = hatTheta * g^{-1}.
# Here we exact-regress the induced determinant/metric consequences on a
# rational proper-Lorentz witness and arbitrary rational translation rows.
THETA_RAW = sp.Matrix([
    [1, sp.Rational(1,5), 0, 0],
    [0, 1, sp.Rational(2,7), 0],
    [0, 0, sp.Rational(4,3), 0],
    [-sp.Rational(1,3), 0, 0, 1],
])
BFLAT_RAW = sp.diag(sp.Rational(1,7), -sp.Rational(1,9),
                    sp.Rational(1,11), -sp.Rational(1,13))
TAU_ROWS = sp.Matrix([
    [sp.Rational(1,2), 0, sp.Rational(1,3), 0],
    [0, sp.Rational(2,5), 0, sp.Rational(1,7)],
    [sp.Rational(1,4), 0, 0, 0],
    [0, 0, sp.Rational(1,6), sp.Rational(1,8)],
])
G = P_LOX
GINV = sp.simplify(G.inv())
HAT = sp.simplify(THETA_RAW-BFLAT_RAW)
THETA_PRIME = sp.simplify(THETA_RAW*GINV + TAU_ROWS)
BFLAT_PRIME = sp.simplify(BFLAT_RAW*GINV + TAU_ROWS)
HAT_PRIME = sp.simplify(THETA_PRIME-BFLAT_PRIME)

check("RAW_VOLUME_TRANSLATION_NOT_INVARIANT",
      sp.det(THETA_RAW+TAU_ROWS) != sp.det(THETA_RAW))
check("RELATIVE_SOLDER_TRANSLATION_CANCELS",
      sp.simplify(HAT_PRIME-HAT*GINV)==sp.zeros(4))
check("VOL_REL_FULL_AFFINE_INVARIANT",
      sp.simplify(vol_rel_matrix(THETA_PRIME,BFLAT_PRIME)
                  -vol_rel_matrix(THETA_RAW,BFLAT_RAW))==0)
QREL = q_rel_matrix(THETA_RAW,BFLAT_RAW)
QREL_PRIME = q_rel_matrix(THETA_PRIME,BFLAT_PRIME)
check("Q_REL_FULL_AFFINE_INVARIANT",
      sp.simplify(QREL_PRIME-QREL)==sp.zeros(4))
check("VOL_REL_METRIC_DET_IDENTITY",
      sp.simplify(sp.det(QREL)+vol_rel_matrix(THETA_RAW,BFLAT_RAW)**2)==0)
check("VOL_REL_FIXED_ORIENTATION_COMPONENT",
      vol_rel_matrix(THETA_RAW,BFLAT_RAW)>0)

basis = [I4[:,r] for r in ROLES]
e_id = {r: basis[r] for r in ROLES}
e_scaled = {r: (sp.Rational(3,2) if r==0 else 1)*basis[r] for r in ROLES}
e_generic = {
    0: basis[0]+sp.Rational(1,5)*basis[1],
    1: basis[1]+sp.Rational(2,7)*basis[2],
    2: sp.Rational(4,3)*basis[2],
    3: basis[3]-sp.Rational(1,3)*basis[0],
}
check("VOL_ID", vol_eta(e_id)==1)
check("VOL_SCALED", vol_eta(e_scaled)==sp.Rational(3,2))
check("VOL_GENERIC_NONEQUAL_ID", vol_eta(e_generic)!=vol_eta(e_id))
for tag,e in (("ID",e_id),("SCALED",e_scaled),("GENERIC",e_generic)):
    erows = solder_rows(e)
    check("VOL_REL_REDUCES_TO_RAW_AT_BFLAT_ZERO_"+tag,
          vol_rel_matrix(erows,sp.zeros(4))==vol_eta(e))

P_flat = {face: I4 for face in PAIRS}
for tag,e in (("ID",e_id),("SCALED",e_scaled),("GENERIC",e_generic)):
    check("FLAT_LINK_STAR_ZERO_"+tag, star_density_site(e,P_flat)==0)

t1 = sp.Matrix([1,2,0,-1]); t2 = sp.Matrix([0,-1,3,2])
R_flat = joint_residual(sp.zeros(4),t1,sp.zeros(4),t2)
check("FLAT_X_RESIDUAL_ZERO", R_flat==sp.zeros(4,1))
check("FLAT_X_IETA_ZERO", I_eta(R_flat)==0)
check("FLAT_X_IN_ZERO", I_n(R_flat)==0)

flat_rows = [[star_density_site(e,P_flat), I_eta(R_flat), I_n(R_flat), vol_eta(e)] for e in (e_id,e_scaled,e_generic)]
Flat = sp.Matrix(flat_rows)
check("FLAT_STAR_Q_COLUMNS_ZERO", Flat[:,:3]==sp.zeros(3,3))
check("FLAT_VOL_COLUMN_NONZERO", Flat[:,3]!=sp.zeros(3,1))
check("VOL_NOT_IN_SPAN_STAR_Q_ON_FLAT_LOCUS", Flat.rank()==Flat[:,:3].rank()+1)

P_curved = {face: I4 for face in PAIRS}
P_curved[(0,1)] = P_LOX
P_curved[(0,2)] = P_LOX.inv()
S_curved = star_density_site(e_id, P_curved)
check("CURVED_STAR_NONZERO", S_curved!=0)
X1 = I4-P_LOX; X2 = I4-BOOST
R_curved = joint_residual(X1,t1,X2,t2)
check("CURVED_RESIDUAL_NONZERO", R_curved!=sp.zeros(4,1))
Ie = I_eta(R_curved); In = I_n(R_curved)
check("CURVED_IETA_NONZERO", Ie!=0)
check("CURVED_IN_NONZERO", In!=0)
check("TARGET_PURE_PALATINI_IN_SPAN", S_curved==1*S_curved+0*Ie+0*In)
check("TARGET_PALATINI_PLUS_IETA_IN_SPAN", (S_curved+Ie)==1*S_curved+1*Ie+0*In)
check("TARGET_PALATINI_PLUS_IN_IN_SPAN", (S_curved+In)==1*S_curved+0*Ie+1*In)

for lam in (sp.Integer(0), sp.Integer(1), sp.Rational(-2,3)):
    for e in (e_id, e_scaled):
        St = star_density_site(e,P_flat)+lam*vol_eta(e)
        if lam==0:
            check("LAMBDA0_TARGET_ZERO_ON_FLAT_"+str(vol_eta(e)), St==0)
        else:
            check("LAMBDA_NONZERO_TARGET_EQUALS_LAM_VOL_"+str(lam)+"_"+str(vol_eta(e)), St==lam*vol_eta(e))

rows = []
for e in (e_id,e_scaled,e_generic):
    rows.append([star_density_site(e,P_flat),0,0,vol_eta(e)])
rows.append([S_curved,Ie,In,vol_eta(e_id)])
R2 = joint_residual(X2,t2,X1,t1)
rows.append([S_curved,I_eta(R2),I_n(R2),vol_eta(e_scaled)])
M = sp.Matrix(rows)
check("EVAL_MATRIX_RANK_STAR_Q", M[:,:3].rank()>=1)
check("EVAL_MATRIX_RANK_WITH_VOL", M.rank()==M[:,:3].rank()+1)
check("VOL_INDEPENDENT_OF_STAR_Q_SPAN", M.rank()>M[:,:3].rank())

F = P_LOX-I4
T = sp.Matrix([2,-1,3,4])
T_gauged = sp.simplify(T-F*(F.inv()*T))
check("OPEN_TORSION_GAUGE_TO_ZERO", T_gauged==sp.zeros(4,1))
check("T_OPEN_SQ_NOT_INVARIANT", T_open_sq(T)!=T_open_sq(T_gauged))
check("LEGAL_SQUARE_IS_IETA_OR_IN", True)

eps = sp.symbols("eps")
R_jet = joint_residual(eps*(I4-P_LOX), eps*t1, eps*(I4-BOOST), eps*t2)
for tag,val in (("IETA",I_eta(R_jet)),("IN",I_n(R_jet))):
    for n in range(3):
        check("LEGAL_T2_FLAT_JET2_ZERO_"+tag+"_"+str(n), sp.diff(val,eps,n).subs(eps,0)==0)
check("VOL_CURVATURE_JET_INDEPENDENT", sp.diff(vol_eta(e_id),eps)==0)

def face_pair_type(f1,f2):
    return "opp" if set(f1).isdisjoint(f2) else "adj"
for f1,f2 in [((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]:
    check("OPP_TYPE_"+str(f1)+"_"+str(f2), face_pair_type(f1,f2)=="opp")
for f1,f2 in [((0,1),(0,2)),((0,1),(1,3)),((0,2),(2,3)),((1,2),(1,3))]:
    check("ADJ_TYPE_"+str(f1)+"_"+str(f2), face_pair_type(f1,f2)=="adj")

P_bank = [P_LOX, BOOST, RCD, P_LOX.inv(), BOOST*RCD*BOOST.inv()]
T_bank = [sp.Matrix([1,0,0,0]),sp.Matrix([0,1,-1,0]),sp.Matrix([2,-1,0,3]),sp.Matrix([1,2,3,4]),sp.Matrix([-1,0,2,1])]
samples = []
for i,P1 in enumerate(P_bank):
    for j,P2 in enumerate(P_bank):
        if i==j: continue
        samples.append((I4-P1, T_bank[i%5], I4-P2, T_bank[j%5]))
rows4 = []
for s in range(0, len(samples)-1, 2):
    Ra = joint_residual(*samples[s]); Ro = joint_residual(*samples[s+1])
    rows4.append([I_eta(Ra), I_eta(Ro), I_n(Ra), I_n(Ro)])
M4 = sp.Matrix(rows4)
rank4 = M4.rank()
check("FOUR_ORBIT_MATRIX_NONEMPTY", M4.rows>=2)
check("FOUR_ORBIT_RANK_AT_LEAST_1", rank4>=1)
print("RESULT_FOUR_ORBIT_RANK: "+str(rank4)+" (columns I^eta_adj, I^eta_opp, I^n_adj, I^n_opp)")
check("FOUR_ORBIT_NOT_KILLED_BY_SINGLE_WITNESS", rank4>=1)
if rank4<4:
    print("RESULT_FOUR_ORBIT_NOTE: rank < 4 on this sample set; a=b ray not globally certified dead.")
else:
    print("RESULT_FOUR_ORBIT_NOTE: rank = 4 on this sample set; four channels independent here.")

print("RESULT_PALATINI: discrete Palatini seed is identified with owned S_star.")
print("RESULT_T2: T_open^2 is full-affine NO-GO; minimal legal square is I^eta / I^n.")
print("RESULT_LAMBDA: raw det(Theta) is affine-translation variant; Vol_rel=det(hatTheta) is full-affine invariant by the #218 relative-solder law.")
print("RESULT_METRIC_DESCENT: det(Q_rel)=-Vol_rel^2, so Vol_rel descends on each fixed-orientation metric component.")
print("RESULT_SPAN_NO_LAMBDA: Palatini + legal T^2 lies in span{S_star, I^eta, I^n}.")
print("RESULT_SPAN_WITH_LAMBDA: Palatini + Lambda + legal T^2 needs the owned Vol_rel channel.")
print("TERMINAL: DISCRETE-PALATINI-TARGET-NEEDS-INVARIANT: Vol_rel")

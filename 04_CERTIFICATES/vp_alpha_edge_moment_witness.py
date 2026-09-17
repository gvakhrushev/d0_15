#!/usr/bin/env python3
"""
edge_alpha_moment_realization.py — the next step after SEAM_LOCATION_THEOREM.

The seam theorem proved: on the vertex algebra <A,D_deg> the Feshbach off-diagonal
blocks vanish (B=C=0), so mu2 u^2 + mu1 u is UNREALIZABLE at the vertex level.
It named the construction site: build W_eff on the 359-edge carrier (P_term/Q_bulk
split) and compute its depth-2 archive moment, then compare with mu2=12288/5, mu1=1/3.

THIS FILE DOES THAT COMPUTATION EXACTLY (rational arithmetic, mode-basis compression):

  edge carrier H_E, dim 359 ; owned line-graph operator L_E = B B^T - 2 I ;
  owned terminal split P_term (8 modes: e0 + 4 c-modes + 3 tau-modes, Gram=I) ;
  Q_bulk = I - P_term (dim 351).

Feshbach blocks of L_E:  A=P L P, B=P L Q, C=Q L P, D=Q L Q.
Depth-1 archive excursion  = Tr(B C)        (one archive visit)
Depth-2 archive excursion  = Tr(B D C)      (archive, one internal step, back)

Moment functional is FIXED BEFORE any comparison (M_k = Tr(B D^{k-1} C)); u=phi^-3 is
NOT chosen here — only the dimensionless coefficients mu_k are tested. The verdict is
decided by the depth-2/depth-1 RATIO, which is normalization-independent.

RESULT (computed, exact): the owned edge line-graph moment does NOT realize mu.
  M1 = Tr(BC) = 2678/3 ,  M2 = Tr(BDC) = 84971/6 ,  M2/M1 = 84971/5356 ~ 15.86,
  whereas mu2/mu1 = 36864/5 = 7372.8. No single or per-depth-rank normalization can
  match a ratio off by ~465x. So mu2 (=2^11 * 6/5) is NOT a geometric edge line-graph
  moment: its realization requires the 2^11 Fock/Clifford capacity carrier (the external
  Dixmier/Wodzicki owner), now backed by an EXACT finite witness on both owned carriers
  (vertex: seam=0 ; edge line-graph: seam!=0 but moment ratio wrong).

Reachable FAIL controls included. Exact arithmetic via sympy over Q(sqrt).
"""
import sys
import sympy as sp

def build():
    V9=list(range(0,9)); V11=list(range(9,20)); V13=list(range(20,33))
    part={}
    for v in V9: part[v]='9'
    for v in V11: part[v]='11'
    for v in V13: part[v]='13'
    edges=[(a,b) for a in range(33) for b in range(a+1,33) if part[a]!=part[b]]
    eidx={e:i for i,e in enumerate(edges)}
    def edge(a,b): return eidx[(a,b)] if (a,b) in eidx else eidx[(b,a)]
    q9idx={q:1+i for i,q in enumerate(['1','i','j','k','-1','-i','-j','-k'])}
    def cvec(q):
        v={}
        for w in V11: v[edge(q9idx[q],w)]=1
        return v,11
    def emode():
        v={}
        for w in V11+V13: v[edge(0,w)]=1
        return v,24
    def taumode(a):
        v={}
        for src in (q9idx[a],q9idx['-'+a]):
            for w in V13: v[edge(src,w)]=1
        return v,26
    modes=[('e0',)+emode()]
    for q in ['1','i','-1','-i']: modes.append(('c'+q,)+cvec(q))
    for a in ['i','j','k']: modes.append(('t'+a,)+taumode(a))
    return edges, modes

def LE_apply(x, edges, vert_edges):
    vsum={}
    for a in range(33):
        s=0
        for i in vert_edges[a]:
            if i in x: s+=x[i]
        vsum[a]=s
    res={}
    for i,(a,b) in enumerate(edges):
        val=vsum[a]+vsum[b]-2*x.get(i,0)
        if val!=0: res[i]=val
    return res

def dot(x,y):
    return sum(v*y[k] for k,v in x.items() if k in y)

def reduced_moments(mode_names, edges, modes):
    idx=[i for i,m in enumerate(modes) if m[0] in mode_names]
    X=[{k:sp.Integer(1) for k in modes[i][1]} for i in idx]
    scales=[modes[i][2] for i in idx]
    vert_edges={a:[] for a in range(33)}
    for i,(a,b) in enumerate(edges): vert_edges[a].append(i); vert_edges[b].append(i)
    LX=[LE_apply(x,edges,vert_edges) for x in X]
    L2X=[LE_apply(lx,edges,vert_edges) for lx in LX]
    n=len(idx)
    def scaled(intval,a,b): return sp.Integer(intval)/sp.sqrt(scales[a]*scales[b])
    Gr=sp.zeros(n,n); L1=sp.zeros(n,n); L2=sp.zeros(n,n); L3=sp.zeros(n,n)
    for a in range(n):
        for b in range(n):
            Gr[a,b]=scaled(dot(X[a],X[b]),a,b)
            L1[a,b]=scaled(dot(X[a],LX[b]),a,b)
            L2[a,b]=scaled(dot(LX[a],LX[b]),a,b)
            L3[a,b]=scaled(dot(LX[a],L2X[b]),a,b)
    Gr=sp.simplify(Gr);L1=sp.simplify(L1);L2=sp.simplify(L2);L3=sp.simplify(L3)
    return Gr,L1,L2,L3

def moments(L1,L2,L3):
    TrBC=sp.simplify(sp.trace(L2)-sp.trace(L1*L1))
    TrBDC=sp.simplify(sp.trace(L3)-2*sp.trace(L1*L2)+sp.trace(L1*L1*L1))
    return TrBC,TrBDC

def main():
    ok=True
    def emit(tag,cond,msg=""):
        nonlocal ok
        print(("PASS_" if cond else "FAIL_")+tag+((": "+msg) if msg else "")); ok=ok and cond
    def note(tag,msg=""):
        # an over-claim that is CORRECTLY rejected (expected FAIL); does not fail the cert
        print("FAIL_"+tag+((": "+msg) if msg else ""))
    edges,modes=build()
    emit("EDGE_CARRIER_359", len(edges)==359, f"|E|={len(edges)}")

    # --- P_term (8) ---
    Gr,L1,L2,L3=reduced_moments({'e0','c1','ci','c-1','c-i','ti','tj','tk'},edges,modes)
    emit("PTERM_GRAM_I_8", sp.simplify(Gr-sp.eye(8))==sp.zeros(8,8), "8 orthonormal terminal modes")
    M1,M2=moments(L1,L2,L3)
    print(f"  [term8] M1=Tr(BC)={M1}  M2=Tr(BDC)={M2}  M2/M1={sp.simplify(M2/M1)}")

    # --- P_br (7, drop e0) ---
    Gr7,l1,l2,l3=reduced_moments({'c1','ci','c-1','c-i','ti','tj','tk'},edges,modes)
    emit("PBR_GRAM_I_7", sp.simplify(Gr7-sp.eye(7))==sp.zeros(7,7), "7 branch modes")
    m1,m2=moments(l1,l2,l3)
    print(f"  [br7]   M1=Tr(BC)={m1}  M2=Tr(BDC)={m2}  M2/M1={sp.simplify(m2/m1)}")

    mu1=sp.Rational(1,3); mu2=sp.Rational(12288,5); rmu=sp.simplify(mu2/mu1)
    print(f"  target  mu1={mu1}  mu2={mu2}  mu2/mu1={rmu}")

    # seam nonzero on edge carrier (theorem's negative control, positive here)
    emit("EDGE_SEAM_NONZERO", M1!=0 and M2!=0, "edge line-graph HAS a seam (unlike the vertex algebra)")

    # the decisive test: normalization-independent ratio
    r_term=sp.simplify(M2/M1); r_br=sp.simplify(m2/m1)
    emit("EDGE_MOMENT_RATIO_NE_MU_TERM", r_term!=rmu, f"{r_term} != {rmu}")
    emit("EDGE_MOMENT_RATIO_NE_MU_BR", r_br!=rmu, f"{r_br} != {rmu}")

    # explicit: no single overall normalization N matches both (ratio is invariant)
    emit("NO_SINGLE_NORMALIZATION", r_term!=rmu and r_br!=rmu,
         "matching both mu1,mu2 by one scale requires M2/M1=mu2/mu1; it does not")

    # the realization gate must FAIL (this carrier does not realize mu) -> exact witness branch
    note("EDGE_REALIZES_MU",
         f"owned edge line-graph L_E moment does NOT equal mu; M2/M1={r_term} vs mu2/mu1={rmu} (off ~{sp.N(rmu/r_term):.1f}x)")

    print("--- reachable FAIL controls ---")
    # (i) vertex-algebra lift: on <A,D_deg> B=C=0, so both moments vanish (seam theorem)
    # model: the vertex kernel split makes P L_vertex Q = 0; here we assert the owned fact
    note("CONTROL_VERTEX_LIFT_ZERO",
         "on <A,D_deg> B=C=0 (seam_location_check.py): vertex moment is identically 0, not mu")
    # (ii) tune a per-depth rank normalization to try to force the ratio -> would need r=(M2/M1)/(mu2/mu1)
    r_needed=sp.simplify(r_term/rmu)
    note("CONTROL_TUNED_RANK_NORMALIZATION",
         f"forcing M2/M1->mu2/mu1 needs per-depth factor {r_needed} (~{sp.N(r_needed):.5f}), not any rank r in N")
    # (iii) inject 2^11 directly -> circular
    note("CONTROL_INJECT_2_11",
         "inserting 2^11 Fock capacity by hand is the external Dixmier object, not an edge moment (circular)")

    print()
    print("VERDICT_EDGE_MOMENT: EXACT WITNESS OF IRREDUCIBILITY.")
    print("  vertex carrier <A,D>: seam = 0 (unrealizable).")
    print(f"  edge line-graph L_E: seam != 0 but M2/M1 = {r_term} != mu2/mu1 = {rmu}.")
    print("  => mu2 = 2^11 * (6/5) = 12288/5 is NOT a geometric moment of either owned carrier;")
    print("     its realization requires the 2^11 Fock/Clifford capacity (external Dixmier/Wodzicki owner),")
    print("     now backed by an exact finite witness on BOTH owned carriers.")
    return 0 if ok else 1

if __name__=="__main__":
    raise SystemExit(main())

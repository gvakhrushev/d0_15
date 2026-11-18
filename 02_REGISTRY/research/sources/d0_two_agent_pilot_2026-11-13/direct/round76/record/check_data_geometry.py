"""Certify the local rank of a single fixed eight-CX measurement of primary DATA/SITE."""
import json
from pathlib import Path
import sys

import numpy as np
from scipy import linalg, sparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"geometry"))
import check_invisible_geometry as geo


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def sum_ball(lhs,rhs):
    a,da = lhs
    b,db = rhs
    return a+b, 1.000001*(da+db+3e-16*(np.abs(a)+np.abs(b)))+1e-290


def scalar_ball(x, k):
    a,da = x
    c = float(k.lo + (k.hi-k.lo)/2)
    dc = max(c-float(k.lo),float(k.hi)-c)*1.000001 + 1e-290
    return c*a, 1.000001*(abs(c)*da+dc*(np.abs(a)+da)+3e-16*abs(c)*np.abs(a))+1e-290


def derivative_matrix(terms, index):
    rows,cols,vals,radii = [],[],[],[]
    for term in terms:
        m = np.flatnonzero(term.j==index)
        rows.extend(term.r[m])
        cols.extend(term.c[m])
        vals.extend(term.dv[m])
        radii.extend(term.dv_err[m]+5e-15*np.abs(term.dv[m]))
    def mat(values):
        return sparse.csr_matrix((values,(rows,cols)),shape=(geo.N,geo.N))/16
    return mat(vals), 1.000001*mat(radii)


def dot_by_site(lhs,rhs):
    x,dx = [v.reshape(256,1024) for v in lhs]
    y,dy = [v.reshape(256,1024) for v in rhs]
    def dot(a,b):
        return np.einsum("si,si->s",a,b,optimize=False)
    mid = dot(x,y)
    # gamma_2048<2.3e-13, also covers the contract of 1024 products
    # with any reduction order or FMA and the separate positive sums.
    rad = dot(np.abs(x),dy)+dot(dx,np.abs(y)+dy)+1e-12*dot(np.abs(x),np.abs(y))
    return mid,1.000001*rad+1e-290


def selected_minor(J,err):
    # Floating QR and inverse choose a candidate. Only the enclosure of
    # R*J_true-I below is used to establish invertibility on actual columns.
    pivot = linalg.qr(J.T,mode="economic",pivoting=True)[2][:128]
    A,E = J[pivot],err[pivot]
    R = linalg.solve(A,np.eye(128),check_finite=True)
    def mm(a,b):
        return np.einsum("ik,kj->ij",a,b,optimize=False)
    c = mm(R,A)
    defect = np.abs(c-np.eye(128))+mm(np.abs(R),E)+3e-14*mm(np.abs(R),np.abs(A))
    upper = 1.000001*float(np.max(np.sum(defect,axis=1)))+1e-15
    require(upper < 1, "true selected 128x128 minor: Neumann certificate")
    uniform_response = (1-upper)/(1.000001*float(np.max(np.sum(np.abs(R),axis=1))))
    return {"certified_inverse_defect":upper,"lower_response_infty":uniform_response,
            "raw_bit_pattern_indices":[int(i) for i in pivot]}


def read_site(J,radius,p):
    # The two possible canonical target states are v and Xv. No known-one,
    # free blank or pre-existing sharp measurement of the site is used.
    distances = np.array([[bin(x^r).count("1") for x in range(256)] for r in range(256)])
    powers = [p]
    for _ in range(15):
        powers.append(powers[-1]*p)
    vals = np.array([float(x.lo+(x.hi-x.lo)/2) for x in powers])
    eps = np.array([1.000001*max(v-float(x.lo),float(x.hi)-v)+1e-290 for v,x in zip(vals,powers)])
    M,delta = vals[7+distances],eps[7+distances]
    def mm(a,b):
        return np.einsum("ik,kj->ij",a,b,optimize=False)
    eff = mm(M,J)
    er = mm(M,radius)+mm(delta,np.abs(J)+radius)+8e-14*mm(M,np.abs(J))
    return eff,1.000001*er+1e-290


def main():
    terms,_,cols,_ = geo.assemble()
    p = geo.heat.P
    pref = (-2*p*p,-2*p*p.sqrt())
    A = geo.matrix_ball(terms,[1]*16)
    C = (cols,np.full(cols.shape,5e-17))
    ac = geo.ball_apply(A,C)
    u = geo.ball_apply(A,ac,transpose=True)
    states = [sum_ball(C,scalar_ball(u,pref[0])), scalar_ball(u,pref[1])]
    J = np.zeros((2,256,128))
    E = np.zeros_like(J)
    for col,idx in enumerate(geo.ACTIVE):
        dA = derivative_matrix(terms,idx)
        da = geo.ball_apply(dA,C)
        du = sum_ball(geo.ball_apply(A,da,transpose=True),geo.ball_apply(dA,ac,transpose=True))
        for b in (0,1):
            mid,rad = dot_by_site(states[b],scalar_ball(du,pref[b]))
            J[b,:,col],E[b,:,col] = 2*mid,2*rad
    result = {}
    for b in (0,1):
        read,err = read_site(J[b],E[b],p)
        result[b] = {"sharp_site":selected_minor(J[b],E[b]),
                     "eight_actual_noisy_reads":selected_minor(read,err)}
        q,qe = dot_by_site(states[b],states[b])
        mass = float(np.sum(q))
        width = 1.000001*float(np.sum(qe)+1e-13*np.sum(np.abs(q)))+1e-290
        result[b]["blank_label_total_mass"] = [mass-width,mass+width]
        require((mass>.99 if b==0 else 3e-6<mass<4e-6),"original blank event")
    print(json.dumps(result,sort_keys=True))


if __name__ == "__main__":
    main()

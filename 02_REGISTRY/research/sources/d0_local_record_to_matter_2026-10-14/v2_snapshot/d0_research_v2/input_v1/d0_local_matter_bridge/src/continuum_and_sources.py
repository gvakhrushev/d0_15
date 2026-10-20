"""Finite numerical diagnostics and analytic-limit constants.
Numerical roots here are not the existence proof: see interval_l8.py and the report.
"""
from __future__ import annotations
import json
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.optimize import root
from scipy.special import logsumexp

ROOT=Path(__file__).resolve().parents[1]

def limit_constants():
    mp.mp.dps=60
    def moment(a,n):
        Z=1+2*mp.fsum(mp.exp(-a*k*k) for k in range(1,30))
        return 2*mp.fsum(mp.mpf(k)**n*mp.exp(-a*k*k) for k in range(1,30))/Z
    a=mp.findroot(lambda a:moment(a,2)-mp.mpf(1)/4,(mp.mpf('1.6'),mp.mpf('2')))
    beta=mp.log(2);d=a/(4*beta*mp.pi**2)
    m4,m6=moment(a,4),moment(a,6)
    d2=(1-4*m4+4*a*(m6-m4/4))/(48*beta*(m4-mp.mpf(1)/16))
    o2=1/(8*beta)
    return {'a_limit':str(a),'g_diagonal_limit':str(d),'diag_Lminus2_coefficient':str(d2),
            'offdiag_Lminus2_coefficient':str(o2),'moment4':str(m4),'moment6':str(m6),
            'sum_cutoff_for_diagnostics':29,'proof':'infinite theta sums, strict monotonicity, dominated Gaussian convergence and a nondegenerate moment Jacobian'}

def finite(L,guess):
    beta=np.log(2);ks=np.indices((L,)*4).reshape(4,-1).T
    zs=L*np.expm1(2j*np.pi*ks/L)
    A=np.sum(np.abs(zs)**2,axis=1);B=np.abs(zs.sum(axis=1))**2-A
    features=np.column_stack([A,B]);lam1=4*L*L*np.sin(np.pi/L)**2
    def compute(x):
        energies=features@x
        prob=np.exp(-beta*energies-logsumexp(-beta*energies))
        means=prob@features;centered=features-means
        return means-np.array([lam1,0]),-beta*centered.T@(prob[:,None]*centered)
    ans=root(lambda x:compute(x),guess,jac=True,tol=1e-10)
    d,o=ans.x
    G=np.full((4,4),o);np.fill_diagonal(G,d)
    vals=features@ans.x
    prob=np.exp(-beta*vals-logsumexp(-beta*vals))
    shell=np.zeros(len(ks))
    for r in range(4):
        for sign in (1,L-1):
            tup=[0]*4;tup[r]=sign
            shell[np.ravel_multi_index(tup,(L,)*4)]=1/8
    diff=shell-prob
    # Entire complex 4x4 moment: inversion symmetry makes its imaginary part zero.
    moment=zs.conj().T@(diff[:,None]*zs)
    # All local linear-link matrix derivatives reduce to this complex moment.
    edge_phase=np.exp(2j*np.pi*ks/L)
    C=zs.conj().T@(diff[:,None]*edge_phase)
    from_moment=moment/L-np.diag(moment)[:,None]/(2*L)
    link_coeffs=np.empty((4,4,4))
    n_sites=L**4
    for r in range(4):
        for a in range(4):
            for b in range(4):
                K=np.zeros((4,4));K[a,b]=1
                vector=G[:,r]*np.trace(K)-(G@K)[:,r]
                link_coeffs[r,a,b]=(L/n_sites*np.dot(C[:,r],vector)).real
    # Positivity and shell ordering are numerical here, rigorous at L=8 in companion.
    eig=np.linalg.eigvalsh(G);exc=vals[(vals>1e-8)&(np.abs(vals-d*lam1)>1e-8)]
    labels=[(r,s) for r in range(4) for s in range(r,4)]
    packed=[(1 if r==s else 2)*moment[r,s].real for r,s in labels]
    return {'L':L,'status':'NUMERICAL_SCOUT_NOT_EXACT_CERTIFICATE','solver_reported_success':bool(ans.success),
        'g_diagonal':float(d),'g_offdiagonal':float(o),'G_eigenvalues':eig.tolist(),
        'first_matter_energy':float(d*lam1),'heat_mean_energy':float(prob@vals),
        'moment_residual_packed10':packed,'max_moment_imaginary':float(np.max(abs(moment.imag))),
        'max_linear_link_source64':float(np.max(abs(link_coeffs))),
        'max_link_moment_identity_error':float(np.max(abs(C-from_moment))),
        'next_shell_gap':float(np.min(exc)-d*lam1),'raw_field_sites':L**4,
        'geometric_Fock_dimension':16,'minimal_purifying_record_dimension':128,
        'complete_heat_dimension_with_record':16*128*L**4,
        'explicit_pure_matter_normalization':1,'physical_D0_admission':False},ans.x

def main():
    lim=limit_constants();rows=[];guess=np.array([.07035,.00442])
    for L in (8,12,16,24,32):
        row,guess=finite(L,guess);rows.append(row)
        print(L,row['g_diagonal'],row['g_offdiagonal'],max(abs(x)for x in row['moment_residual_packed10']),row['max_linear_link_source64'])
    data={'continuum_diagnostics':lim,'finite_rows':rows,
          'statements_not_claimed':['native archive-projection compatibility','Einstein field equations','stability in all matter directions','pi0-to-common-Hodge generator identity']}
    (ROOT/'results/refinement_and_sources.json').write_text(json.dumps(data,indent=2)+'\n')
    print('LIMIT',json.dumps(lim,indent=2))
if __name__=='__main__':main()

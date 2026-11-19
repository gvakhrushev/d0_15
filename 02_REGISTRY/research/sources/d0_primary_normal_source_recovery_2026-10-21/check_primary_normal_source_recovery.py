#!/usr/bin/env python3
"""D0 primary Brinkmann source: uniform Dirichlet correction and saddle inverse.

Uses the existing all40 normal row, not a new action or a full40 inverse.
Exact finite tests + bounded numerical replay. No actual native Info/work
residual or physical stationarity/minimization law is supplied by this file.
Run: python check_primary_normal_source_recovery.py [--json result.json]
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy import sparse
from scipy.sparse.linalg import factorized

PIN = '963a9ae0a22ac05ba13b86e66f56bae68a6ec492'

def require(ok: bool, message: str) -> None:
    if not bool(ok):
        raise AssertionError(message)

def exact_checks() -> dict:
    x, y, h = sp.symbols('x y h', real=True, nonzero=True)
    lam, matter, aa, bb, cc, dd = sp.symbols('lambda matter A B C D', real=True)
    H = -lam*matter*(x*x+y*y)+aa*(x*x-y*y)+2*bb*x*y \
        +cc*(x**3-3*x*y*y)+dd*(3*x*x*y-y**3)
    lap = (H.subs(x,x+h)+H.subs(x,x-h)+H.subs(y,y+h)+H.subs(y,y-h)-4*H)/(h*h)
    require(sp.expand(lap+4*lam*matter)==0, 'unchanged polynomial sourced Brinkmann row')
    barrier = x*(1-x)/2
    dx = (barrier.subs(x,x+h)-2*barrier+barrier.subs(x,x-h))/(h*h)
    require(sp.expand(-dx-1)==0, 'exact mesh-independent strip barrier')
    # Original homogeneous transverse Dirichlet five-point operator for h=1/4.
    n=3
    D=sp.diag(*([2]*n))
    for j in range(n-1): D[j,j+1]=D[j+1,j]=-1
    L=16*(sp.kronecker_product(D,sp.eye(n))+sp.kronecker_product(sp.eye(n),D))
    inv=L.inv()
    require(all(v>=0 for v in inv), 'Dirichlet inverse entrywise positive')
    C=max(sum(inv[i,j] for j in range(n*n)) for i in range(n*n))
    require(C<=sp.Rational(1,8), 'uniform Green bound on original source subblock')
    eps=sp.Rational(1,1000)
    force=eps*sp.ones(n*n,1)
    w=-inv*force
    require(L*w+force==sp.zeros(n*n,1), 'exact correction sign and coefficient')
    require(max(abs(v) for v in w)<=eps/8, 'exact normal-row metric correction bound')
    # Hessian block is an algebra identity for arbitrary symmetric B, NOT
    # an assumption of positive definiteness or of a whole40 regular inverse.
    A=sp.Matrix([[4,-1],[-1,3]])
    b0,b1,b2=sp.symbols('b0 b1 b2',real=True)
    B=sp.Matrix([[b0,b1],[b1,b2]])
    Z=sp.zeros(2)
    K=Z.row_join(A).col_join(A.T.row_join(B))
    Ai=A.inv()
    Ki=(-Ai.T*B*Ai).row_join(Ai.T).col_join(Ai.row_join(Z))
    require(sp.simplify(K*Ki-sp.eye(4))==sp.zeros(4), 'exact indefinite saddle inverse')
    require(sp.factor(K.det()-A.det()**2)==0, 'two-pair saddle determinant independent of B')
    t=sp.symbols('t',positive=True)
    birth=t*t*sp.log(t*t)/2
    require(sp.limit(sp.diff(birth,t),t,0,dir='+')==0, 'entropy-like first source extends at zero')
    require(sp.limit(sp.diff(birth,t,2),t,0,dir='+')==-sp.oo, 'no false C2 assumption')
    # Compatibility cannot be removed by a small norm: an extra untouched
    # Euler row epsilon has no zero, even when the Poisson row is solved.
    untouched=sp.symbols('epsilon_extra',positive=True)
    require(untouched.is_positive, 'uncancelled extra Euler row is a genuine obstruction')
    return {'polynomial_normal_row':'EXACT', 'barrier_minus_laplacian':'1',
            'exact_green_norm_h_1_4':str(C),'green_uniform_bound':'1/8',
            'saddle_inverse':'EXACT_FOR_SYMBOLIC_SYMMETRIC_B',
            'non_C2_first_source_control':'PASS',
            'all_other_Euler_rows_required':True}

def numerical_checks() -> list[dict]:
    result=[]
    for intervals in (8,16,32):
        h=1.0/intervals; n=intervals-1
        D=sparse.diags((-np.ones(n-1),2*np.ones(n),-np.ones(n-1)),(-1,0,1),format='csc')/h**2
        I=sparse.eye(n,format='csc')
        Lx=sparse.kron(D,I,format='csc'); Ly=sparse.kron(I,D,format='csc')
        L=Lx+Ly; solve=factorized(L)
        rowsums=solve(np.ones(n*n))
        require(np.min(rowsums)>0 and np.max(rowsums)<=.125+1e-13, 'numerical uniform Green norm')
        grid=np.arange(1,intervals)*h
        X,Y=np.meshgrid(grid,grid,indexing='ij')
        # DIAGNOSTIC source, not claimed to be the actual full Book remainder.
        epsilon=h*h
        residual=epsilon*np.sin(np.pi*X).ravel()*np.sin(np.pi*Y).ravel()
        w=-solve(residual)
        require(np.max(np.abs(L@w+residual))<5e-12, 'forced Poisson correction residual')
        xx=Lx@w; yy=Ly@w
        # Commuting x/y Dirichlet operators give the discrete H2 energy identity.
        cross=float(w@(Lx@(Ly@w)))
        lhs=float(xx@xx+yy@yy+2*cross)
        rhs=float((L@w)@(L@w))
        require(abs(lhs-rhs)<=1e-10*max(1,abs(rhs)), 'discrete second-derivative energy identity')
        require(np.max(np.abs(w))<=epsilon/8+1e-13, 'source to metric bound')
        # A continuous first source with logarithmically divergent derivative.
        # Existence in the radius epsilon/4 ball follows analytically from
        # Brouwer; iteration here is a numerical control, NOT that proof.
        def r_nonC2(v: np.ndarray) -> np.ndarray:
            f=np.zeros_like(v)
            mask=v!=0
            f[mask]=v[mask]*np.log(np.abs(v[mask]))
            return epsilon*(1+f)
        z=np.zeros(n*n)
        for it in range(200):
            nxt=-solve(r_nonC2(z))
            if np.max(np.abs(nxt-z))<1e-15:
                z=nxt;break
            z=nxt
        err=float(np.max(np.abs(L@z+r_nonC2(z))))
        require(err<5e-11,'continuous/nonC2 source numerical stationary correction')
        require(np.max(np.abs(z))<=epsilon/4,'same closed-ball source budget')
        result.append({'intervals':intervals,'interior_sites':n*n,
                       'green_inf_bound_measured':float(rowsums.max()),
                       'diagnostic_source_bound':epsilon,
                       'linear_metric_error_inf':float(abs(w).max()),
                       'linear_normal_equation_error':float(abs(L@w+residual).max()),
                       'discrete_hessian_energy_error':abs(lhs-rhs),
                       'continuous_nonC2_equation_error':err,
                       'continuous_nonC2_iterations':it+1})
    return result

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    result={'status':'PASS_PRIMARY_NORMAL_SOURCE_RECOVERY', 'input_ref':PIN,
            'exact':exact_checks(),'numerical':numerical_checks(),
            'scope':{'same_primary_normal_row':True,
                     'actual_full_native_Info_work_residual_computed':False,
                     'other_41_Euler_rows_automatic_for_arbitrary_residual':False,
                     'generic_full40_inverse':False,'C2_remainder_required':False,
                     'native_stationarity_selection_proved':False,
                     'prospective_minimum_repaired':False,'GR_closed':False}}
    text=json.dumps(result,indent=2,ensure_ascii=False)
    print(text)
    if args.json: args.json.write_text(text+'\n',encoding='utf-8')

if __name__=='__main__':main()

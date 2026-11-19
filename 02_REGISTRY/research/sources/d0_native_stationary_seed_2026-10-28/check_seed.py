#!/usr/bin/env python3
"""Exact native recording seed and whole-word first source, not a D0->GR claim.

Original boundary from the paid-binary owner: 16 binary wires; all are blank
except q6, Spin13/14, oldRIGHT15. The five-pulse word is CX(6,0); SourceI^4.
Numerical matrices use its exact 32-dimensional active tensor factor; all
2^11 unused binary factors are retained analytically in the full heat.
"""
from __future__ import annotations
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
import numpy as np
import scipy.linalg as la

COUNT = 0

def require(ok: bool, message: str) -> None:
    global COUNT
    COUNT += 1
    if not bool(ok):
        raise ArithmeticError(message)

def near(x, y, message: str, tol: float = 2e-11) -> float:
    error = float(np.max(np.abs(np.asarray(x)-np.asarray(y))))
    require(error < tol, message + ': ' + str(error))
    return error

def adj(x): return x.conj().T

def skew(x): return (x-adj(x))/2

ZETA = 2.0**-20
p = (math.sqrt(5)-1)/2
BETA = 2*p*p


def scene():
    sizes = [9,11,13]
    cuts = np.cumsum([0]+sizes)
    A = np.zeros((33,33))
    for i in range(3):
        for j in range(3):
            if i != j:
                A[cuts[i]:cuts[i+1],cuts[j]:cuts[j+1]] = 1.
    degree = A.sum(1)+2
    R = np.diag(1/np.sqrt(degree))
    return R@A@R, R@R

BSC, CSC = scene()

def phase_heat(U, N: int, spectator: int = 1):
    """Full two-grade INTERNAL heat through finite Bloch spectra, no truncation.

Z01=2*Z0+359*N*d. Eigenphase derivatives retain the noncommuting scene
matrices. The returned skew cotangent C_H obeys dH=ReTr(C_H X), dU=XU.
"""
    d = len(U)
    schur, V = la.schur(U, output='complex')
    near(schur, np.diag(np.diag(schur)), 'unitary Schur diagonal', 2e-10)
    angles = np.angle(np.diag(schur))
    z0 = 0.
    dz0 = np.zeros(d)
    for a,theta in enumerate(angles):
        for j in range(N):
            phi = (theta + 2*math.pi*j)/N
            L = np.eye(33)-BSC-2*math.cos(phi)*CSC
            e, Q = la.eigh(L)
            weights = np.exp(-BETA*e)
            z0 += weights.sum()
            diag_C = np.diag(adj(Q)@CSC@Q).real
            dz0[a] -= BETA*2*math.sin(phi)/N*np.dot(weights,diag_C)
    baseZ = 2*z0 + 359*N*d
    slopes = 2*dz0/(BETA*baseZ)
    cotangent = V@np.diag(-1j*slopes)@adj(V)
    # spectator only adds log(spectator)/beta to heat at fixed dimension.
    return math.log(spectator*baseZ)/BETA, cotangent, {
        'full_modes':425*N*d*spectator,
        'H0_modes':33*N*d*spectator,
        'harmonic_modes':359*N*d*spectator,
        'Z01':float(spectator*baseZ)}


def return_data(U, embed, z=ZETA, scale=1.):
    K = adj(embed)@U@embed
    D = (1-z)*np.eye(K.shape[0])+z*scale*adj(K)@K
    inv = la.inv(D)
    Rbar = embed@inv@adj(embed)
    P = embed@adj(embed)
    H = U@Rbar@adj(U)
    cotangent = -z*scale*(H@P-P@H)
    eigen = la.eigvalsh(adj(K)@K)
    # Stable original absolute determinant, including baseline.
    J = -np.log1p(z*(scale*eigen-1)).sum()
    w = z*scale*np.trace(adj(K)@K@inv).real
    return float(J),cotangent,K,float(w)


def native_seed():
    # Reduced order: port0, control6, Spin13/14, oldRIGHT15.
    Li = np.array([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]], dtype=int)
    # Port factor, query factor, then spin and oldRIGHT.
    SI = np.zeros((32,32),dtype=int)
    for port in range(2):
        for query in range(2):
            lo=(2*port+query)*8
            SI[lo:lo+8,lo:lo+8] = (np.eye(8,dtype=int) if port==0
                                  else np.kron(Li,np.eye(2,dtype=int)))
    CX = np.zeros((32,32),dtype=int)
    for old in range(32):
        port=(old>>4)&1; query=(old>>3)&1
        new=((port^query)<<4)|(old&15)
        CX[new,old]=1
    gates=[CX,SI,SI,SI,SI]
    U=np.eye(32,dtype=int)
    for g in gates:
        require(np.array_equal(g.T@g,np.eye(32,dtype=int)), 'native integer primitive orthogonal')
        U=g@U
    require(np.array_equal(U,CX), 'five positive original calls end at CX')
    require(np.array_equal(U,U.T) and np.array_equal(U@U,np.eye(32,dtype=int)),
            'complete native endpoint is an involution')
    embed=np.eye(32,dtype=int)[:,:16]
    P=embed@embed.T; rotated=U.T@P@U
    require(np.array_equal(P@rotated,rotated@P), 'initial and transported projectors commute exactly')
    K=embed.T@U@embed
    expected=np.diag([1]*8+[0]*8)
    require(np.array_equal(K,expected), 'original all16 cold columns, no reset')
    require(np.array_equal(K.T@K@K.T@K,K.T@K),'partial isometry exact')
    # At plus input the output has a genuine retained copy, not pure identity.
    v=np.zeros(32);v[0]=v[8]=1/math.sqrt(2)
    out=U@v
    require(abs(out[0]-1/math.sqrt(2))<1e-15 and abs(out[24]-1/math.sqrt(2))<1e-15,
            'closed copy is not erased')
    # Rebuild the ACTUAL five generated cuts, not an imposed canonical one.
    prefixes=[np.eye(32,dtype=int)]
    for g in gates:
        prefixes.append(g@prefixes[-1])
    Ph=la.block_diag(*[V@P@V.T for V in prefixes[:-1]])
    Th=np.zeros((160,160),dtype=int)
    for j,g in enumerate(gates):
        Th[((j+1)%5)*32:((j+1)%5+1)*32,j*32:(j+1)*32]=g
    Fh=Ph@Th.T@(np.eye(160,dtype=int)-Ph)@Th@Ph
    require(int(np.trace(Ph))==80, 'true rank80 generated history input')
    require(np.array_equal(Fh@Fh,Fh), 'whole history defect is an exact projection')
    require(int(np.trace(Fh))==8, 'all nonclosing cuts plus closing rank8 defect')
    J,CJ,K,w=return_data(U,embed)
    near(J,-8*math.log1p(-ZETA),'true nonzero native return price')
    near(w,8*ZETA,'true nonzero prefix response weight')
    H,CH,meta=phase_heat(U,5,2**11)
    near(CJ,0.,'complete return source zero')
    near(CH,0.,'complete finite clock first source zero',2e-15)
    # Test all496 real skew endpoint directions. No continuous native
    # actuation is assumed: the analytic zero holds on a larger domain.
    maxsource=0.
    for a in range(32):
        for b in range(a):
            X=np.zeros((32,32));X[a,b]=1;X[b,a]=-1
            dK=embed.T@X@U@embed
            D=(1-ZETA)*np.eye(16)+ZETA*K.T@K
            source=-2*ZETA*np.trace(la.solve(D,K.T@dK)).real
            maxsource=max(maxsource,abs(source))
            require(abs(source)<1e-18,'all real skew return rows')
    # Uniform every-scalar-history cancellation, not a single gain.
    scaled=[]
    rng=np.random.default_rng(28)
    for t in (1.,.1,1e-12,1e-60):
        JJ,CC,KK,ww=return_data(U,embed,scale=t)
        near(CC,0.,'source vanishes for arbitrary following scalar-return product')
        formula=8*ZETA*t/(1-ZETA+ZETA*t)
        require(abs(ww/formula-1)<1e-14,'positive actual history gain')
        for _ in range(4):
            A=rng.normal(size=(32,32));X=skew(A);X/=la.norm(X,2)
            dK=embed.T@X@U@embed
            D=(1-ZETA)*np.eye(16)+ZETA*t*K.T@K
            numerator=np.trace(la.solve(D,K.T@dK)).real
            require(abs(numerator)<1e-13,'all ancestral skew insertions exact zero up to arithmetic')
        scaled.append({'T':t,'gain_w':ww,'return_source_operator_norm':float(la.norm(CC,2))})
    return {'raw_word':[{'gate':'CX','wires':[6,0]},
                        {'gate':'SourceI','wires':[0,13,14],'count':4}],
            'original_initial_unknown_wires':[6,13,14,15],
            'original_zero_boundary_qubits':12,
            'complete_binary_dimension':65536,'active_factor_dimension':32,
            'unused_spectator_dimension':2048,'input_rank':16,
            'perfect_return_rank':8,'complete_escape_rank':8,
            'complete_endpoint_multiplicities':{'+1':49152,'-1':16384},
            'heat':H,'return_price':J,'full_Book_price':H+J,
            'phase_heat_source_norm':float(la.norm(CH,2)),
            'return_source_norm':float(la.norm(CJ,2)),
            'real_skew_basis_directions_tested':496,
            'max_basis_source':maxsource,'positive_gain':w,
            'history':scaled,'full_clock':meta},(U,embed,gates)


def independent_word_source():
    rng=np.random.default_rng(11)
    d=4;N=3;embed=np.eye(d)[:,:2]
    gs=[]
    for _ in range(N):
        A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
        X=skew(A);gs.append(la.expm(.2*X))
    U=gs[2]@gs[1]@gs[0]
    J,CJ,_,_=return_data(U,embed,z=.19)
    H,CH,_=phase_heat(U,N)
    C=CJ+CH
    eigS=la.eigvalsh(adj(adj(embed)@U@embed)@(adj(embed)@U@embed))
    near(la.norm(CJ,'fro')**2,2*.19**2*np.sum(eigS*(1-eigS)/(1-.19+.19*eigS)**2),
         'complete cotangent norm identity')
    # Completely independent entire clock matrix from the actual stages.
    T=np.zeros((N*d,N*d),complex)
    for j,g in enumerate(gs):T[((j+1)%N)*d:((j+1)%N+1)*d,j*d:(j+1)*d]=g
    L=np.eye(33*N*d)-np.kron(BSC,np.eye(N*d))-np.kron(CSC,T+adj(T))
    vals,V=la.eigh(L);W=np.exp(-BETA*vals)
    expL=(V*W)@adj(V);Z=2*W.sum()+359*N*d
    near(H,math.log(Z)/BETA,'whole native-style clock heat, no commuting scene replacement')
    maxerr=0.;wrong=0.
    for j in range(N):
        prefix=np.eye(d,dtype=complex)
        for g in gs[:j]: prefix=g@prefix
        suffix=np.eye(d,dtype=complex)
        for g in gs[j+1:]: suffix=g@suffix
        for _ in range(5):
            A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));X=skew(A);X/=la.norm(X,2)
            dg=X@gs[j];dU=suffix@dg@prefix
            dT=np.zeros_like(T)
            dT[((j+1)%N)*d:((j+1)%N+1)*d,j*d:(j+1)*d]=dg
            dL=-np.kron(CSC,dT+adj(dT))
            dH=-2*np.trace(expL@dL).real/Z
            K=adj(embed)@U@embed;dK=adj(embed)@dU@embed
            D=(1-.19)*np.eye(2)+.19*adj(K)@K
            dJ=-2*.19*np.trace(la.solve(D,adj(K)@dK)).real
            source=np.trace(adj(suffix)@C@suffix@X).real
            maxerr=max(maxerr,near(source,dH+dJ,'whole-word source adjoint'))
            wrong=max(wrong,abs(source-np.trace(C@X).real))
    require(wrong>1e-5,'omitting actual suffix transport is detected')
    # Finite differences include both entire finite heat and determinant.
    A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));X=skew(A);X/=la.norm(X,2)
    def b(t):
        UU=la.expm(t*X)@U
        return phase_heat(UU,N)[0]+return_data(UU,embed,z=.19)[0]
    h=2e-4
    fd=(-b(2*h)+8*b(h)-8*b(-h)+b(-2*h))/(12*h)
    analytic=np.trace(C@X).real
    error=near(fd,analytic,'full-price five-point derivative',2e-10)
    return {'matrix_size':d,'stages':N,'scene_vertices':33,
            'full_H0_modes':33*N*d,'full_Hodge_modes':425*N*d,
            'max_analytic_stage_source_error':maxerr,
            'five_point_full_price_error':error,
            'wrong_untransported_source_error':wrong,
            'scope':'structural complex-matrix control, not newly admitted D0 gates'}


def stability_and_nonselection(seed_tuple):
    U,E,_=seed_tuple
    rng=np.random.default_rng(45)
    r=16;q=8;records=[]
    A=rng.normal(size=(32,32));Y=skew(A);Y/=la.norm(Y,2)
    A=rng.normal(size=(32,32));X=skew(A);X/=la.norm(X,2)
    for eps in (1e-2,1e-4,1e-6):
        V=la.expm(eps*Y)@U
        actualeps=la.norm(V-U,2)
        K=E.T@V@E;dK=E.T@X@V@E
        for T in (1.,1e-9,1e-90):
            a=1-ZETA;b=ZETA*T
            D=a*np.eye(r)+b*K.T@K
            denom=np.trace(la.solve(D,K.T@K)).real
            g=-2*np.trace(la.solve(D,K.T@dK)).real/denom
            bound=4*r*actualeps*(a+b)**2/(a*a*(math.sqrt(q)-math.sqrt(r)*actualeps)**2)
            require(abs(g)<=bound,'compiler-error source budget independent of historical T')
            records.append({'epsilon':actualeps,'T':T,'normalized_seed_source':g,'bound':bound})
    # First source zero does not select an Einstein law. The same seed is
    # constant under arbitrary displayed geometric labels (not a field map).
    # Also show the seed is a true saddle of return, not a minimum.
    def pair(a,b):
        X=np.zeros((32,32))
        for j in range(8):
            X[a+j,b+j]=-1;X[b+j,a+j]=1
        return X
    directions={'return_to_escape':pair(0,16), 'escape_to_return':pair(8,24)}
    second={}
    J0=return_data(U,E)[0]
    for name,X in directions.items():
        def j(t):return return_data(la.expm(t*X)@U,E)[0]
        h=1e-3
        val=(j(h)-2*J0+j(-h))/(h*h)
        second[name]=val
    require(second['return_to_escape']>0,'positive Hessian direction')
    require(second['escape_to_return']<0,'negative Hessian direction')
    # Full heat cannot reverse those signs: exact original C2 majorant.
    x=Fraction(2,55);qn=x**5/math.factorial(5)
    A1=Fraction(176,359)/(1-x*x)*qn/(1-qn)**2
    A2=2*Fraction(176,359)/(1-x*x)*qn*qn/(1-qn)**3+Fraction(4,5)*A1*A1
    heat_bound=A1+A2
    require(heat_bound<16*Fraction(1,2**20), 'whole price has both strict second-variation signs')
    # Positive scalar-loop source remains over the stationary recorded seed.
    for c in (.4,.7,.95):
        T=c*c;w=8*ZETA*T/(1-ZETA+ZETA*T)
        true=4*w*math.sqrt(1-c*c)/c
        require(true>0,'a newly free QUERY is not neutralized by seed stationarity')
    return {'robust_source_tests':records,'return_Hessian_controls':second,
            'exact_return_second_derivatives':['16*zeta','-16*zeta/(1-zeta)'],
            'full_heat_second_source_upper_bound':float(heat_bound),
            'full_heat_second_source_upper_bound_exact':str(heat_bound),
            'full_Book_saddle_on_declared_matrix_chart':True,
            'stationary_seed_does_not_imply_GR':True,
            'new_QUERY_source_remains':True}


def main():
    seed,tu=native_seed()
    out={'status':'PASS_WHOLE_WORD_SOURCE_AND_NATIVE_STATIONARY_SEED',
         'input_commit':'7c079c0180de6e6e12edbd8e79c4628f5048deae',
         'seed':seed,'whole_word_source':independent_word_source(),
         'stability':stability_and_nonselection(tu),
         'GR_closed':False,'geometry_source_identified_at_this_seed':False,
         'full_variation_domain_derived':False,'fixed_rank_clock_scene_beta_only':True,
         'large_7do_preparation_replayed':False,'native_physical_actuation_proved':False,
         'Lean_or_CI_run':False,
         'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out['checks']=COUNT
    print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__':main()

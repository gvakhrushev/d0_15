#!/usr/bin/env python3
"""Checks for exact clock-scene heat and full128 record holonomy transport.

General theorems are proved in THEOREM.md. Matrix checks below are finite
floating tests; coefficient/source majorants are outward interval bounds.
No GR closure, compulsory cut, or genuine 42-field writer is asserted.
"""
from __future__ import annotations
from pathlib import Path
import sys,json,hashlib
import numpy as np
from scipy.linalg import expm,expm_frechet
from mpmath import mp,iv
from scene_heat import (P,BETA,adj,projected_native,recorded_moments,
                        heat_from_coeffs,circuit_laplacian,scene_matrices,
                        scene_symbol,cycle_trace_from_unitary,native_feedback)
from interval_coefficients import coefficients,source_bounds,upper,lower
ROOT=Path(__file__).resolve().parent
CHECKS=[];ERRORS={}

def require(ok,name):
    if not bool(ok):raise RuntimeError(name)
    CHECKS.append(name)

def close(a,b,name,tol=2e-10):
    err=float(np.max(np.abs(a-b)));ERRORS[name]=err
    require(err<tol,name)

def pin_inputs():
    expected={'native_excerpt.py':'ed8a505d00337037d7aec976098717c3a4c43308',
              'native_weld.py':'de371c016bfd1bbc1222971589fc51ac6786c1eb'}
    for name,sha in expected.items():
        b=(ROOT/'inputs'/name).read_bytes()
        close_hash=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        require(close_hash==sha,'pinned '+name)

def toy_record_reflection():
    # Generic coisometry; tests the all-column XOR holonomy identity directly.
    rng=np.random.default_rng(624)
    d=2;jcount=4
    x=rng.normal(size=(jcount*d,d))+1j*rng.normal(size=(jcount*d,d))
    V0=np.linalg.qr(x)[0];N=adj(V0);Q=adj(N)@N
    spin=np.array([P,np.sqrt(P)])
    V=np.kron(spin[:,None],adj(N))
    U=np.eye(2*jcount*d)-2*V@adj(V)
    # Reorder port-major to literal fine alpha=2*j+b ordering.
    perm=np.array([b*jcount*d+j*d+k for j in range(jcount) for b in range(2) for k in range(d)])
    U=U[np.ix_(perm,perm)];V=V[perm]
    labels=2*jcount;D=len(U)
    copy=np.zeros((D*labels,D*labels))
    for a in range(labels):
        for k in range(d):
            for r in range(labels):
                copy[(a*d+k)*labels+(r^a),(a*d+k)*labels+r]=1
    Hol=copy@np.kron(U,np.eye(labels))
    close(adj(Hol)@Hol,np.eye(len(Hol)),'actual copied word unitary')
    sectors=[]
    for c in range(labels):
        signs=np.repeat([(-1)**((c&a).bit_count()) for a in range(labels)],d)
        A=adj(V)@(signs[:,None]*V)
        Dmat=np.diag(signs);Vc=Dmat@U
        close(A,adj(A),f'character {c} selfadjoint compression')
        T0=np.eye(d);T1=-A
        Vpower=np.eye(D,dtype=complex)
        for ell in range(1,7):
            Vpower=Vpower@Vc
            if ell>1:T0,T1=T1,-2*A@T1-T0
            traceD=signs.sum() if ell%2 else D
            rhs=traceD-d*(1+(-1)**ell)+2*np.trace(T1)
            close(np.trace(Vpower),rhs,f'character {c} exact reflection trace l{ell}')
        sectors.append(Vc)
    for ell in [1,2,3,4]:
        close(np.trace(np.linalg.matrix_power(Hol,ell)),
              sum(np.trace(np.linalg.matrix_power(v,ell)) for v in sectors),
              f'full retained record Fourier decomposition l{ell}',1e-9)
    # Full recorded holonomy, not the bare reflection, enters real clock heat.
    m=3;gates=[np.eye(len(Hol)),np.eye(len(Hol)),Hol]
    Lap=circuit_laplacian(gates,base=False)
    direct=np.exp(-BETA*np.linalg.eigvalsh(Lap)).sum()
    reduced=cycle_trace_from_unitary(Hol,m)
    close(direct,reduced,'full copied 384-dimensional clock heat',5e-9)
    return {'d':d,'labels':labels,'full_record_word_dimension':len(Hol),
            'direct_clock_laplacian_dimension':len(Lap)}

def scene_controls(coef):
    B,C,B3,C3=scene_matrices()
    sizes=(9,11,13);degs=(26,24,22)
    require(np.linalg.eigvalsh(B+2*C).max()<1+2e-14,'normalized product adjacency norm')
    for ct in [-1.0,-0.2,0.3,1.0]:
        full=np.linalg.eigvalsh(scene_symbol(ct))
        reduced=list(np.linalg.eigvalsh(np.eye(3)-B3-2*ct*C3))
        for n,d in zip(sizes,degs):reduced.extend([1-2*ct/d]*(n-1))
        close(np.sort(full),np.sort(reduced),'all33 scene eigenmodes cos='+str(ct))
        theta=np.arccos(ct)
        fourier=float(coef[0])+2*sum(float(coef[n])*np.cos(n*theta) for n in range(1,len(coef)))
        direct=np.trace(expm(BETA*(B+2*ct*C))).real
        close(fourier,direct,'positive Laurent heat coefficients cos='+str(ct),2e-12)
    # A genuinely moving, noncommuting, three-stage circuit, with all33 scene vertices.
    sigx=np.array([[0,1],[1,0]],complex);sigz=np.diag([1,-1])
    y=.173
    gates=[expm(1j*.31*sigz),expm(1j*y*sigx),expm(1j*.27*(sigx+sigz))]
    dgates=[np.zeros((2,2),complex),1j*sigx@gates[1],np.zeros((2,2),complex)]
    V=gates[2]@gates[1]@gates[0];dV=gates[2]@dgates[1]@gates[0]
    Lap=circuit_laplacian(gates)
    shiftjet=np.zeros((6,6),complex)
    for t,g in enumerate(dgates):shiftjet[((t+1)%3)*2:((t+1)%3+1)*2,t*2:(t+1)*2]=g
    dLap=-np.kron(C,shiftjet+adj(shiftjet))
    heat=expm(-BETA*Lap);Z=np.trace(heat).real
    direct_source=-np.trace(heat@dLap).real/Z
    vals=[2.0];ders=[0.0];Vp=np.eye(2,dtype=complex)
    for ell in range(1,22):
        ders.append(float((ell*np.trace(Vp@dV)).real));Vp=Vp@V
        vals.append(float(np.trace(Vp).real))
    hh,src,Zred=heat_from_coeffs(coef,3,np.array(vals),np.array(ders))
    close(Z,Zred,'198-dimensional actual normalized incidence heat',2e-10)
    close(direct_source,src,'198-dimensional Duhamel versus holonomy source',2e-14)
    lim=float(source_bounds(3,iv.mpf(str(BETA)),True)['first_source_constant_upper'])*np.linalg.norm(dV,2)
    require(abs(src)<lim,'general operator-norm source inequality on moving circuit')
    return {'direct_dimension':len(Lap),'source_direct':float(direct_source),
            'source_holonomy':src,'source_bound':lim}

def native_application(coef):
    m,A,dA=projected_native()
    close(sum(adj(k)@k for k in m['K']),np.eye(16),'native CPTP retained')
    require(A.shape==(128,16,16),'all128 archive character sectors retained')
    close(A[0],np.eye(16),'trivial character compression')
    close(dA[0],0,'trivial character derivative')
    close(A[1],-(P**3)*np.eye(16),'pure port character fixed compression')
    vals,ders=recorded_moments(A,dA,22)
    Ddim=2048*128
    close(vals[0],Ddim,'complete recorded holonomy dimension')
    close(vals[1],128*np.trace(np.eye(16)-2*P**2*m['D']).real,'first full recorded trace equals128 traceK0',3e-10)
    close(ders[1],-256*P**2*np.trace(m['dD']).real,'first full recorded source from original Delta',2e-12)
    # Independent finite differences rebuild all original Julia/Walsh blocks.
    eps=2e-4
    _,Ap,_=projected_native(np.log(1.25)+eps)
    _,Am,_=projected_native(np.log(1.25)-eps)
    vp,_=recorded_moments(Ap,np.zeros_like(Ap),22)
    vm,_=recorded_moments(Am,np.zeros_like(Am),22)
    err=np.max(np.abs((vp[1:9]-vm[1:9])/(2*eps)-ders[1:9]))
    require(err<2e-4,'independently rebuilt fine-record moment derivatives')
    ERRORS['native moment finite difference']=float(err)
    # Bound full-word derivative without constructing the 262144-square matrix.
    # U=I-2 vv* x Q; rank(dQ)<=32; ||dU||_op <=2||dQ||_F.
    L1=2*np.linalg.norm(m['dQ'],'fro')
    feedback=native_feedback(m['D'],m['dD'])
    rows=[]
    for stages in [3,8,11,15,16,32]:
        H,source,Z=heat_from_coeffs(coef,stages,vals,ders)
        const=float(source_bounds(stages,iv.mpf(str(BETA)),True)['first_source_constant_upper'])
        require(abs(source)<const*L1,f'native original clock-source bound m{stages}')
        # Stable finite difference: only varying winding terms, never subtract H~30.
        numerator=sum(2*float(coef[l*stages])*(vp[l]-vm[l])/(2*eps)
                      for l in range(1,min(len(vals),len(coef)//stages+1)) if l*stages<len(coef))
        denom=Z/(stages*np.exp(-BETA))
        finite_diff=numerator/(BETA*denom)
        rel=abs(source-finite_diff)/max(abs(source),1e-300)
        require(rel<2e-5,f'stable rebuilt native heat derivative m{stages}')
        rows.append({'m':stages,'H_graph':H,'d_rapidity_H_graph':source,
                     'abs_source_bound':const*L1,'relative_FD_error':rel,
                     'd_rapidity_J_pre':feedback['dJ'],
                     'heat_feedback_source_ratio':abs(source/feedback['dJ'])})
    # Bare original U has constant rank16 reflection spectrum; no record, no source.
    bare=np.array([2048.0]+[2032+16*((-1)**l) for l in range(1,23)])
    _,bare_source,_=heat_from_coeffs(coef,15,bare,np.zeros_like(bare))
    require(bare_source==0.0,'bare reflection heat exactly zero, recorded word not substituted')
    require(abs(rows[0]['d_rapidity_H_graph'])>1e-15,'full record generates nonzero heat source')
    return {'rapidity':float(np.log(1.25)),'boost_r':1/9,'derivative_coordinate':'rapidity, not r',
            'full_recorded_word_dimension':Ddim,'all_scene_modes':33,
            'norm_Dword_upper_from_Frobenius':float(L1),'clocks':rows,
            'bare_reflection_source':bare_source,'moments':vals[:9].tolist(),
            'moment_derivatives':ders[:9].tolist()}

def mixed_loop_guard():
    # Nonuniform gates over the scene produce a genuine length-four loop.
    # K2 x C15 has degree3. One vertical edge phase depends on y.
    m=15;y=.41;n=2*m
    A=np.zeros((n,n),complex);dA=np.zeros_like(A)
    for v in range(2):
        for t in range(m):
            i=v*m+t;j=v*m+(t+1)%m
            w=np.exp(1j*y) if (v,t)==(0,0) else 1.0
            dw=1j*w if (v,t)==(0,0) else 0.0
            A[j,i]=w;A[i,j]=np.conj(w);dA[j,i]=dw;dA[i,j]=np.conj(dw)
    for t in range(m):A[t,m+t]=A[m+t,t]=1.0
    L=np.eye(n)-A/3;dL=-dA/3
    moment_derivative=4*np.trace(np.linalg.matrix_power(L,3)@dL).real
    expected=-8*np.sin(y)/81
    close(moment_derivative,expected,'inhomogeneous scene has exact fourth-moment source')
    require(abs(moment_derivative)>0.01,'short mixed-loop source does not wait for15 windings')
    heat=expm(-BETA*L)
    source=-np.trace(heat@dL).real/np.trace(heat).real
    require(abs(source)>1e-7,'inhomogeneous negative control violates homogeneous tiny bound')
    return {'graph':'K2 x C15','phase':y,'d_trace_L4':float(moment_derivative),
            'exact_formula':'-8 sin(y)/81','d_heat':float(source)}

def main():
    pin_inputs();beta,coef,tail=coefficients()
    coefficient_midpoints=[float(c.mid) for c in coef]
    toy=toy_record_reflection();scene=scene_controls(coefficient_midpoints);native=native_application(coefficient_midpoints)
    guard=mixed_loop_guard()
    # These numerical bounds have deliberately rounded safe upper thresholds.
    for m,threshold in [(15,'1.120e-33'),(16,'2.430e-36'),(32,'8.632e-82')]:
        lim=source_bounds(m,beta,True)['first_source_constant_upper']
        require(mp.mpf(lim)<mp.mpf(threshold),f'outward uniform source constant m{m}')
    out={'status':'PASS_EXPLICIT_SCENE_CLOCK_INCIDENCE_HEAT_AND_FULL128_RECORD_SOURCE',
         'checks':len(CHECKS),'check_names':CHECKS,'matrix_errors':ERRORS,
         'toy_full_record_controls':toy,'direct_scene_controls':scene,'inhomogeneous_mixed_loop_guard':guard,
         'native_original_application':native,
         'uniform_coefficient_tail_upper':str(upper(tail)),
         'scene_graph':'K(9,11,13) x C_m, homogeneous circuit fibre, normalized degree d_v+2',
         'heat_operator':'genuine connection-incidence D*D; not paired cut C*C+CC*',
         'feedback_heat_added_twice':False,
         'compulsory_Book03_graph_or_cut_selected':False,
         'full42_field_writer_constructed':False,'GR_closed':False,
         'scope':'Exact analytical identities + interval majorants; native application double precision, not an interval root proof.'}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Narrow numerical controls for the fixed-dimensional coherent archive theorem.
This is NOT the original CAR16/full128 execution; it checks universal algebra
on two explicit internal CPTP examples and the original-form Golden port bound.
"""
import itertools
import math
import numpy as np


def assert_close(a, b, desc, tol=2e-11):
    if not np.allclose(a, b, atol=tol, rtol=tol):
        raise AssertionError(f'{desc}: {a} vs {b}')


def entropy(mat):
    w = np.linalg.eigvalsh((mat + mat.conj().T) / 2)
    if np.min(w) < -1e-10:
        raise AssertionError('nonpositive density')
    return -float(sum(t * math.log(t) for t in w if t > 1e-13))


def tprod(a, b):
    return np.kron(a, b)


def reset_example(n, alpha=0.4):
    rho = np.diag([2/3, 1/3]).astype(complex)
    S = np.diag(np.sqrt(np.diag(rho)))
    omega = np.array([1, 0, 0, 1], dtype=complex)
    psi = tprod(S, np.eye(2)) @ omega
    sigma = np.outer(psi, psi.conj())
    Kraus = [math.sqrt(alpha)*np.eye(2,dtype=complex)]
    for i in range(2):
        for j in range(2):
            K = np.zeros((2,2),complex)
            K[i,j] = math.sqrt((1-alpha)*rho[i,i].real)
            Kraus.append(K)
    assert_close(sum((k.conj().T @ k for k in Kraus)),np.eye(2),'Kraus trace preserving')
    # All ORIGINAL-STYLE chronological products; rank <= dim(DATA)*dim(R)=4.
    columns=[]
    for word in itertools.product(range(5), repeat=n):
        M=np.eye(2,dtype=complex)
        for k in word:
            M=Kraus[k]@M
        columns.append(tprod(M,np.eye(2))@psi)
    V=np.stack(columns,axis=1)
    theta=V@V.conj().T
    analytic=alpha**n*sigma+(1-alpha**n)*tprod(rho,rho.T)
    assert_close(theta,analytic,f'n={n} coherent archive compression',tol=3e-10)
    s_archive=entropy(theta)
    sing=np.linalg.svd(V,compute_uv=False)**2
    s_tape=-sum(float(t)*math.log(float(t)) for t in sing if t>1e-13)
    assert_close(s_archive,s_tape,f'n={n} same nonzero Schmidt spectrum')
    delta3=(1-alpha**3)*min(rho.diagonal()).real
    eig=np.linalg.eigvalsh(theta)
    assert eig[0]>=delta3*min(rho.diagonal()).real-1e-11 if n>=3 else True
    limiting=2*entropy(rho)
    assert abs(s_archive-limiting)<=2.0*math.log(1/(delta3/3))*((1-2*delta3)**(n//3))+1e-10 if n>=3 else True
    return (n,s_archive,limiting,theta.shape[0],len(columns))


def original_port_floor_test():
    p=(math.sqrt(5)-1)/2
    a=np.diag([1/4,4/9]).astype(float)
    eta=min(4*p**3*min(a.diagonal()),1-4*p**3*max(a.diagonal()))
    assert 0<eta<0.5
    # The EXACT original port effect R1=4*p^3 A is bounded on EVERY state.
    R=4*p**3*a
    for weight in [0,0.1,0.5,0.91,1]:
        state=np.diag([weight,1-weight])
        q=np.trace(R@state)
        assert eta-1e-12<=q<=1-eta+1e-12
    s=(0.5,2/3)
    w=np.array([1/x**2 for x in s]);w=w/w.sum()
    rates=4*p**3*np.array([x*x for x in s])
    for n in [1,2,3,4,5,6]:
        vals=[]
        for bits in itertools.product((0,1),repeat=n):
            k=sum(bits)
            vals.append(sum(w[i]*(rates[i]**k)*((1-rates[i])**(n-k)) for i in range(2)))
        assert_close(sum(vals),1,'port word normalization')
        assert min(vals)>=eta**n-1e-12
        h=-sum(v*math.log(v) for v in vals)
        h_eta=-(eta*math.log(eta)+(1-eta)*math.log(1-eta))
        assert h+1e-12>=n*h_eta
    return eta


def coherent_first_source_test():
    # Smooth INTERNAL reset channel example: native DATA fixed point is rho(y)
    # and the full fresh archive source is computed through 4x4 theta_n only.
    alpha, n = .4, 3
    a, b = 0.5, 2/3
    def theta_and_diff(a):
        den=a*a+b*b
        w0=b*b/den
        w1=a*a/den
        dw0=-2*a*b*b/(den*den)
        dw1=-dw0
        rho=np.diag([w0,w1]).astype(complex)
        drho=np.diag([dw0,dw1]).astype(complex)
        psi=np.array([math.sqrt(w0),0,0,math.sqrt(w1)],complex)
        dpsi=np.array([dw0/(2*math.sqrt(w0)),0,0,dw1/(2*math.sqrt(w1))],complex)
        sigma=np.outer(psi,psi.conj())
        dsigma=np.outer(dpsi,psi.conj())+np.outer(psi,dpsi.conj())
        factor=alpha**n
        T=factor*sigma+(1-factor)*np.kron(rho,rho)
        dT=factor*dsigma+(1-factor)*(np.kron(drho,rho)+np.kron(rho,drho))
        return T,dT
    T,dT=theta_and_diff(a)
    vals,U=np.linalg.eigh(T)
    assert min(vals)>0
    logT=(U*np.log(vals))@U.conj().T
    analytic=-np.trace(dT@logT).real
    step=1e-5
    numeric=(entropy(theta_and_diff(a+step)[0])-entropy(theta_and_diff(a-step)[0]))/(2*step)
    assert_close(analytic,numeric,'whole coherent archive first source',tol=1e-8)
    return analytic,numeric


def native_diagonal_no_mixing_control(n=5):
    # Genuine original-form Golden 1/2 port algebra on two commuting levels.
    # THIS control fails Choi strict positivity: the uniform floor claim must
    # NOT be asserted from endpoint Kraus completeness alone.
    p=(math.sqrt(5)-1)/2
    aa=np.array([.5,2/3]); nn=np.sqrt(1-aa*aa)
    K=[np.diag(1-2*p*p*aa*aa),np.diag(-2*p*p*aa*nn),
       np.diag(-2*p*math.sqrt(p)*aa*aa),
       np.diag(-2*p*math.sqrt(p)*aa*nn)]
    assert_close(sum(k.conj().T@k for k in K),np.eye(2),'QND Kraus TP')
    z=1/aa[0]**2+1/aa[1]**2
    rho=np.diag((aa**-2)/z)
    psi=np.array([math.sqrt(rho[0,0]),0,0,math.sqrt(rho[1,1])],complex)
    columns=[]
    pp={}
    for word in itertools.product(range(4),repeat=n):
        U=np.eye(2)
        for k in word: U=K[k]@U
        v=np.kron(U,np.eye(2))@psi
        columns.append(v)
        bits=tuple(int(k>=2) for k in word)
        pp[bits]=pp.get(bits,0.)+np.vdot(v,v).real
    V=np.stack(columns,axis=1)
    th=V@V.conj().T
    pf=np.array([np.vdot(v,v).real for v in columns])
    Hfine=-sum(t*math.log(t) for t in pf if t>0)
    Hport=-sum(t*math.log(t) for t in pp.values() if t>0)
    eta=min(4*p**3*min(aa**2),1-4*p**3*max(aa**2))
    heta=-(eta*math.log(eta)+(1-eta)*math.log(1-eta))
    assert Hport >= n*heta-1e-11
    assert Hfine >= Hport-1e-11
    assert Hfine-entropy(th)>=n*heta-math.log(4)-1e-11
    assert np.linalg.eigvalsh(th)[0]<1e-10
    return Hfine,Hport,entropy(th)


def coherent_c1_limit_control():
    alpha=.4
    a,b=.5,2/3
    den=a*a+b*b
    w0=b*b/den
    w1=1-w0
    dw0=-2*a*b*b/den**2
    dw1=-dw0
    rho=np.diag([w0,w1]).astype(complex)
    drho=np.diag([dw0,dw1]).astype(complex)
    psi=np.array([math.sqrt(w0),0,0,math.sqrt(w1)],complex)
    dpsi=np.array([dw0/(2*math.sqrt(w0)),0,0,dw1/(2*math.sqrt(w1))],complex)
    S0=np.outer(psi,psi.conj())
    dS0=np.outer(dpsi,psi.conj())+np.outer(psi,dpsi.conj())
    W=np.kron(rho,rho)
    dW=np.kron(drho,rho)+np.kron(rho,drho)
    entropy_source_limit=-2*(dw0*math.log(w0)+dw1*math.log(w1))
    errors=[]
    for n in (3,6,9,12):
        t=alpha**n
        T=t*S0+(1-t)*W
        dT=t*dS0+(1-t)*dW
        lam,U=np.linalg.eigh(T)
        assert min(lam)>0
        logT=(U*np.log(lam))@U.conj().T
        dEntropy=-np.trace(dT@logT).real
        errors.append(abs(dEntropy-entropy_source_limit))
    assert errors==sorted(errors,reverse=True)
    assert errors[-1]<2e-6
    return entropy_source_limit,errors


def main():
    rows=[reset_example(n) for n in (1,2,3,4)]
    eta=original_port_floor_test()
    first=coherent_first_source_test()
    limit,errors=coherent_c1_limit_control()
    Hfine,Hport,Scoh=native_diagonal_no_mixing_control()
    for row in rows:
        print('n=%d S_fresh=%.12f S_limit=%.12f DR=%d |words|=%d'%row)
    print('Golden original-form uniform port floor eta=%.12f'%eta)
    print('archive source analytic %.12f, finite difference %.12f'%first)
    print('C1 source limit %.12f; source errors %s'%(limit,[round(e,9) for e in errors]))
    print('QND negative control: fine Shannon %.8f, port Shannon %.8f, fresh coherent %.8f'%(Hfine,Hport,Scoh))
    print('PASS_CLOSED_NATIVE_ARCHIVE_FIXED_DIM (structural tests only)')

if __name__=='__main__':
    main()

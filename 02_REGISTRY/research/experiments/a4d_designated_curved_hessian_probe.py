#!/usr/bin/env python3
"""Literal Hessian at a numerical smooth connection continuation, L=8,12.

The metric is fixed as L changes, normal and curved at x1=0.  Translation
symmetry reduces the background solve to 24L coordinates; transverse Bloch
fibres retain the quarter resonance.  This is a floating-point connection
probe, not an exact joint-critical/source-compatible witness or a proof that
the numerical continuation equals the #216 cutoff parametrix.
"""
from __future__ import annotations
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import expm, logm, solve, svdvals

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'certificates'))
from a4d_designated_full_gap_check import GEN, PAIRS, SIG, STAR_MAP, flat_symbols

G = np.array(GEN,float)
I = np.eye(4)
ETA = np.diag(SIG)
SYM_G = (G[:,None]@G[None,:]+G[None,:]@G[:,None])/2
STAR = np.zeros((6,6))
for c,(r,s) in enumerate(STAR_MAP):
    STAR[r,c] = s
G2 = np.diag([SIG[a]*SIG[b] for a,b in PAIRS])


def orient(a,b):
    x = [a,b]+[r for r in range(4) if r not in (a,b)]
    return (-1)**sum(x[i]>x[j] for i,j in combinations(range(4),2))


def wedge(u,v):
    return np.array([u[a]*v[b]-u[b]*v[a] for a,b in PAIRS])


def linv(a):
    return ETA@a.T@ETA


def matprod(xs):
    ans = I
    for x in xs:
        ans = ans@x
    return ans


class Model:
    def __init__(self,n,amplitude):
        self.n = n
        self.amplitude = amplitude
        f = 1+amplitude*(1-np.cos(2*np.pi*np.arange(n)/n))
        self.solder = np.array([np.diag([1,1,x,x]) for x in f])
        self.weights = np.zeros((n,6,4,4))
        for x in range(n):
            for face,(a,b) in enumerate(PAIRS):
                u,v = [k for k in range(4) if k not in (a,b)]
                area = orient(a,b)*wedge(self.solder[x,:,u],self.solder[x,:,v])@G2@STAR
                for value,(aa,bb) in zip(area,PAIRS):
                    self.weights[x,face,aa,bb] += value*SIG[bb]/2
                    self.weights[x,face,bb,aa] -= value*SIG[aa]/2

    def identity(self):
        return np.broadcast_to(I,(self.n,4,4,4)).copy()

    def update(self,k,step):
        a = step.reshape(self.n,4,6)
        out = k.copy()
        for x in range(self.n):
            for r in range(4):
                out[x,r] = k[x,r]@expm(np.einsum('a,aij->ij',a[x,r],G))
        return out

    def face(self,k,x,face):
        r,s = PAIRS[face]
        # Link variables sit at 0, e_r, e_s, 0 in the actual plaquette.
        offsets = [np.zeros(4,int),np.eye(4,dtype=int)[r],
                   np.eye(4,dtype=int)[s],np.zeros(4,int)]
        roles = [r,s,r,s]
        loc = [((x+int(off[1]))%self.n,role) for off,role in zip(offsets,roles)]
        factors = [k[xx,rr] if i<2 else linv(k[xx,rr]) for i,(xx,rr) in enumerate(loc)]
        first = [factors[i]@G if i<2 else -G@factors[i] for i in range(4)]
        weight = self.weights[x,face]
        gradient = np.zeros((4,6))
        hessian = np.zeros((4,6,4,6))
        for i in range(4):
            left,right = matprod(factors[:i]),matprod(factors[i+1:])
            dp = left@first[i]@right
            gradient[i] = np.einsum('ab,iab->i',weight,dp)
            same = factors[i]@SYM_G if i<2 else SYM_G@factors[i]
            d2 = left@same@right
            hessian[i,:,i,:] = np.einsum('ab,ijab->ij',weight,d2)
            for j in range(i+1,4):
                between = matprod(factors[i+1:j])
                end = matprod(factors[j+1:])
                d2 = left@first[i][:,None]@between@first[j][None,:]@end
                block = np.einsum('ab,ijab->ij',weight,d2)
                hessian[i,:,j,:],hessian[j,:,i,:] = block,block.T
        value = float(np.sum(weight*matprod(factors)))
        return value,gradient,hessian,loc,offsets

    def assemble(self,k,transverse=(1,1,1),need_gradient=True):
        h = np.zeros((24*self.n,24*self.n),complex)
        grad = np.zeros(24*self.n)
        action = 0.
        for x in range(self.n):
            for f in range(6):
                value,d,dd,loc,offsets = self.face(k,x,f)
                action += value
                chars = [transverse[0]**off[0]*transverse[1]**off[2]*transverse[2]**off[3]
                         for off in offsets]
                for i,(xx,r) in enumerate(loc):
                    row = slice(24*xx+6*r,24*xx+6*r+6)
                    if need_gradient:
                        grad[row] += d[i]
                    for j,(yy,s) in enumerate(loc):
                        col = slice(24*yy+6*s,24*yy+6*s+6)
                        h[row,col] += np.conjugate(chars[i])*chars[j]*dd[i,:,j,:]
        assert np.max(abs(h-h.conj().T))<2e-12
        return action,grad,h

    def action(self,k):
        return sum(self.face(k,x,f)[0] for x in range(self.n) for f in range(6))


def flat_controls():
    model = Model(8,0.)
    k = model.identity()
    worst = 0.
    # Compare actual plaquette Hessian with independently reconstructed
    # mixed symbol, transposed for the owner Euler placement.
    for transverse,theta in [((1,1,1),0.),((1j,1j,1j),np.pi/2)]:
        _,grad,h = model.assemble(k,transverse)
        phase = np.exp(1j*theta*np.arange(8))
        embed = np.kron(phase[:,None],np.eye(24))/np.sqrt(8)
        block = embed.conj().T@h@embed
        z = [transverse[0],np.exp(1j*theta),transverse[1],transverse[2]]
        # These controls use exactly Gaussian-rational quarter phases.
        from a4d_designated_full_gap_check import QI,F
        zz = [QI(F(round(complex(x).real)),F(round(complex(x).imag))) for x in z]
        a,_ = flat_symbols(zz)
        a = np.array([[complex(x) for x in row] for row in a])
        worst = max(worst,float(np.max(abs(block-a.T))))
        assert np.max(abs(grad))<2e-13
    assert worst<2e-12
    # Directional finite differences check gradient and same-factor terms
    # at a curved, nonstationary exponential chart.
    model = Model(8,0.02); k = model.identity()
    rng = np.random.default_rng(310216)
    step = rng.normal(size=192)*0.002
    k = model.update(k,step)
    value,gradient,h = model.assemble(k)
    direction = rng.normal(size=192); direction /= np.linalg.norm(direction)
    eps = 2e-4
    plus = model.action(model.update(k,eps*direction))
    minus = model.action(model.update(k,-eps*direction))
    grad_error = abs((plus-minus)/(2*eps)-gradient@direction)
    hess_error = abs((plus+minus-2*value)/eps**2-np.real(direction@h@direction))
    assert grad_error<1e-7 and hess_error<1e-6
    return {'flat_symbol_max_error':worst,'curved_gradient_fd_error':float(grad_error),
            'curved_hessian_fd_error':float(hess_error)}


def probe(n,amplitude):
    k = Model(n,0.).identity()
    total_steps = 0
    # Continue from the flat identity; do not seed the finite z=1 Y vacuum.
    for amp in np.linspace(0,amplitude,5)[1:]:
        model = Model(n,float(amp))
        for iteration in range(12):
            _,grad,h = model.assemble(k)
            residual = np.max(abs(grad))
            if residual<2e-13:
                break
            step = solve(h.real,-grad,assume_a='sym')
            for damp in (1.,0.5,0.25,0.125,0.0625):
                trial = model.update(k,damp*step)
                _,new_grad,_ = model.assemble(trial)
                if np.max(abs(new_grad))<residual:
                    k = trial
                    total_steps += 1
                    break
            else:
                raise RuntimeError('Newton continuation failed')
        else:
            raise RuntimeError('Continuation did not converge')
    model = Model(n,amplitude)
    _,grad,h0 = model.assemble(k)
    _,_,hq = model.assemble(k,(1j,1j,1j),False)
    phase = np.exp(1j*np.pi*np.arange(n)/2)
    y = np.zeros(24); y[3:6] = [1,-1,1]
    packet = (phase[:,None]*y).reshape(-1)
    s0,sq = svdvals(h0),svdvals(hq)
    # The quotient fibre lifts to physical sites with the same multiplicity
    # in input and output, so its l1 ratios retain the unweighted norm.
    inverse0 = solve(h0,np.eye(24*n),assume_a='her')
    inverseq = solve(hq,np.eye(24*n),assume_a='her')
    log_size = max(float(np.linalg.norm(logm(k[x,r]),2)) for x in range(n) for r in range(4))
    result = {
        'L':n,'h':1/n,'fixed_metric_amplitude':amplitude,
        'normal_center_f_second_derivative':float(4*np.pi**2*amplitude),
        'newton_steps':total_steps,'connection_residual_infinity':float(np.max(abs(grad))),
        'max_link_log_operator_norm':log_size,'max_link_log_divided_by_h':n*log_size,
        'background_translation_fibre_sigma_min':float(s0[-1]),
        'background_translation_fibre_inverse_l1_norm':float(np.max(np.sum(abs(inverse0),axis=0))),
        'quarter_transverse_fibre_sigma_min':float(sq[-1]),
        'quarter_transverse_fibre_inverse_l1_norm':float(np.max(np.sum(abs(inverseq),axis=0))),
        'quarter_transverse_fibre_eight_smallest':list(map(float,sq[-8:])),
        'Y_plane_rayleigh_residual_l2':float(np.linalg.norm(hq@packet)/np.linalg.norm(packet)),
        'Y_plane_residual_ratio_l1':float(np.sum(abs(hq@packet))/np.sum(abs(packet))),
        'status':'NUMERICAL_CONNECTION_CONTINUATION_ONLY',
        'source':'No independent joint metric source is imposed.'}
    print(json.dumps(result,sort_keys=True),flush=True)
    assert result['connection_residual_infinity']<1e-11
    return result


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--periods',type=int,nargs='+',default=[8,12])
    parser.add_argument('--amplitude',type=float,default=0.02)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    assert all(n%4==0 and n>=4 for n in args.periods)
    report = {'metric':'diag(1,-1,-f(x1)^2,-f(x1)^2), f=1+epsilon*(1-cos(2*pi*x1))',
              'fixed_epsilon':args.amplitude,'controls':flat_controls(),
              'runs':[probe(n,args.amplitude) for n in args.periods],
              'nonclaims':['no exact joint source-compatible witness',
                           'no identification with the #216 cutoff parametrix',
                           'no all-fibre minimum or continuum rate from two grids']}
    if args.output:
        args.output.write_text(json.dumps(report,indent=2)+'\n')

#!/usr/bin/env python3
"""Internal adjacent-Jones transport in the actual Fibonacci algebra.

The level is a mathematical adapter argument. This supplies no autonomous
physical stage scheduler and does not postselect the prepared corner.
"""
import argparse
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import sys

_path=Path(__file__).with_name('a4d_native_fibonacci_record_activation.py')
_spec=importlib.util.spec_from_file_location('jones_fibonacci_input',_path)
E=importlib.util.module_from_spec(_spec);sys.modules[_spec.name]=E;_spec.loader.exec_module(E)
s=E.s;a,p,z=E.a,E.p,E.z


def include(blocks):
    """The actual unital AF inclusion, preserving all off-diagonal entries."""
    return [s.diag(*blocks),blocks[0]]


def corner_frames(n):
    """Jones frame in the native six-step path basis, not an abstract M_D."""
    sizes=E.counts(n);target=E.counts(n+6);parts=[]
    for j,rows in enumerate(E.segments(*sizes,6)):
        J=s.MutableSparseMatrix(target[j],sizes[j],{})
        for kind,path,offset in rows:
            if kind!=j:continue
            x1,x2,x3,x4,x5,x6=path
            if (x4,x5,x6)!=(x2,x1,j):continue
            for r in range(sizes[j]):J[offset+r,r]=E.root_weight(3+x3-j)
        parts.append(J)
    return parts


def adjacent_frames(n):
    old=corner_frames(n)
    return include(old),corner_frames(n+1)


@lru_cache(maxsize=8)
def operators(n):
    Gs,Fs=adjacent_frames(n);result=[]
    for G,F in zip(Gs,Fs):
        e=E.mat(G*G.T);f=E.mat(F*F.T);diff2=E.mat((e-f)*(e-f))
        skew=E.mat(f*e-e*f);I=s.eye(e.rows)
        Q=E.mat((2*p+3)*diff2/4)
        H=E.mat(I+(a-1)*Q+a*(3*p+5)*skew/2)
        R=E.mat(I-(1+p)*diff2/2+(2*p+3)*skew)
        # 1/(2ap)=a*(p+2)/2 in the positive golden branch.
        Z=E.mat(a*(p+2)*(F-p**3*G)/2)
        result.append({'G':G,'F':F,'Z':Z,'e':e,'f':f,'Q':Q,'H':H,'R':R})
    return result


def transport(n,blocks):
    """Actual inclusion followed by the explicitly constructed inner rotation."""
    parts=operators(n)
    return [E.mat(data['R']*x*data['R'].T) for data,x in zip(parts,include(blocks))]


def coarse(n,blocks):
    """Trace-adjoint coarse component; use decompose to retain the full residual."""
    parts=operators(n)
    X,Y=[E.mat(data['R'].T*x*data['R']) for data,x in zip(parts,blocks)]
    A,B=E.counts(n+6)
    return [E.mat(p*X[:A,:A]+p*p*Y),X[A:A+B,A:A+B]]


def decompose(n,blocks):
    """Return the coarse component AND every orthogonal fine residual entry."""
    part=coarse(n,blocks);lift=transport(n,part)
    return part,[E.mat(y-x) for y,x in zip(blocks,lift)]


def native_trace(level,blocks):
    return E.red(sum(p**(level+1+j)*s.trace(x) for j,x in enumerate(blocks)))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--level',type=int,default=0)
    args=parser.parse_args();n=args.level
    sizes=E.counts(n+7);rank=sum(v*v for v in E.counts(n+4))
    print(json.dumps({'scope':'EXACT_NATIVE_JONES_TRANSPORT_PHYSICAL_EXECUTION_OPEN',
      'input_AF_level':n+6,'output_AF_level':n+7,'output_block_sizes':sizes,
      'full_regular_dimension':sum(v*v for v in sizes),
      'golden_half_step_feedback_rank':rank,'squared_step_feedback_rank':rank,
      'adjacent_frame_overlap':'p^3 I',
      'ordinary_corner_coherence_defect_squared':'8 p^9',
      'internal_transport':'R=H^2; R alpha(e_n) R*=e_(n+1)',
      'physical_clock_or_preparation_law_derived':False},indent=2))


if __name__=='__main__':main()

#!/usr/bin/env python3
"""Exact full invariant preparation fiber. No physical admission is assigned."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

spec=importlib.util.spec_from_file_location('preparation_jones_input',Path(__file__).with_name('a4d_native_jones_record_transport.py'))
N=importlib.util.module_from_spec(spec);sys.modules[spec.name]=N;spec.loader.exec_module(N)
E=N.E;s=E.s;a,p=E.a,E.p


def field(value):
    """Exact Q(p,a) reduction, including reciprocal coefficients."""
    num,den=s.fraction(s.cancel(value));num=E.red(num);den=E.red(den)
    # All actual denominators below lie in Q(p). Rationalize its conjugate.
    if den.has(a):raise ValueError('DENOMINATOR_OUTSIDE_Q_P')
    conjugate=den.subs(p,-1-p)
    norm=E.red(den*conjugate)
    if norm==0:raise ZeroDivisionError('ZERO_ALGEBRAIC_DENOMINATOR')
    return E.red(num*conjugate)/norm


def fiber(level,lam,mu,ranks=None):
    X,Y=E.counts(level)
    if min(X,Y)<2:raise ValueError('BOTH_TRACELESS_BLOCKS_REQUIRED')
    wx,wy=p**(level+1),p**(level+2);u=E.red(wx*X);v=E.red(wy*Y)
    ax=field(((1-lam)*u-mu*v)/(X*X-1))
    ay=field(((1-lam)*v-mu*u)/(Y*Y-1))
    result={'sizes':(X,Y),'weights':(wx,wy),'u':u,'v':v,
      'lambda':lam,'mu':mu,'alpha':ax,'gamma':ay,
      'spectrum':[(lam,1),(mu,1),(ax,X*X-1),(ay,Y*Y-1)]}
    if ranks is not None:
        rx,ry=ranks;fx=s.Rational(rx*(X-rx),X*X-1);fy=s.Rational(ry*(Y-ry),Y*Y-1)
        K=E.red(u*fx+v*fy);J=E.red(v*fx+u*fy)
        c=E.red(wx*rx+wy*ry);mismatch=field((1-lam)*K-mu*J)
        result.update({'ranks':ranks,'K':K,'J':J,'corner_weight':c,
          'mismatch':mismatch,'t':field(c-mismatch),'fixed_t_mu_slope':field(-K/J)})
    return result


def jones_fiber(n,lam,mu):
    return fiber(n+7,lam,mu,E.counts(n+1))


def density(level,lam,mu):
    """Full sparse density, including cross-block central coherence."""
    data=fiber(level,lam,mu);X,Y=data['sizes'];d=X*X+Y*Y
    ex=s.MutableSparseMatrix(d,1,{});ey=s.MutableSparseMatrix(d,1,{})
    omega=s.MutableSparseMatrix(d,1,{});eta=s.MutableSparseMatrix(d,1,{})
    for i in range(X):
        ex[i*X+i,0]=1/s.sqrt(X)
        omega[i*X+i,0]=E.root_weight(level+1)
        eta[i*X+i,0]=E.root_weight(level+2)*s.sqrt(s.Rational(Y,X))
    for i in range(Y):
        index=X*X+i*Y+i;ey[index,0]=1/s.sqrt(Y)
        omega[index,0]=E.root_weight(level+2)
        eta[index,0]=-E.root_weight(level+1)*s.sqrt(s.Rational(X,Y))
    PX=s.SparseMatrix(d,d,{(i,i):1 for i in range(X*X)})-ex*ex.T
    PY=s.SparseMatrix(d,d,{(i,i):1 for i in range(X*X,d)})-ey*ey.T
    sigma=(lam*omega*omega.T+mu*eta*eta.T+data['alpha']*PX+data['gamma']*PY).applyfunc(field)
    return {**data,'sigma':sigma,'omega':omega,'eta':eta,'PX':PX,'PY':PY}


def fixed_t_path(n,lam,mu,step):
    data=jones_fiber(n,lam,mu)
    return jones_fiber(n,lam+step,field(mu+data['fixed_t_mu_slope']*step))


def reversible_rank_data(level):
    A,B=E.counts(level);d=A*A+B*B;D=(A+B)**2+A*A
    return {'coarse_dimension':d,'fine_dimension':D,'maximum_lossless_output_rank':2*d,
      'minimum_kernel_rank':D-2*d,'missing_fraction':str(s.Rational(D-2*d,D))}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--level',type=int,default=0)
    n=parser.parse_args().level;X,Y=E.counts(n+7);u=p**(n+8)*X;v=p**(n+9)*Y
    data=jones_fiber(n,p,field((1-p)*u*v))
    print(json.dumps({'scope':'FULL_INVARIANT_INTERFACE_NOT_PHYSICAL_ADMISSION',
      'native_Jones_level':n,'full_state_dimension':X*X+Y*Y,
      'independent_state_coordinates':['lambda','mu'],
      'fixed_joint_table_tangent':[1,str(data['fixed_t_mu_slope'])],
      'complete_Jones_price_derivative':'-1/(beta*lambda)',
      'full_lossless_refinement':reversible_rank_data(n+6),
      'whole_native_core_excluded':False},indent=2))


if __name__=='__main__':main()

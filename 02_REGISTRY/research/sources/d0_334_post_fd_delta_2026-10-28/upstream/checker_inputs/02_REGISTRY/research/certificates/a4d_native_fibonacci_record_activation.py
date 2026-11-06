#!/usr/bin/env python3
"""Exact native AF recording frames. Refinement is an explicit adapter, not a clock."""
import argparse
from functools import lru_cache
import json
import sympy as s

a,p,z=s.symbols('a p z',real=True)
_basis=s.groebner([a*a-p,p*p+p-1],a,p,domain=s.EX)


@lru_cache(maxsize=32768)
def red(value):
    if value==0:return s.S.Zero
    value=s.expand(value)
    return s.expand(_basis.reduce(value,auto=True)[1])


def mat(value):
    return value.applyfunc(red)


def zero(value):
    if isinstance(value,s.MatrixBase):
        return all(red(x)==0 for x in value)
    return red(value)==0


def counts(n):
    if not isinstance(n,int) or n<0:raise ValueError('NONNEGATIVE_AF_LEVEL')
    A,B=1,1
    for _ in range(n):A,B=A+B,A
    return A,B


def segments(A,B,r):
    # Each record is (old type, native inclusion path). The literal inclusion
    # concatenates X,Y in block 0 and repeats X in block 1.
    blocks=[[(0,())],[(1,())]]
    for _ in range(r):
        blocks=[[(j,path+(0,)) for block in blocks for j,path in block],
                [(j,path+(1,)) for j,path in blocks[0]]]
    result=[]
    for block in blocks:
        offset=0;row=[]
        for j,path in block:
            row.append((j,path,offset));offset+=(A,B)[j]
        result.append(row)
    return result


def root_weight(exponent):
    return p**(exponent//2)*(a if exponent%2 else 1)


def frame(n):
    sizes=counts(n);fine=counts(n+3);d=sum(k*k for k in sizes)
    block_segments=segments(*sizes,3)
    old=[(j,r,c) for j,k in enumerate(sizes) for r in range(k) for c in range(k)]
    new=[(v,r,c) for v,k in enumerate(fine) for r in range(k) for c in range(k)]
    index={coordinate:i for i,coordinate in enumerate(new)}
    V=s.MutableSparseMatrix(len(new),4*d,{})
    for column,(j,r,c) in enumerate(old):
        for v,rows in enumerate(block_segments):
            for kind,path,offset in rows:
                if kind==j:V[index[(v,offset+r,offset+c)],column]=root_weight(3+v-j)
        first,second=[off for kind,path,off in block_segments[0] if kind==j][:2]
        V[index[(0,first+r,second+c)],d+column]=1
        V[index[(0,second+r,first+c)],2*d+column]=1
        V[index[(0,first+r,first+c)],3*d+column]=s.sqrt(2)/2
        V[index[(0,second+r,second+c)],3*d+column]=-s.sqrt(2)/2
    return {'n':n,'old_sizes':sizes,'fine_sizes':fine,'old_coordinates':old,
            'fine_coordinates':new,'segments':block_segments,'V':V,'old_dimension':d}


def right_frames(n):
    sizes=counts(n);fine=counts(n+3);rows=segments(*sizes,3);result=[]
    for j,dj in enumerate(sizes):
        labels=[(v,k,row) for v in range(2) for k,segment in enumerate(rows[v])
                if segment[0]==j for row in range(fine[v])]
        index={label:i for i,label in enumerate(labels)}
        V=s.MutableSparseMatrix(len(labels),4*dj,{})
        first,second=[(k,item[2]) for k,item in enumerate(rows[0]) if item[0]==j][:2]
        for r in range(dj):
            for v in range(2):
                for k,(kind,path,offset) in enumerate(rows[v]):
                    if kind==j:V[index[(v,k,offset+r)],r]=root_weight(3+v-j)
            V[index[(0,second[0],first[1]+r)],dj+r]=1
            V[index[(0,first[0],second[1]+r)],2*dj+r]=1
            V[index[(0,first[0],first[1]+r)],3*dj+r]=s.sqrt(2)/2
            V[index[(0,second[0],second[1]+r)],3*dj+r]=-s.sqrt(2)/2
        result.append({'old_type':j,'spectator_dimension':dj,'dimension':len(labels),
                       'labels':labels,'V':V})
    return result


def record():
    return s.Matrix([[a,0,-p,0],[0,a,0,-p],[0,p,0,a],[p,0,a,0]])


def full_operators(V,d):
    # The whole complement is an identity sector; neither P nor Blank selects it.
    R=mat(V*V.T);I=s.eye(V.rows)
    U=s.kronecker_product(record(),s.eye(d))
    P=s.kronecker_product(s.diag(1,1,0,0),s.eye(d))
    B=s.kronecker_product(s.diag(1,0,1,0),s.eye(d))
    return mat(V*U*V.T+I-R),mat(V*P*V.T),mat(V*B*V.T),R


def activate(n,state):
    data=frame(n);d=data['old_dimension']
    if state.shape!=(d,1):raise ValueError('COMPLETE_OLD_GNS_VECTOR_REQUIRED')
    V=data['V']
    return mat(a*V[:,:d]*state+p*V[:,3*d:]*state)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--level',type=int,default=0)
    args=parser.parse_args();n=args.level;A,B=counts(n);C,D=counts(n+3);E,F=counts(n+6)
    print(json.dumps({'scope':'EXACT_AF_REPRESENTATION_NOT_PHYSICAL_REFINEMENT_TRIGGER',
      'base_level':n,'working_level':n+3,'operator_algebra_level':n+6,
      'coarse_dimension':A*A+B*B,'working_dimension':C*C+D*D,
      'full_regular_dimension':E*E+F*F,
      'whole_regular_two_tick_feedback_rank':C*C+D*D,
      'prepared_corner_probability':'p^6=4*delta0^2',
      'new_detail_norm_squared':'p^2*old_norm_squared',
      'physical_preparation_execution_or_time_law_derived':False},indent=2))


if __name__=='__main__':main()

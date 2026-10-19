#!/usr/bin/env python3
"""Exact two-original-null controls, a regular CLOSED 12-gate Lorentz atlas,
and an ordered-word information lower bound. Research-only, no native GR claim.
Run: python3 check_regular_two_null_atlas.py
"""
from collections import Counter
import sympy as s

I=s.eye(4)
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
def E(i,j):
    m=s.zeros(4); m[i,j]=1; return m
A=E(1,2)+E(2,0)  # ORIGINAL N_2
B=E(0,3)+E(3,1)  # ORIGINAL bar N_3
comm=lambda x,y:x*y-y*x
C=comm(A,B)
D=comm(A,C)
E3=comm(B,C)
F=comm(A,E3)
vec=lambda x:x.reshape(16,1)
basis=(A,B,C,D,E3,F)
assert all(x.T*eta+eta*x==s.zeros(4) for x in basis)
assert A**3==B**3==s.zeros(4)
for depth,terms,expected in [
    (1,(A,B),2),(2,(A,B,C),3),
    (3,(A,B,C,D,E3),5),(4,basis,6)]:
    rank=s.Matrix.hstack(*map(vec,terms)).rank()
    assert rank==expected
    print("LIE_DEPTH",depth,"RANK",rank)

def expnull(x,t):
    return I+t*x+t*t*(x*x)/2

# A six-forward/six-fixed-reverse word, at a NONZERO closed baseline.
X=(A,B,A,B,A,B)
t0=[s.Rational(x,40) for x in (1,1,1,1,2,1)]
G0=I
forward=[]
for x,t in zip(X,t0):
    g=expnull(x,t); forward.append(g); G0=G0*g
ret=[expnull(x,-t) for x,t in zip(X[::-1],t0[::-1])]
closed=I
for g in forward+ret:
    assert g.T*eta*g==eta
    closed=closed*g
assert closed==I
assert max(t0)<s.Rational(1,10) # inside existing Julia small chart

# d[ G(t) G(t0)^(-1) ]_t0 in a common left-trivialization:
# columns = Ad(prefix_j) X_j, j=0,...,5.
prefix=I
cols=[]
for x,g in zip(X,forward):
    cols.append(vec(prefix*x*prefix.inv()))
    prefix=prefix*g
J=s.Matrix.hstack(*cols)
assert J.shape==(16,6) and J.rank()==6
minor=s.factor(J[[0,2,3,6,7,11],:].det())
assert minor==s.Rational(1,26214400000000),minor
for j in range(6):
    x=s.Matrix(4,4,list(J[:,j]))
    assert x.T*eta+eta*x==s.zeros(4)
print("REGULAR_IDENTITY_WORD_12", closed==I)
print("ENDPOINT_JACOBIAN_RANK", J.rank())
print("EXACT_NONZERO_PIVOT_MINOR",minor)
print("ANALYTIC_IFT: local six-control coordinates on SO+(1,3) near I")

# Lie depth4 is essential for obtaining F from this specific two-generator pair.
assert F==E(0,0)-E(1,1)

# A second independent exact test: same signed primitive GATE MULTISET
# can have different noncommuting holonomy when the ORDER is changed.
def invert(word):
    flips={'a':'A','A':'a','b':'B','B':'b'}
    return [flips[t] for t in word[::-1]]
def commword(x,y):
    return x+y+invert(x)+invert(y)
WC=commword(['a'],['b'])
WE=commword(['b'],WC)
WF=commword(['a'],WE)
counts=Counter(WF)
assert len(WF)==22
assert counts==Counter({'a':5,'A':5,'b':6,'B':6})
sorted_word=list('a'*5+'A'*5+'b'*6+'B'*6)
assert Counter(sorted_word)==counts
t=s.Rational(1,40)
letter={'a':expnull(A,t),'A':expnull(A,-t),
        'b':expnull(B,t),'B':expnull(B,-t)}
def holo(word):
    ans=I
    for z in word: ans=ans*letter[z]
    return ans
H1=holo(WF)
H0=holo(sorted_word)
assert H0==I and H1!=I and H1.T*eta*H1==eta

# Exact truncated bivariate jet through total primitive degree four.
Z=s.zeros(4)
def jetexp(x,is_a,sign):
    ix=1 if is_a else 0
    iy=0 if is_a else 1
    return {(0,0):I,(ix,iy):sign*x,(2*ix,2*iy):x*x/2}
atoms={'a':jetexp(A,True,1),'A':jetexp(A,True,-1),
       'b':jetexp(B,False,1),'B':jetexp(B,False,-1)}
def mul(P,Q):
    ans={}
    for (a,b),u in P.items():
        for (c,d),v in Q.items():
            k=(a+c,b+d)
            if sum(k)>4:continue
            ans[k]=ans.get(k,Z)+u*v
    return {k:v for k,v in ans.items() if v!=Z}
def wordjet(word):
    res={(0,0):I}
    for z in word:res=mul(res,atoms[z])
    return res
assert wordjet(WC)[(1,1)]==C
assert wordjet(WE)[(1,2)]==E3
jet4=wordjet(WF)
assert jet4[(2,2)]==F
assert all(i+j>=4 or (i,j)==(0,0) for i,j in jet4)
print("DEPTH4_COMMUTATOR_BOOST_F",F!=Z)
print("COUNT_ONLY_HOLONOMY_NO_GO",H0==I and H1!=I)
print("PASS_TWO_NULL_REGULAR_ATLAS; GR_closed=false")

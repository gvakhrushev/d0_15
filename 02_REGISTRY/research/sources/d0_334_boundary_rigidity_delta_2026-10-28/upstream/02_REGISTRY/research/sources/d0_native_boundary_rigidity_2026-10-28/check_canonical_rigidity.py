#!/usr/bin/env python3
"""Exact algebraic identities for conditional metric HDA classification.
No construction of D0 symplectic form, generators, or lapse functions.
"""
import json
import sympy as s

def check(p,name):
    if not p:
        raise RuntimeError(name)

def sym(prefix):
    a,b,c,d,e,f=s.symbols(prefix+'0:6')
    return s.Matrix([[a,d,e],[d,b,f],[e,f,c]])

I=s.eye(3);S=sym('s');Z=sym('z');N=sym('n');X=sym('x')
def Cz(Z,S):
    return (S*Z+Z*S)/2-s.trace(S*Z)*I/2-s.trace(S)*Z/2

def matzero(A):
    return all(s.cancel(s.expand(v))==0 for v in A)

# Direct contraction with the principal metric variation of Ricci.
raw=0
for a in range(3):
    for b in range(3):
        ric_grad=(sum(N[a,k]*Z[k,b]+N[b,k]*Z[k,a] for k in range(3))
                  -s.trace(N)*Z[a,b]
                  -(1 if a==b else 0)*s.trace(N*Z))/2
        raw+=S[a,b]*ric_grad
check(s.expand(raw-s.trace(Cz(Z,S)*N))==0,'Ricci principal variation contraction')
check(matzero(Cz(Z,S)-Cz(Z,S).T),'Cz symmetric output')
check(s.expand(s.trace(X*Cz(Z,S))-s.trace(S*Cz(Z,X)))==0,'Cz selfadjoint')
check(matzero(Cz(Z,I)+(Z+s.trace(Z)*I)/2),'Cz evaluated at identity')
check(matzero(-2*Cz(Z,I)+s.trace(Cz(Z,I))*I/2-Z),'injective Z reconstruction')

b,rootq,k=s.symbols('b rootq k',nonzero=True)
L=lambda X:2*(X-s.trace(X)*I/2)/(b*rootq)
check(matzero(Cz(-b*I,L(X))+2*X/rootq),'DeWitt Hessian solves strong-HDA principal equation')
# Explicit six-coordinate matrices retain the Frobenius factors for off-diagonal entries.
pairs=[(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
basis=[]
for i,j in pairs:
    E=s.zeros(3);E[i,j]=1;E[j,i]=1;basis.append(E)
vec=lambda M:s.Matrix([M[i,j] for i,j in pairs])
C6=s.Matrix.hstack(*[vec(Cz(Z,E)) for E in basis])
L6=s.Matrix.hstack(*[vec(L(E)) for E in basis])
W=s.diag(1,1,1,2,2,2)
check(matzero(W*C6-C6.T*W),'six-coordinate Frobenius adjoint convention')
EinsteinC6=C6.subs({Z[i,j]:(-b if i==j else 0) for i,j in pairs})
check(matzero(EinsteinC6*L6+2*s.eye(6)/rootq),'full six-by-six strong-HDA principal composition')
Q=lambda X:s.trace(X*X)-s.trace(X)**2/2
Pi=sym('p');old=Pi+b*k*I
check(s.expand(Q(old)/b+k*s.trace(old)-Q(Pi)/b-s.Rational(3,2)*b*k*k)==0,'constant trace drift canonical completion')

# Six independent Ricci values exist at a normal-coordinate point in dimension 3.
# Algebraic Riemann tensor from an arbitrary Ricci tensor via the Schouten tensor.
R=sym('r');scal=s.trace(R);Sch=R-scal*I/4
Riem=[[[[I[i,k]*Sch[j,l]-I[i,l]*Sch[j,k]-I[j,k]*Sch[i,l]+I[j,l]*Sch[i,k]
          for l in range(3)] for k in range(3)] for j in range(3)] for i in range(3)]
RicRecovered=s.Matrix(3,3,lambda j,l:sum(Riem[i][j][i][l] for i in range(3)))
check(matzero(RicRecovered-R),'all six algebraic Ricci components realizable')

# Nonlinear curvature potential changes principal C_Z at fixed q,pi.
alpha=s.symbols('alpha',nonzero=True)
Zquad=-b*I+2*alpha*R
change=Cz(Zquad,L(X))-Cz(-b*I,L(X))
check(not matzero(change),'Ricci-squared nonlinearity changes principal HDA response')
Zf=-b*I+2*alpha*scal*I
change_f=Cz(Zf,L(X))-Cz(-b*I,L(X))
check(matzero(change_f-4*alpha*scal*X/(b*rootq)),'R-squared principal anomaly')

# Independent scalar-gradient flux calculation in six spatial components.
d11,d22,d12=s.symbols('d11 d22 d12')
D=s.Matrix([[d11,d12],[d12,d22]])
v=s.Matrix(3,2,s.symbols('v0:6'))
Gram=v.T*v/2
Glinear=s.trace(D*Gram)
flux=s.Matrix(3,2,lambda i,a:s.diff(Glinear,v[i,a]))
check(matzero(flux-v*D),'full scalar-gradient flux and off-diagonal factor')
n1,n2=s.symbols('nu1 nu2',real=True)
nu=s.Matrix([n1,n2])
F=(nu.T*D.inv()*nu)[0]/2
check(matzero(D*s.Matrix([s.diff(F,x) for x in nu])-nu),'reciprocal scalar momentum source')
check(matzero(D*s.hessian(F,(n1,n2))-s.eye(2)),'full two-scalar Hessian reciprocity')

# Actual nonlinear-gradient failure for a separated canonical kinetic term.
x11=s.symbols('x11',positive=True)
x22=s.symbols('x22',positive=True)
nonlinear_D=(1+2*alpha*(x11+x22))*s.eye(2)
check(matzero(nonlinear_D*nu-nu-2*alpha*(x11+x22)*nu),
      'nonlinear separated gradient anomaly')
check(not matzero(nonlinear_D*nu-nu),'nonlinear separated gradient defect is nonzero')

# A valid nonseparable escape on the same two-scalar carrier.
DBI=s.sqrt((1+n1*n1)*(1+2*x11))+n2*n2/2+x22
DBI_D=s.diag(s.diff(DBI,x11),s.diff(DBI,x22))
DBI_u=s.Matrix([s.diff(DBI,n1),s.diff(DBI,n2)])
check(all(s.simplify(t)==0 for t in DBI_D*DBI_u-nu),'nonseparable exact HDA matter control')
check(s.simplify(s.diff(DBI,n1,x11))!=0,'nonseparable control is actually mixed')

out={'scope':'conditional continuum canonical metric class; no native D0 bracket constructed',
     'sympy_version':s.__version__,
     'tests':['Ricci principal lapse contraction','symmetric output','selfadjoint Cz',
              'identity evaluation','injective Z reconstruction','DeWitt Hessian composition',
              'six-coordinate Frobenius adjoint convention','full six-by-six principal composition',
              'trace drift completion','six Ricci components realized','Ricci-square hostile control',
              'R-square anomaly coefficient',
              'full scalar-gradient flux and off-diagonal factor',
              'reciprocal scalar momentum source','full two-scalar Hessian reciprocity',
              'nonlinear separated gradient anomaly','nonlinear separated gradient defect is nonzero',
              'nonseparable exact HDA matter control',
              'nonseparable control is actually mixed'],
     'status':'PASS_EXACT_CANONICAL_AND_SCALAR_RIGIDITY_CONTROLS',
     'native_D0_phase_space_constructed':False,'GR_closed':False}
print(json.dumps(out,indent=2,sort_keys=True))

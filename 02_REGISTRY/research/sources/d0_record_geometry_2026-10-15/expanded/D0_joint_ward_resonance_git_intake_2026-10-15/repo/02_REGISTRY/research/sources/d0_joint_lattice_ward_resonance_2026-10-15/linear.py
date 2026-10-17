"""Literal naked-star joint flat symbol; no nonlinear gauge is installed."""
from pathlib import Path
import importlib.util,hashlib,tempfile
from itertools import combinations
import sympy as s

# Prefer a verified expanded input; otherwise consume the already-published capsule.
# Extraction is temporary, never a second repository owner.
UPSTREAM = Path(__file__).resolve().parent.parent/'d0_full_four_dimensional_sheet_2026-10-15'/'symbol.py'
_TEMP_INPUT=None
if not UPSTREAM.is_file():
    loader=Path(__file__).resolve().parent.parent/'d0_full4d_intake_2026-10-15'/'restore.py'
    raw=loader.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if blob!='1512bf6d2907209a753c7291fc7a1a47df5f81a7':raise RuntimeError('PUBLISHED_RESTORE_OWNER_CHANGED')
    spec=importlib.util.spec_from_file_location('d0_existing_full4d_intake',loader)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    _TEMP_INPUT=tempfile.TemporaryDirectory(prefix='d0-ward-owned-input-')
    UPSTREAM=mod.restore(Path(_TEMP_INPUT.name))/'symbol.py'
if hashlib.sha256(UPSTREAM.read_bytes()).hexdigest()!='37c2b21429c5e703068d2ac398160329e9728ffce480ec86fc57418813e90dab':
    raise RuntimeError('LITERAL_SYMBOL_INPUT_CHANGED')
_spec=importlib.util.spec_from_file_location('d0_declared_symbol_input',UPSTREAM)
if _spec is None or _spec.loader is None: raise RuntimeError('missing input symbol')
_owner=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_owner)
PAIR,eta,GEN,G2,STAR,wedge,symbol=[getattr(_owner,k) for k in ('PAIR','eta','GEN','G2','STAR','wedge','symbol')]
PACK=[(i,j) for i in range(4) for j in range(i,4)]

def mixed(z):
    """C=partial_a partial_g A: all ten true covariant Gram slots."""
    out=s.zeros(24,10);I=s.eye(4)
    for r,t in PAIR:
        u,v=[a for a in range(4) if a not in (r,t)]
        seq=[r,t,u,v];sg=(-1)**sum(seq[i]>seq[j] for i,j in combinations(range(4),2))
        for k,(a,b) in enumerate(PACK):
            V=s.zeros(4); V[a,b]=V[b,a]=1
            dE=eta*V/2
            dw=sg*(wedge(dE[:,u],I[:,v])+wedge(I[:,u],dE[:,v])).T*G2*STAR
            for alpha,G in enumerate(GEN):
                Ge=G*eta;val=(dw*s.Matrix([Ge[x,y] for x,y in PAIR]))[0]
                out[r*6+alpha,k]+=(1-1/z[t])*val
                out[t*6+alpha,k]+=(1/z[r]-1)*val
    return out.applyfunc(s.expand)

def joint(z):
    z=list(map(s.sympify,z))
    H=symbol(s.eye(4),z);C=mixed(z)
    Cd=mixed([1/x for x in z]).T
    return s.BlockMatrix([[s.zeros(10),Cd],[C,H]]).as_explicit()

def backward_lift(z):
    """Exact quadratic-null lift; different from the old forward coframe lift."""
    z=list(map(s.sympify,z))
    d=s.Matrix([1/x - 1 for x in z]);cols=[]
    for a in range(4):
        e=s.eye(4)[:,a]*d.T
        q=e.T*eta+eta*e
        omega=e-eta*q/2
        links=[(x-1)*omega for x in z]
        cols.append(s.Matrix([q[i,j] for i,j in PACK]+[A[i,j] for A in links for i,j in PAIR]))
    return s.Matrix.hstack(*cols).applyfunc(s.expand)

def simplify(M): return M.applyfunc(s.simplify)

def resonance():
    z=[s.S.One,s.I,s.I,s.S.One];J=joint(z);H=J[10:,10:];C=J[10:,:10]
    Z=s.Matrix.hstack(*J.nullspace())
    P=simplify(Z*(Z.conjugate().T*Z).inv()*Z.conjugate().T)
    R=simplify((J+P).inv()-P)
    G=backward_lift(z)
    Pg=simplify(G*(G.conjugate().T*G).inv()*G.conjugate().T)
    Pphysical=simplify(P-Pg)
    Y0=s.Matrix.hstack(*Pphysical.columnspace())
    # This is a coordinate change of the two-dimensional quotient, not a selector.
    Y=Y0*s.Matrix([[2,2],[0,1]])
    return dict(z=z,J=J,H=H,C=C,Z=Z,P=P,R=R,G=G,Pg=Pg,Pphysical=Pphysical,Y=simplify(Y))

def phase_jets(J,z,at):
    """Exact angle derivatives from Laurent coefficients, no angle samples."""
    D=[s.zeros(J.rows) for _ in range(4)]
    DD={(i,j):s.zeros(J.rows) for i in range(4) for j in range(i,4)}
    for aa in range(J.rows):
        for bb in range(J.cols):
            for term in s.Add.make_args(s.expand(J[aa,bb])):
                pp=term.as_powers_dict();powers=[int(pp.get(x,0)) for x in z]
                co=s.cancel(term/s.prod(x**e for x,e in zip(z,powers)))
                if not co.is_Rational: raise AssertionError(('not a rational Laurent coefficient',term))
                val=co*s.prod(s.sympify(x)**e for x,e in zip(at,powers))
                for i in range(4): D[i][aa,bb]+=s.I*powers[i]*val
                for i in range(4):
                    for j in range(i,4): DD[i,j][aa,bb]-=powers[i]*powers[j]*val
    return [v.applyfunc(s.expand) for v in D],{ij:m.applyfunc(s.expand) for ij,m in DD.items()}

def effective_jets(data=None):
    d=resonance() if data is None else data
    z=s.symbols('z0:4',nonzero=True);k=s.symbols('k0:4',real=True)
    D,DD=phase_jets(joint(z),z,d['z']);Y=d['Y'];R=d['R']
    U=[(a*Y).applyfunc(s.expand) for a in D]
    # Y*Y=I/7; multiplication by 7 reads this form in orthonormal coordinates.
    first=sum((7*k[i]*(Y.conjugate().T*D[i]*Y) for i in range(4)),s.zeros(2)).applyfunc(s.expand)
    second=s.zeros(2)
    for i in range(4):
        for j in range(i,4):
            c=Y.conjugate().T*DD[i,j]*Y/(2 if i==j else 1)-U[i].conjugate().T*R*U[j]
            if i!=j: c-=U[j].conjugate().T*R*U[i]
            second+=7*k[i]*k[j]*c.applyfunc(s.expand)
    return dict(k=k,D=D,DD=DD,first=simplify(first),second=simplify(second),tangent=simplify(second.subs(k[2],-k[1])))

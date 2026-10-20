"""Exact cubic-source control for the original six-plaquette crossed-null trial.

The coefficient ring is Q[a,b]/(a^3,b^3), with h=1, A=(1,0), B=(0,1).
The coframe is fixed to its affine crossed-null form. Links are exact truncated
exponentials of the continuum LC connection plus the published order-ab h/8
Cartan correction. This checks only whether a site-independent cubic link
correction closes all original Euler rows; it does not exclude spatially
variable links or lower-order coframe corrections.
"""
import itertools, sympy as s

MAX=2
I=s.eye(4); O=s.zeros(4); eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
E=lambda i,j:s.Matrix(4,4,lambda k,l:int(i==k and j==l))
N2,N3=E(1,2)+E(2,0),E(1,3)+E(3,0)
M2,M3=E(0,2)+E(2,1),E(0,3)+E(3,1)
Boost,Rot=E(1,1)-E(0,0),E(2,3)-E(3,2)
pairs=list(itertools.combinations(range(4),2))
G=[(E(i,j)-E(j,i))*eta for i,j in pairs]

class Jet:
    def __init__(self,c0=None,terms=None):
        self.c={} if terms is None else dict(terms)
        if terms is None and c0 is not None: self.c[(0,0)]=c0
    @staticmethod
    def co(p,q,x): return Jet(terms={(p,q):x})
    def __add__(self,d):
        if not isinstance(d,Jet): d=Jet(d)
        out=dict(self.c)
        for k,v in d.c.items(): out[k]=out[k]+v if k in out else v
        return Jet(terms=out)
    __radd__=__add__
    def __neg__(self): return Jet(terms={k:-v for k,v in self.c.items()})
    def __sub__(self,d): return self+(-d if isinstance(d,Jet) else -d)
    def __rsub__(self,d): return (-self)+d
    def __mul__(self,d):
        if not isinstance(d,Jet): d=Jet(d)
        out={}
        for (p,q),a in self.c.items():
            for (r,t),b in d.c.items():
                k=(p+r,q+t)
                if k[0]>MAX or k[1]>MAX: continue
                z=a*b
                out[k]=out[k]+z if k in out else z
        return Jet(terms=out)
    __rmul__=__mul__
    def __truediv__(self,d): return self*(s.Rational(1,1)/d)
    def __getitem__(self,ij):
        return Jet(terms={k:v[ij[0],ij[1]] for k,v in self.c.items()})
    def coeff(self,p,q,default=0): return self.c.get((p,q),default)
    def left(self,X): return Jet(X)*self
    def right(self,X): return self*Jet(X)
    def l_inv(self): return Jet(terms={k:eta*v.T*eta for k,v in self.c.items()})
    def copy(self):
        return Jet(terms={k:(v.copy() if isinstance(v,s.MatrixBase) else v) for k,v in self.c.items()})

def expj(A):
    out=Jet(I); term=Jet(I)
    for n in range(1,5):
        term=term*A/s.Integer(n)
        out=out+term
    return out

AA=(1,0); BB=(0,1)
dx=AA[0]*BB[0]; dy=AA[1]*BB[1]; wedge=AA[0]*BB[1]-AA[1]*BB[0]
CORR_HIGH=[{(2,1):O,(1,2):O} for _ in range(4)]
CORR=[
 s.Rational(1,8)*(dx*M2+dy*M3+wedge*Rot),
 s.Rational(1,8)*(dx*N2+dy*N3-wedge*Rot),
 s.Rational(1,8)*(wedge*(M3-N3)-dy*Rot),
 s.Rational(1,8)*(wedge*(N2-M2)+dx*Rot),
]

def coframe(z):
    x,y=z[2],z[3]
    H=Jet.co(1,0,AA[0]*x+AA[1]*y)
    J=Jet.co(0,1,BB[0]*x+BB[1]*y)
    return Jet(I)+(H*Jet(E(1,0)))/2+(J*Jet(E(0,1)))/2

def link(z,r,back=False):
    x,y=z[2],z[3]
    H=Jet.co(1,0,AA[0]*x+AA[1]*y)
    J=Jet.co(0,1,BB[0]*x+BB[1]*y)
    A=[Jet.co(1,0,v) for v in AA]
    B=[Jet.co(0,1,v) for v in BB]
    Q=H*J/4
    invOmega=Jet(1)+Q+Q*Q
    wb=[Jet(O),Jet(O),Jet(O),Jet(O)]
    for i in range(2):
        a=A[i]*invOmega/2
        b=B[i]*invOmega/2
        c=-(H*B[i]+J*A[i])*invOmega/8
        d=(J*A[i]-H*B[i])*invOmega/8
        Np=(N2,N3)[i]; Nm=(M2,M3)[i]
        wb[0]=wb[0]+Jet(Np)*a+Jet(Nm)*c
        wb[1]=wb[1]+Jet(Np)*c+Jet(Nm)*b
        wb[i+2]=wb[i+2]+Jet(Boost)*d
    ef=[[Jet(1),J/2,Jet(0),Jet(0)],
        [H/2,Jet(1),Jet(0),Jet(0)],
        [Jet(0),Jet(0),Jet(1),Jet(0)],
        [Jet(0),Jet(0),Jet(0),Jet(1)]]
    wc=[]
    for mu in range(4):
        W=Jet(O)
        for j in range(4): W=W+wb[j]*ef[j][mu]
        d=dict(W.c)
        if CORR[r]!=O: d[(1,1)]=d.get((1,1),O)+CORR[r]
        for key,matrix in CORR_HIGH[r].items():
            if matrix!=O: d[key]=d.get(key,O)+matrix
        W=Jet(terms=d)
        wc.append(W)
    U=expj(wc[r])
    return U.l_inv() if back else U

def shift(z,axis,k=1):
    p=list(z);p[axis]+=k;return tuple(p)
def edges(z,r,t):
    return ((z,r,False),(shift(z,r),t,False),(shift(z,t),r,True),(z,t,True))
one=Jet(I)
def scalar_pair(e,u,v,R):
    out=Jet(0); RR=R*Jet(eta)
    for a,b in pairs:
        c,d=[k for k in range(4) if k not in (a,b)]
        val=e[a,u]*e[b,v]-e[b,u]*e[a,v]
        out=out+s.LeviCivita(a,b,c,d)*val*RR[c,d]
    return out
def plaquette(z,r,t,target=None,axis=None,X=None):
    P=one; dP=Jet(O)
    for at,a,back in edges(z,r,t):
        U=link(at,a,back)
        hit=(X is not None and at==target and a==axis)
        dU=(U.right(-X) if back else U.left(X)) if hit else Jet(O)
        dP=dP*U+P*dU
        P=P*U
    return P,dP
def link_rows(z):
    result=[]
    for axis in range(4):
      for X in G:
        value=Jet(0)
        for r,t in pairs:
          if axis not in (r,t): continue
          other=t if axis==r else r
          u,v=[k for k in range(4) if k not in (r,t)]
          for base in (z,shift(z,other,-1)):
            P,dP=plaquette(base,r,t,z,axis,X)
            Pi=P.l_inv()
            dR=(dP+Pi*dP*Pi)/2
            value=value+s.LeviCivita(r,t,u,v)*scalar_pair(coframe(base),u,v,dR)
        result.append(value)
    return result
def replace_column(e,col,internal):
    q=e.copy()
    for k,m in q.c.items():
        for a in range(4): m[a,col]=int(k==(0,0) and a==internal)
    return q
def solder_rows(z):
    result=[Jet(0) for _ in range(16)];e=coframe(z)
    for r,t in pairs:
      u,v=[k for k in range(4) if k not in (r,t)]
      sign=s.LeviCivita(r,t,u,v)
      P,_=plaquette(z,r,t)
      R=(P-P.l_inv())/2
      for a in range(4):
        result[4*a+u]=result[4*a+u]+sign*scalar_pair(replace_column(e,u,a),u,v,R)
        result[4*a+v]=result[4*a+v]+sign*scalar_pair(replace_column(e,v,a),u,v,R)
    return result

def val_at(z,p,q):
    links=link_rows(z); solder=solder_rows(z)
    return [s.simplify(v.coeff(p,q)) for v in links], [s.simplify(v.coeff(p,q)) for v in solder]


def flat_hessian():
    M=s.zeros(24)
    for r,t in pairs:
        u,v=[k for k in range(4) if k not in (r,t)]
        sign=s.LeviCivita(r,t,u,v)
        for j,X in enumerate(G):
            for k,Y in enumerate(G):
                value=sign*scalar_pair(Jet(I),u,v,Jet(X*Y-Y*X)).coeff(0,0)
                M[6*r+j,6*t+k]=value
                M[6*t+k,6*r+j]=value
    return M

def nonzero_rows(values):
    return [(i,s.simplify(v)) for i,v in enumerate(values) if s.simplify(v)!=0]

def correction_matrix(c,axis):
    return sum((c[6*axis+j]*G[j] for j in range(6)),O)

def main():
    M=flat_hessian()
    assert M.rank()==24 and M.det()==256
    print('PASS exact homogeneous flat Cartan block: rank=24 det=256')
    origin=(0,0,s.Rational(0),s.Rational(0))
    neighbor=(0,0,s.Rational(1),s.Rational(0))
    for xy in (origin,neighbor):
        l,sr=val_at(xy,1,1)
        assert l==[0]*24 and sr==[0]*16
    print('PASS published order-ab correction: all 40 rows vanish at both exact control nodes')
    for pwr,expected_origin_coframe,expected_neighbor_links,expected_neighbor_coframe in (
      ((2,1),[(3,-s.Rational(1,32)),(13,-s.Rational(1,32))],
       [(11,-s.Rational(3,16)),(14,s.Rational(1,32)),(19,-s.Rational(1,32))],
       [(3,-s.Rational(1,32)),(13,-s.Rational(1,32))]),
      ((1,2),[(6,-s.Rational(1,32)),(8,-s.Rational(1,32))],
       [(0,s.Rational(1,16)),(4,s.Rational(1,16)),(15,-s.Rational(3,32)),(22,s.Rational(1,32))],
       [(4,-s.Rational(1,8)),(6,-s.Rational(1,32)),(8,-s.Rational(1,32))])):
        CORR_HIGH[:] = [{(2,1):O,(1,2):O} for _ in range(4)]
        f0=s.Matrix([v.coeff(*pwr) for v in link_rows(origin)])
        c=-M.inv()*f0
        for axis in range(4): CORR_HIGH[axis][pwr]=correction_matrix(c,axis)
        links0=[s.simplify(v.coeff(*pwr)) for v in link_rows(origin)]
        coframe0=[s.simplify(v.coeff(*pwr)) for v in solder_rows(origin)]
        links1=[s.simplify(v.coeff(*pwr)) for v in link_rows(neighbor)]
        coframe1=[s.simplify(v.coeff(*pwr)) for v in solder_rows(neighbor)]
        assert links0==[0]*24
        assert nonzero_rows(coframe0)==expected_origin_coframe
        assert nonzero_rows(links1)==expected_neighbor_links
        assert nonzero_rows(coframe1)==expected_neighbor_coframe
        print(f'PASS coefficient a^{pwr[0]} b^{pwr[1]}: homogeneous correction solves 24 link rows at origin')
        print('  origin coframe residual:',nonzero_rows(coframe0))
        print('  neighbor link residual:',nonzero_rows(links1))
        print('  neighbor coframe residual:',nonzero_rows(coframe1))
    CORR_HIGH[:] = [{(2,1):O,(1,2):O} for _ in range(4)]
    print('SCOPE: fixed affine coframe and spatially uniform cubic correction only; no no-go for spatially varying corrections or coframe modes.')

if __name__=='__main__':
    main()

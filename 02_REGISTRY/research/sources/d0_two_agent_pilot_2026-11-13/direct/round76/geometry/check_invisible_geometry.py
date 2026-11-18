"""Full pointer rows on independent inverse-leg scalings of the primary regulator."""
from fractions import Fraction as Q
from pathlib import Path
import sys
import numpy as np
from scipy import sparse,linalg
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/"round75/curvature"))
import check_local_coframe_source as heat
car=heat.car
N=2048
DIRECTIONS=[(car.site_index(x),j) for x in car.SITES_LIST if all(x[k] in (1,2) for k in (0,2,3)) for j in range(4)]
ACTIVE=np.array([4*i+j for i,j in DIRECTIONS])
GAMMA=(.5,2.,1.,1.)
EV=[m for m in range(16) if bin(m).count("1")%2==0]
OD=[m for m in range(16) if bin(m).count("1")%2]
def parity(k): return (-1)**bin(k).count("1")

class Atom:
    """One of the role terms, with each nonzero assigned to its own site/leg."""
    def __init__(self,r,c,j,v,parameter,derivative):
        self.r=np.array(r,dtype=int);self.c=np.array(c,dtype=int)
        self.j=np.array(j,dtype=int); self.v=np.array(v,dtype=float)
        assert np.bincount(self.j).max() <= 128
        self.dv=self.v*derivative[self.j]
        self.dv_err=np.abs(self.v)*8e-15
        self.Merr=sparse.csr_matrix((self.dv_err,(self.r,self.c)),shape=(N,N))
        self.M=sparse.csr_matrix((self.v*parameter[self.j],(self.r,self.c)),shape=(N,N))
    def bounded_pull(self,l,r):
        lc,le=l;rc,re=r
        ix=self.r; iy=self.c
        dot=lambda x,y:np.einsum('ij,ij->i',x,y)
        center=dot(lc[ix],rc[iy]); left=np.abs(lc[ix]);right=np.abs(rc[iy])
        radius=dot(le[ix],right+re[iy])+dot(left,re[iy])+2e-14*dot(left,right)
        radius=1.000001*radius+1e-290
        terms=self.dv*center
        local=np.bincount(self.j,weights=terms,minlength=1024)
        raw=np.abs(self.dv)*radius+self.dv_err*(np.abs(center)+radius)+5e-14*np.abs(terms)
        error=1.000001*np.bincount(self.j,weights=raw,minlength=1024)+1e-290
        return local,error
    def pull(self,l,r):
        dot=np.einsum('ij,ij->i',l[self.r],r[self.c])
        return np.bincount(self.j,weights=dot*self.dv,minlength=4*256)


def atom(role,leg,out_masks,in_masks,rowshift,colshift,param,deriv):
    vals=[(o,i,float(leg[mo][mi])) for o,mo in enumerate(out_masks)
           for i,mi in enumerate(in_masks) if leg[mo][mi]]
    rr=[];cc=[];jj=[];vv=[]
    for j,z in enumerate(car.SITES_LIST):
        k=car.site_index(car.step(z,role,rowshift)) if rowshift else j
        m=car.site_index(car.step(z,role,colshift)) if colshift else j
        for o,i,value in vals:
            rr.append(8*k+o);cc.append(8*m+i);jj.append(4*j+role);vv.append(value)
    return Atom(rr,cc,jj,vv,param,deriv)


def assemble():
    fr=car.actual_counts(heat.ROOT)
    p=(np.sqrt(5.)-1)/2
    t=np.repeat(p**3*np.sqrt(256*np.array(fr)/sum(fr)),4)
    g=np.tile(GAMMA,256)
    defect=np.sqrt(1-g*t*t)-1
    d_defect=g*t*t/(defect+1)
    ints=[heat.I.rational(Q(256*n,sum(fr))) for n in fr]
    ir=heat.I([v.lo for v in ints],[v.hi for v in ints]).sqrt()
    it=(heat.P*heat.P*heat.P)*ir
    for role in range(4):
        rad=(heat.I(1.)-it.square()*Q(GAMMA[role])).sqrt()
        df=it.square()*Q(GAMMA[role])/rad
        for nom,true in ((t[role::4],it),(defect[role::4],rad-1),(d_defect[role::4],df)):
            assert max(nom-true.lo)<5e-15 and max(true.hi-nom)<5e-15
    D=[]; families=[[],[]]
    for role,creator in enumerate(car.ROLE_CREATION):
        adj=car.transpose(creator)
        for mat,os,ins in ((creator,0,1),(adj,1,0),(car.mscale(adj,-1),0,0),(car.mscale(creator,-1),0,0)):
            D.append(atom(role,mat,EV,OD,os,ins,t,-t))
        for mat,os,ins in ((adj,1,0),(creator,0,1),(car.mscale(adj,-1),0,0),(car.mscale(creator,-1),0,0)):
            families[0].append(atom(role,mat,OD,EV,os,ins,t,-t))
        LP=car.mscale(car.mmul(creator,adj),1/Q(GAMMA[role]))
        RP=car.mscale(car.mmul(adj,creator),1/Q(GAMMA[role]))
        for mat,shift in ((LP,0),(RP,1),(car.mscale(LP,-1),0),(car.mscale(RP,-1),0)):
            families[1].append(atom(role,mat,EV,EV,shift,shift,defect,d_defect))
    C=np.zeros((N,128))
    f=np.asarray(car.fourier_numerators())/128
    for m,a in ((1,np.sqrt(p)),(14,p)):
        C[OD.index(m)::8,:]=a*f
    return D,families,C,t


def matrix_ball(terms,signs,diagonal=0):
    M=sum(w*t.M for t,w in zip(terms,signs))+diagonal*sparse.eye(N)
    # 16-term assembly and possible identity. Sparse rows have fewer than 128
    # entries. Coefficients of flat four-leg CAR and its projectors are dyadic.
    err=sum(t.Merr+5e-15*abs(t.M) for t in terms)+abs(diagonal)*5e-15*sparse.eye(N)
    return M/16,err*(1.000001/16)


def ball_apply(mats,ball,transpose=False):
    M,E=mats
    if transpose: M,E=M.T,E.T
    x,ex=ball
    y=M@x
    assert M.getnnz(axis=1).max()<=128
    err=abs(M)@ex+E@(np.abs(x)+ex)+2e-14*(abs(M)@np.abs(x))
    return y,err*1.000001+1e-290


def pointer_rows(D,families,C):
    A=matrix_ball(D,[1]*16)
    # a and p are divided by 128; all Fourier numerators are -1, 0, 1.
    C=(C,np.full(C.shape,5e-17))
    ac=ball_apply(A,C)
    rows=[];errors=[]
    for coeff,terms in enumerate(families):
        for j in range(16):
            # Representatives for the four equal pairs of squared amplitudes.
            if coeff==1 and j%4==1:
                continue
            if coeff==0 and j in (9,14):
                continue
            signs=[parity(j&k) for k in range(16)]
            const=sum(w*(1 if k%4<2 else -1) for k,w in enumerate(signs)) if coeff else 0
            S=matrix_ball(terms,signs,const)
            o=ball_apply(S,ac)
            back=ball_apply(S,o,transpose=True)
            vals=[d.bounded_pull(back,C) for d in D]
            for w,a in zip(signs,terms):
                x,e=a.bounded_pull(o,ac)
                vals.append((w*x,e))
            grad=sum(x for x,e in vals)[ACTIVE]/8
            err=sum(e+6e-15*np.abs(x) for x,e in vals)[ACTIVE]/8
            rows.append(grad);errors.append(err*1.000001+1e-290)
    return np.array(rows),np.array(errors)


def heat_rows(D):
    cache=[]
    old_svd=heat.linalg.svd
    def capture(*args,**kwargs):
        out=old_svd(*args,**kwargs)
        cache.append(out)
        return out
    with patch.object(heat.linalg,"svd",side_effect=capture):
        s,_=heat.numerical_basis()
    X0,_,Yt0=cache[0]
    # Our block uses the opposite parity order to the SVD owner.
    X=Yt0.T;Y=X0
    assert (32*32*2*(heat.P*heat.P*heat.P).square()*heat.I.rational(Q(256*78,10946))*16).hi<64**2
    locals_by_leg=[]
    for j in ACTIVE:
        local=np.zeros(N)
        nu=0
        for atom in D:
            positions=np.where(atom.j==j)[0]
            if len(positions)==0:continue
            for k in positions:
                local+=(-4*atom.dv[k])*X[atom.r[k]]*Y[atom.c[k]]
                nu+=1
        # The diagonal coefficient l1 aggregate error is strictly <1e-7:
        # each row product has l1<=1+1e-9 from the polar certificate;
        # the at most 64 dyadic-coefficient summands have magnitude < 8.
        assert nu<=64 and 64*(4*8e-15+65*2e-16*8)*1.001<1e-7
        locals_by_leg.append(local)
    # The sum of four legs scales all four covariant legs at one free site.
    # The full Weyl source has rank <=32 and squared HS norm 144 t_i^2/h^2.
    # Half of that source has nuclear norm <45; the common bound 64 applies.
    assert (32*144*(heat.P*heat.P*heat.P).square()*heat.I.rational(Q(256*78,10946))*16).hi < 90**2
    # At most 256 previously bounded product collections enter each Weyl row.
    # Including three additions and scaling by 1/2 leaves aggregate l1 error <1e-7.
    assert (4*64*(4*8e-15+70*2e-16*8)*1.001)/2 < 1e-7
    weyl_locals=np.asarray(locals_by_leg).reshape(32,4,N).sum(axis=1)/2
    def enclose(locals_,factor):
        centers=[]; radii=[]
        for local in locals_:
            cells=[heat.across_depths(s,local,n,n)[0]*factor for n in (1,64,512)]
            mid=np.array([(x.lo+x.hi)/2 for x in cells])
            error=[max(v-x.lo,x.hi-v)*1.000001+1e-290 for x,v in zip(cells,mid)]
            centers.append(mid); radii.append(error)
        return np.asarray(centers).T,np.asarray(radii).T
    return enclose(locals_by_leg,1),enclose(weyl_locals,2)


def signed_rank(rows,errs):
    n,m=rows.shape
    scale=np.linalg.norm(rows,axis=1)
    A=rows/scale[:,None]
    delta=errs/scale[:,None]+3e-16*np.abs(A)
    Qm,s,Vt=linalg.svd(A,full_matrices=False)
    # R is a right-inverse candidate. Certify ||(A_true R)-I||_inf <1.
    from scipy.linalg.blas import dgemm
    R=dgemm(1.,Vt.T/s,Qm,trans_b=1)
    product=dgemm(1.,A,R)
    defect=np.max(np.sum(np.abs(product-np.eye(n)),axis=1))
    arithmetic=3e-14*np.max(np.sum(dgemm(1.,np.abs(A),np.abs(R)),axis=1))
    uncertainty=np.max(np.sum(dgemm(1.,delta,np.abs(R)),axis=1))
    certified=1.000001*(defect+arithmetic+uncertainty)+1e-15
    print("rows",n,"least nominal singular value",s[-1],
          "uncertainty",uncertainty,"certified inverse defect",certified,flush=True)
    assert certified<1


def check_structural_identities():
    walsh=np.array([[parity(k & l) for l in range(16)] for k in range(16)])
    assert np.array_equal(walsh @ walsh.T,16*np.eye(16))
    for r in range(4):
        cr=car.ROLE_CREATION[r]
        assert all(value==0 for row in car.mmul(cr,cr) for value in row)
        for low in range(4):
            for d in (1,3):
                assert (4*r+low)^d == 4*r+(low^d)
                assert low%2 != (low^d)%2
        def defect_coeffs(k):
            a,b,c,d=walsh[k,4*r:4*r+4]
            return np.array([a-c,b,-d])
        for k in range(0,16,4):
            assert np.array_equal(defect_coeffs(k),-defect_coeffs(k+1))
    a,b=walsh[1,[9,14]]
    c,d=walsh[3,[9,14]]
    assert abs(a*d-b*c)==2


def main():
    check_structural_identities()
    D,fam,C,_=assemble()
    rows,radius=pointer_rows(D,fam,C)
    signed_rank(rows,radius)
    (g,ge),(wg,wge)=heat_rows(D)
    signed_rank(np.concatenate([rows,g]),np.concatenate([radius,ge]))
    wr=rows.reshape(-1,32,4)
    we=(radius.reshape(-1,32,4)+1e-15*np.abs(wr)).sum(axis=2)*1.000001
    wr=wr.sum(axis=2)
    print("Weyl coordinates alone:",flush=True)
    signed_rank(wr,we)
    signed_rank(np.vstack((wr,wg)),np.vstack((we,wge)))
    print("Pointer rank 26; depths 1, 64 and 512 raise the rank to 29 on both charts.")


if __name__=="__main__":
    main()

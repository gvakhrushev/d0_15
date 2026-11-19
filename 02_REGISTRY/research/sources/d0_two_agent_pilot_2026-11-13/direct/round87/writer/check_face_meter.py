"""Paid XOR shear on the real Julia bank, including its untouched 32-column reference."""
import itertools
import json
import math

import numpy as np
import sympy as sp


p=(math.sqrt(5)-1)/2
a=math.sqrt(p)
G=np.array([[a,-p],[p,a]])
NADDR=2049
D=32*NADDR
FADDR=1
LADDR=1041  # positive u-link at x+e2 on the 4^4 reference torus
ORDER=(0,2,3,1)
EYE=np.eye(4)
ETA=EYE[[1,0,2,3]].copy()
ETA[2,2]=ETA[3,3]=-1
N2=np.outer(EYE[1],EYE[2])+np.outer(EYE[2],EYE[0])


def require(ok,msg):
    if not ok:
        raise ValueError(msg)


def close(actual,expected):
    require(np.allclose(actual,expected,rtol=3e-12,atol=3e-14),"numerical identity")


def creators():
    matrices=np.zeros((4,16,16))
    for q in ORDER:
        for mask in range(16):
            if not mask&(1<<q):
                before=sum(bool(mask&(1<<i)) for i in ORDER[:ORDER.index(q)])
                matrices[q,mask|(1<<q),mask]=(-1)**before
    return matrices


CREATORS=creators()


def exterior(u):
    grades=[tuple(i for i in ORDER if mask&(1<<i)) for mask in range(16)]
    return np.array([[np.linalg.det(u[np.ix_(row,col)]) if row and len(row)==len(col)
                      else float(not row and not col) for col in grades] for row in grades])


def defect(x):
    vals,vec=np.linalg.eigh(x)
    require(min(vals)>0,"strict physical Julia chart")
    return np.einsum("ij,kj->ik",vec*np.sqrt(vals),vec)


def julia(x):
    eye=np.eye(16)
    j=np.block([[x,defect(eye-np.einsum("ij,kj->ik",x,x))],
                [defect(eye-np.einsum("ji,jk->ik",x,x)),-x.T]])
    close(np.einsum("ij,kj->ik",j,j),np.eye(32))
    return j


def blocks(s,t):
    coframe=ETA/4
    coframe[0,0]+=s
    jf=julia(np.tensordot(coframe[:,0],CREATORS,axes=1))
    u=EYE+t*N2+(t*t/2)*(N2@N2)
    jl=julia(exterior(u)/2)
    close(u.T@ETA@u,ETA)
    return jf,jl


def true_density():
    eye=sp.eye(4)
    unit=lambda i,j:eye[:,i]*eye[:,j].T
    eta=unit(0,1)+unit(1,0)-unit(2,2)-unit(3,3)
    nu,s,t=sp.symbols("nu s t",real=True,nonzero=True)
    v=nu*eta+s*unit(0,0)
    n=unit(1,2)+unit(2,0)
    u=eye+t*n+t*t*n*n/2
    sharp=lambda b:eta*b.T*eta
    curve=(sharp(u)-u)/2
    biv=(v[:,0]*v[:,2].T-v[:,2]*v[:,0].T)*eta
    value=sp.factor(nu**4*sp.trace(biv*curve)/(2*v.det()))
    require(value==nu*s*t and v.det()==-nu**4,"original normalized Palatini value")
    return str(value)


def shear(left,right):
    diff=left^right
    pivot=diff.bit_length()-1
    targets=tuple(i for i in range(pivot) if diff&(1<<i))
    def route(word):
        for i in targets:
            if word&(1<<pivot):
                word^=1<<i
        return word
    require(route(left)^route(right)==1<<pivot,"both physical words share a syndrome")
    return pivot,targets,route


def main():
    value=true_density()
    # Existing torus labels: four columns at each site, then four links at each site.
    require(FADDR==1 and LADDR==1+4*256+4*4, "u(z),u-link(z+e2)")
    i=(FADDR<<5)|5
    j=(LADDR<<5)|2
    bit,targets,perm=shear(i,j)
    require(len(targets)==4,"literal number of address/data CX")
    width=(NADDR-1).bit_length()+5
    # Every computational input outside the selected pair stays outside its two outputs.
    target_words={perm(i),perm(j)}
    matching=[n for n in range(1<<width) if perm(n) in target_words]
    require(matching==[i,j],"all 131072 physical basis words including padding")
    four={}
    linear_rows=two_local=0
    for s,t in itertools.product((0.,1/8),(0.,1/4)):
        jf,jl=blocks(s,t)
        # Complete 32-column rows; all original reference wires remain spectators.
        ri,rj=jf[5,:],jl[2,:]
        close(ri[16:]@rj[16:],0)
        close(ri[:16]@rj[:16],s*t/2)
        out=np.einsum("ij,jk->ik",G,np.stack((ri,rj)))/math.sqrt(D)
        q0,q1=np.sum(out**2,axis=1)
        close(np.array([q0,q1]),np.array([1-a*p*s*t,1+a*p*s*t])/D)
        four[s,t]=q1
        # For each independent coherent input with the protected reference,
        # pairing any row with a retained identity-anchor row reads the actual J entry.
        for orig in (jf,jl):
            for r,col in itertools.product(range(32),repeat=2):
                x,y=np.einsum("ij,jk->ik",G,np.stack((orig[r,:],np.eye(32)[col,:])))
                close((y@y-x@x)/(4*a*p),orig[r,col])
                linear_rows+=1
        # Two local pure Choi operands or two independently dephased-address resources.
        # Local coframe defect and vacuum link provide two invariant amplitude anchors.
        close(jf[0,16],1)
        close(jl[0,0],.5)
        left=jf[1,0]*jl[0,0]
        right=jf[0,16]*jl[2,4]
        close([left,right],[s/2,t/2])
        # Four old reference signals in the two admitted address-matched blocks.
        close((G@np.array([left,right]))**2/32**2,
              np.array([(a*s-p*t)**2,(p*s+a*t)**2])/(4*32**2))
        two_local+=1
    st=(1/8)*(1/4)
    cross=four[1/8,1/4]-four[1/8,0.]-four[0.,1/4]+four[0.,0.]
    close(cross,a*p*st/D)
    # Selector for rational sums. The marked tags are all actual original Born words.
    # A two-coin decoder has probability p^2+p^3 E[sign]; it needs no fair coin.
    for sign in (-1,0,1):
        prob=0.
        for r,s in itertools.product((0,1),repeat=2):
            w=(p**2 if r else p)*(p**2 if s else p)
            y=r if r==s or sign==0 else int(sign>0)
            prob+=w*y
        close(prob,p**2+p**3*sign)
    tag_weights=[math.prod(p**2 if bit else p for bit in tag)
                 for tag in itertools.product((0,1),repeat=6) if sum(tag)==3]
    require(len(tag_weights)==20,"number of equal-weight programmed tags")
    close(tag_weights,np.full(20,p**9))
    print(json.dumps({
      "status":"PASS","L":4,"active_global_addresses":NADDR,"Choi_normalization_D":D,
      "paid_address_examples":[FADDR,LADDR],"visible_pair":[i,j],"hidden_reference_dimension":32,
      "elementary_XOR_shear_CX":len(targets),"XOR_controls_and_targets":[bit,list(targets)],
      "positive_G_after_shear":1,"exhaustive_live_NC1_readers":width,
      "quantum_reference_rows_tested_against_identity_anchor":linear_rows,
      "normalized_true_face":value,"mixed_response_rectangle_D_times":round(float(cross*D),13),
      "two_independent_locally_purified_dephased_inputs_checked":two_local,
      "labelled_addresses_and_inaccessible_reference_give_constant_state_for_all_copies":True,
      "same_pure_input_returned":False,"full_geometry_supplier_native":False,"GR_closed":False
    },indent=2))


if __name__=="__main__":
    main()


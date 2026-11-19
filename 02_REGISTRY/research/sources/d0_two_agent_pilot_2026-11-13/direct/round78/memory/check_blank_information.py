"""RIGHT posterior, actual fixed-basis read and binary blank event on a held preparation."""
from contextlib import redirect_stdout
import io
import json
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import sys

import numpy as np
from scipy import sparse

DIRECT = Path(__file__).resolve().parents[2]
for rel in ("round76/geometry","round77/volume","round75/history","round75/work"):
    sys.path.insert(0,str(DIRECT/rel))
import check_invisible_geometry as geo
import check_isochoric_source as volume
import check_two_site_source as sites
import check_pointer_weyl as pointer

I, O, spectral = pointer.I, pointer.O, pointer.spectral
N = 128
UNIT = I(np.eye(N))
P = I(geo.heat.P.lo, geo.heat.P.hi)
LOG_PHI = O.logarithm(I(1.)/P)


def close_ball(pair):
    x,e = pair
    return I(np.nextafter(x-e,-np.inf),np.nextafter(x+e,np.inf))


def add_ball(first,second):
    x,e=first
    y,f=second
    return x+y,1.000001*(e+f+2e-16*(abs(x)+abs(y)))+1e-290


def diff_operator(atoms, entries):
    weights,err=np.zeros(1024),np.zeros(1024)
    for idx, value in entries:
        weights[idx]=(value.lo+value.hi)/2
        err[idx]=1.000001*max(weights[idx]-value.lo,value.hi-weights[idx])+1e-290
    matrices,radii=[],[]
    for t in atoms:
        val=t.dv*weights[t.j]
        rad=t.dv_err*(abs(weights[t.j])+err[t.j])+abs(t.dv)*err[t.j]+5e-15*abs(val)
        for coeff,target in ((val,matrices),(rad,radii)):
            target.append(sparse.csr_matrix((coeff,(t.r,t.c)),shape=(geo.N,geo.N)))
    return sum(matrices)/16,1.000001*(sum(radii)+5e-15*sum(abs(m) for m in matrices))/16


def derivatives(atoms, prepared):
    a,b=sites.material_coefficients()
    idx=lambda site:4*geo.car.site_index(site)
    main=[(idx(site)+r,I(sign)/I(q.lo,q.hi)) for site,sign,q in
          ((sites.SITE_A,1.,a),(sites.SITE_B,-1.,b)) for r in range(4)]
    all_fields={"A75":diff_operator(atoms,main)}
    R=volume.material_rows(atoms,prepared)
    for name,z,w,r,scale in (("A77_16",(1,0,1,1),(1,2,2,2),1,16),
                              ("A77_128",(1,1,2,2),(2,1,1,2),2,128)):
        j,k=idx(z),idx(w)
        a,b=R[j+r]-R[j+3],R[k+r]-R[k+3]
        all_fields[name]=diff_operator(atoms,[(j+r,-scale*b),(j+3,scale*b),(k+r,scale*a),(k+3,-scale*a)])
    return all_fields


def moment_tables():
    terms,_,C,_=geo.assemble()
    A=geo.matrix_ball(terms,[1]*16)
    fields=derivatives(terms,C)
    state=(C,np.full(C.shape,5e-17))
    dstates={name:(np.zeros_like(C),np.zeros_like(C)) for name in fields}
    moments=[]
    for j in range(1,7):
        # A maps odd to even, and on even equals the transpose parity block.
        trans=j%2==0
        for name,D in fields.items():
            dstates[name]=add_ball(geo.ball_apply(A,dstates[name],transpose=trans),
                                   geo.ball_apply(D,state,transpose=trans))
        state=geo.ball_apply(A,state,transpose=trans)
        true=close_ball(state)
        gram=spectral.matmul(spectral.transpose(true),true)
        dgrams={}
        for name,value in dstates.items():
            v=spectral.matmul(spectral.transpose(true),close_ball(value))
            dgrams[name]=v+spectral.transpose(v)
        moments.append((gram,dgrams))
    return moments


def trace(x):
    return O.reduce_sum(I(np.diag(x.lo),np.diag(x.hi)))


def diag(x):
    return I(np.diag(x.lo),np.diag(x.hi))


def log_vector(x):
    logs=[O.logarithm(I(a,b)) for a,b in zip(x.lo,x.hi)]
    return I([v.lo for v in logs],[v.hi for v in logs])


def log_matrix_test(m):
    """Enclose log(m) in op norm; candidate diagonalization never certifies itself."""
    cen,_=spectral.midpoint_radius(m)
    eig,basis=np.linalg.eigh((cen+cen.T)/2)
    U=I(basis)
    Ut=spectral.transpose(U)
    delta=spectral.exact_upper(spectral.norm_upper(spectral.matmul(Ut,U)-UNIT))
    assert delta.hi<1e-9
    dist=delta/(1+(I(1.)-delta).sqrt())
    factor=2*(I(1.)+delta).sqrt()*dist+dist.square()
    model=spectral.matmul(U*I(eig[None,:]),Ut)
    err=spectral.exact_upper(spectral.norm_upper(m-model))+factor*float(max(eig))
    lower=I(float(min(eig)))-err
    assert lower.lo>0
    logs=log_vector(I(eig))
    absolute=max(abs(logs.lo).max(),abs(logs.hi).max())
    log_value=spectral.matmul(U*I(logs.lo[None,:],logs.hi[None,:]),Ut)
    return log_value,err/lower+factor*float(absolute)


def pairing(x,log_approx,err):
    # ||x||_* <= sqrt(128) ||x||_HS, including its supplied interval error.
    raw=O.reduce_sum(x*spectral.transpose(log_approx))
    extra=12*spectral.exact_upper(spectral.norm_upper(x))*err
    return (raw+I(-float(extra.hi),float(extra.hi)))/LOG_PHI


def gain(matrix,field):
    mass=trace(matrix)
    post=matrix/mass
    logr,err=log_matrix_test(post*N)
    md=diag(post)
    classical_log=log_vector(md*N)
    val=pairing(post,logr,err)
    cl_val=O.reduce_sum(md*classical_log)/LOG_PHI
    results={}
    for name,dm in field.items():
        dm_total=trace(dm)
        dpost=(dm-post*dm_total)/mass
        rate=pairing(dpost,logr,err)
        cl_rate=O.reduce_sum(diag(dpost)*classical_log)/LOG_PHI
        results[name]=(rate,cl_rate,dm_total)
    return mass,val,cl_val,results


def bounds(x):
    return (float(x.lo),float(x.hi))


def run():
    moments=moment_tables()
    p=P
    power=I(1.)
    coeff=[]
    for _ in range(6):
        power=power*2*p*p
        coeff.append(power)
    for_table={}
    probabilities=[]
    blank_values=[]
    fixed_basis_values=[]
    for k in (1,2,3):
        stop=I(np.zeros((N,N)))
        rates={name:I(np.zeros((N,N))) for name in moments[0][1]}
        for i,(m,ds) in enumerate(moments[:2*k]):
            weight=(((-1)**i)*comb(2*k,i+1))*coeff[i]
            stop=stop+m*weight
            for name,dm in ds.items():
                rates[name]=rates[name]+dm*weight
        blank=UNIT/N-stop
        q,blank_i,blank_cl,db=gain(blank,{n:-v for n,v in rates.items()})
        r,fail_i,fail_cl,df=gain(stop,rates)
        probabilities.append(q)
        blank_values.append(blank_i)
        fixed_basis_values.append(blank_cl)
        print("length",k,"P",bounds(q),"RIGHT gain upon blank",bounds(blank_i),
              "basis gain",bounds(blank_cl),flush=True)
        for name in rates:
            dg,dgc,dq=db[name]
            dfail,dfc,dr=df[name]
            weighted=dq*blank_i+q*dg
            full=weighted+dr*fail_i+r*dfail
            full_cl=dq*blank_cl+q*dgc+dr*fail_cl+r*dfc
            dp_surprise=-dq/(q*LOG_PHI)
            dh=dq*O.logarithm(r/q)/LOG_PHI
            for_table.setdefault(name,[]).append(
                {"blank_gain":dg,"blank_weighted":weighted,"binary_CQ_I":full,
                 "basis_blank_gain":dgc,"basis_binary_I":full_cl,
                 "blank_surprise":dp_surprise, "binary_H":dh,
                 "binary_joint_H":dh-full,"mass":dq,"literal_binary_cost":-dq,
                 "literal_minus_binary_H":-dq-dh,"literal_minus_joint_H":-dq-dh+full})
    jets={}
    for name,entries in for_table.items():
        print(name,"mass derivatives per length:", [bounds(elt["mass"]) for elt in entries])
        print(name,"D of second differences:",flush=True)
        jets[name]={key:entries[2][key]-2*entries[1][key]+entries[0][key]
                    for key in entries[0]}
        for key,x in jets[name].items():
            print(key,bounds(x))
    t=jets["A75"]["blank_surprise"]
    g=jets["A75"]["blank_gain"]
    assert -4.145025e-6<t.lo<=t.hi<-4.145024e-6
    assert 1.887340e-6<g.lo<=g.hi<1.887342e-6
    assert (jets["A75"]["basis_blank_gain"]).hi < 0
    fraction=(-g)/t
    assert .4553<fraction.lo<=fraction.hi<.4554
    print("fraction of target signed source supplied by minus blank RIGHT gain",bounds(fraction))
    def det(a,b,c):
        rows=[([jets[name][x]*factor for x in (a,b,c)])
              for name,factor in (("A75",10**6),("A77_16",10**10),("A77_128",10**10))]
        (x,y,z),(l,m,n),(r,s,t)=rows
        return x*(m*t-n*s)-y*(l*t-n*r)+z*(l*s-m*r)
    for second,threshold in (("binary_CQ_I",10.),("binary_H",.03),("basis_blank_gain",10.)):
        determinant=det("blank_surprise","blank_gain",second)
        print("determinant target / blank gain /",second,bounds(determinant))
        assert determinant.lo>threshold or determinant.hi< -threshold
    return {"P":probabilities, "blank_RIGHT_gain":blank_values,
            "basis_blank_gain":fixed_basis_values, "fields":for_table, "curvature":jets}


def certificate():
    """Machine-readable enclosures as [lower, upper], including P, dP and d2 jets."""
    with redirect_stdout(io.StringIO()):
        raw=run()
    def encode(x):
        if isinstance(x,dict):
            return {k:encode(v) for k,v in x.items()}
        if isinstance(x,list):
            return [encode(v) for v in x]
        return list(bounds(x))
    return encode(raw)


if __name__=="__main__":
    if sys.argv[1:]==["--json"]:
        print(json.dumps(certificate(),sort_keys=True))
    else:
        run()

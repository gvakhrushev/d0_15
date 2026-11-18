"""Full primary Julia/Walsh pointer on the two-site coframe variation with DR=0."""
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[7]
OWNER = ROOT/"02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source"
sys.path.insert(0, str(OWNER))
import check_primary_car_preparation_source as car
import check_primary_right_posterior_gain as spectral

O = spectral.O
I = O.I


def norm(x):
    return spectral.norm_upper(x)


def dirac(x, k, forward, backward):
    # This is h*D/16, the original first column of the Julia processor.
    weight = O.broadcast_site(k)
    total = I(np.zeros_like(x.lo))
    for role, cr in enumerate(car.ROLE_CREATION):
        ct = car.transpose(cr)
        first = O.const_matrix_action(cr, O.shifted(x,forward[role])-x)
        second = weight*O.const_matrix_action(ct,x)
        total = total+weight*first+O.shifted(second,backward[role])-second
    return total*Q(1,16)


def site_vector():
    p = (I.rational(5).sqrt()-1)*Q(1,2)
    f = I(np.array(car.fourier_numerators()) / 128.)
    base = np.zeros((256,16,128))
    lo, hi = base.copy(), base.copy()
    for grade, coeff in ((1,p.sqrt()),(14,p)):
        row = coeff*f
        lo[:,grade,:],hi[:,grade,:] = row.lo,row.hi
    state = I(lo,hi)
    counts = car.actual_counts(ROOT)
    density = [I.rational(Q(256*n,sum(counts))).sqrt() for n in counts]
    w = p*p*p*I([v.lo for v in density],[v.hi for v in density])
    fw = [np.array([car.site_index(car.step(x,j,1)) for x in car.SITES_LIST]) for j in range(4)]
    bw = [np.array([car.site_index(car.step(x,j,-1)) for x in car.SITES_LIST]) for j in range(4)]
    u = dirac(state,w,fw,bw)
    dw = I(np.zeros(256))
    rows = []
    for site, sign in (((1,3,2,2),-1),((2,2,1,1),1)):
        i = car.site_index(site)
        mask = np.zeros(256)
        mask[i] = 1
        unscaled = w*I(mask)
        dr = 2*64**2*O.reduce_sum(u*dirac(state,unscaled,fw,bw))
        O.require(dr.lo > 0, "true scale derivative is negative")
        dw = dw+sign*unscaled/dr
        rows.append(O.bounds(dr))
    du = dirac(state,dw,fw,bw)
    O.require(O.reduce_sum(u*du).contains(0), "DR cancels on its own real tangent")
    return p,state,w,dw,fw,bw,u,du,rows


def actions(coefficient,w,dw,fw,bw,u,du):
    values, derivatives = [],[]
    wt,dt = O.broadcast_site(w),O.broadcast_site(dw)
    for j,(cr,g) in enumerate(zip(car.ROLE_CREATION,(Q(1,2),Q(2),Q(1),Q(1)))):
        ct = car.transpose(cr)
        if coefficient == 0:
            x,y = O.const_matrix_action(ct,u),O.const_matrix_action(cr,u)
            dx,dy = O.const_matrix_action(ct,du),O.const_matrix_action(cr,du)
            values.extend((O.shifted(wt*x,bw[j]),wt*O.shifted(y,fw[j]),-wt*x,-wt*y))
            derivatives.extend((O.shifted(dt*x+wt*dx,bw[j]),
                                dt*O.shifted(y,fw[j])+wt*O.shifted(dy,fw[j]),
                                -(dt*x+wt*dx),-(dt*y+wt*dy)))
        else:
            # A conformal variation changes the leg length but not these
            # degree projectors. The positive Julia square roots do change.
            rad = (I(1.)-w.square()*g).sqrt()
            dot = -w*dw*g/rad
            defect = rad-1
            le = car.mscale(car.mmul(cr,ct),1/g)
            ri = car.mscale(car.mmul(ct,cr),1/g)
            def rooted(proj,r,t):
                base = O.const_matrix_action(proj,u)
                dbase = O.const_matrix_action(proj,du)
                return (u+O.broadcast_site(r)*base,
                        du+O.broadcast_site(t)*base+O.broadcast_site(r)*dbase)
            a,da = rooted(le,defect,dot)
            b,db = rooted(ri,O.shifted(defect,bw[j]),O.shifted(dot,bw[j]))
            c,dc = rooted(ri,defect,dot)
            values.extend((a,b,-a,-c))
            derivatives.extend((da,db,-da,-dc))
    return O.fwht(values), O.fwht(derivatives)


def flatten(x):
    return I(x.lo.reshape(4096,128),x.hi.reshape(4096,128))


def main():
    for rel,digest in O.PINS.items():
        O.require(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,"primary source changed")
    p,state,w,dw,fw,bw,u,du,rows = site_vector()
    h,gain,port,jet_sum = (I(0.) for _ in range(4))
    gram_sum = I(np.zeros((128,128)))
    full_tangent = I(np.zeros((128,128)))
    logphi = -O.logarithm(p)
    witness = None
    for coeff in range(2):
        values,ders = actions(coeff,w,dw,fw,bw,u,du)
        for j,(v,dv) in enumerate(zip(values,ders)):
            blank = j==coeff==0
            for e in ((0,1) if blank else (1,)):
                fac = -2*(p*p if e==0 else p*p.sqrt())
                Z = flatten(v*fac+state if blank and e==0 else v*fac)
                DZ = flatten(dv*fac)
                active = np.any((DZ.lo!=0)|(DZ.hi!=0),axis=1)
                za, da = Z[active], DZ[active]
                cross = spectral.matmul(spectral.transpose(za),da)
                DB = cross+spectral.transpose(cross)
                B = spectral.matmul(spectral.transpose(Z),Z)
                # Holder: ||DB||_1 <= 2||Z_active||_F ||DZ_active||_F.
                # The imported log proof uses its last three arguments only
                # to bound this nuclear norm by 2*p*||cross||_F*||rr||_F.
                g,q,_ = spectral.posterior_certificate(B,DB,za,da,I(1.))
                tr = O.reduce_sum(I(np.diag(DB.lo),np.diag(DB.hi)))
                mult = I(1.) if blank else 1+p
                gram_sum = gram_sum+mult*B
                full_tangent = full_tangent+mult*DB
                jet_sum = jet_sum+mult*tr
                gain = gain+mult*g
                h = h-tr*O.logarithm(q)
                if not blank:
                    h = h-p*tr*O.logarithm(p*q)
                if e==1:
                    port = port+tr
                if 8*j+2*coeff+e==19:
                    witness = tr
    O.require(gram_sum.contains(np.eye(128)/128) and full_tangent.contains(np.zeros((128,128))),
              "all marks preserve the original RIGHT prior")
    O.require(jet_sum.contains(0) and port.contains(0),"complete weight and real port are stationary")
    H,J = h/logphi,gain/logphi
    cq = H-J
    O.require(witness is not None and witness.hi < -0.00001203 and witness.lo > -0.00001204,"fine outcome 19")
    O.require(H.lo > 0.00024 and H.hi < 0.00025,"complete classical pointer")
    O.require(J.lo > 0.00030 and J.hi < 0.00031,"RIGHT gain")
    O.require(cq.lo > -0.000070 and cq.hi < -0.000050,"joint pointer and RIGHT entropy")
    O.require(Q(2204,100000)/Q(1204,10**8)>1830, "slope in the physical outcome coordinate")
    print(json.dumps({"absolute_site_D_R":rows,"finite_receiver_19":O.bounds(witness),
                      "H_full_pointer":O.bounds(H),"I_RIGHT_pointer":O.bounds(J),
                      "S_joint_pointer_RIGHT":O.bounds(cq),"port_derivative":O.bounds(port),
                      "physical_Book_Info_identified":False},sort_keys=True))


if __name__=="__main__":
    main()

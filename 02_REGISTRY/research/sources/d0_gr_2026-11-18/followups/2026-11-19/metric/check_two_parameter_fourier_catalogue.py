"""Fixed native logical catalogue of four two-component Fourier fields.

All retained descriptors, SITE bits and all sixteen CAR columns are checked
against the literal signed phase network. Heralded factories are composed by
their previously certified scalar-success effects; their unitary dilation,
the varying descriptor preparation and full Book03 price remain open.
"""
from itertools import product
from fractions import Fraction
import json
import math
import numpy as np
import sympy as sp
from mpmath import iv
import check_dyadic_car_loader as car
from check_fourier_fresh_localization import original_reference
from check_native_fourier_uncompute import BDD, schedule


def programme():
    ops=[]
    def cx(c,t):ops.append(('CX',c,t))
    def tof(a,b,t):ops.append(('T',a,b,t))
    def ccz(a,b,c):ops.append(('CCZ',a,b,c))
    def swap_pair(u,v):
        target=(u^v).bit_length()-1
        others=[i for i in range(4) if i != target]
        neg=[i for i in others if not ((u>>i)&1)]
        for i in neg:cx('h',f'c{i}')
        tof(f'c{others[0]}',f'c{others[1]}','a')
        tof('a',f'c{others[2]}',f'c{target}')
        tof(f'c{others[0]}',f'c{others[1]}','a')
        for i in reversed(neg):cx('h',f'c{i}')
    def low(ctrl):
        for a,b in ((0,1),(1,3),(3,7)):swap_pair(a,b)
        tof('c0','c1','a');tof('c2',ctrl,'b')
        ccz('a','b','c3');tof('a','b','c3')
        tof('c2',ctrl,'b');tof('c0','c1','a')
        for a,b in ((3,7),(1,3),(0,1)):swap_pair(a,b)
    def high(ctrl):
        for pattern in (0,15):
            neg=[i for i in range(4) if not ((pattern>>i)&1)]
            for i in neg:cx('h',f'c{i}')
            tof('c0','c1','a');tof('c2','c3','b')
            ccz('a','b',ctrl)
            tof('c2','c3','b');tof('c0','c1','a')
            for i in reversed(neg):cx('h',f'c{i}')
    low('y2');high('y3')             # y1
    for desc,lo,hi in (('u','y0','y1'),('v','y4','y5')):
        tof(desc,lo,'t');low('t');tof(desc,lo,'t')
        tof(desc,hi,'t');high('t');tof(desc,hi,'t')
    return ops


def main():
    # Four descriptor states, every 4^4 site and all 16 CAR columns.
    count=4*256*16
    ix=np.arange(count,dtype=np.uint32)
    c=ix&15; y=(ix>>4)&255; d=(ix>>12)&3
    bits={f'c{i}':((c>>i)&1).astype(np.uint8) for i in range(4)}
    bits.update({f'y{i}':((y>>i)&1).astype(np.uint8) for i in range(8)})
    bits.update(u=(d&1).astype(np.uint8),v=((d>>1)&1).astype(np.uint8),
                h=np.ones(count,dtype=np.uint8),
                a=np.zeros(count,dtype=np.uint8),b=np.zeros(count,dtype=np.uint8),
                t=np.zeros(count,dtype=np.uint8))
    sign=np.ones(count,dtype=np.int8)
    ops=programme()
    for op in ops:
        if op[0]=='CX':bits[op[2]]^=bits[op[1]]
        elif op[0]=='T':bits[op[3]]^=bits[op[1]]&bits[op[2]]
        else:sign*=1-2*(bits[op[1]]&bits[op[2]]&bits[op[3]]).astype(np.int8)
    actual=sum(bits[f'c{i}'].astype(np.uint32)<<i for i in range(4))
    for i in range(8):assert np.array_equal(bits[f'y{i}'],(y>>i)&1)
    assert np.array_equal(bits['u'],d&1) and np.array_equal(bits['v'],(d>>1)&1)
    assert np.all(bits['h']==1)
    assert not bits['a'].any() and not bits['b'].any() and not bits['t'].any()
    n=((y>>2)&3)+(d&1)*(y&3)+((d>>1)&1)*((y>>4)&3)
    n &= 3
    expected=c.copy(); exsign=np.ones(count,dtype=np.int8)
    for k in range(4):
        sel=n==k
        if k in (1,3):
            expected[sel&(c==0)]=15;expected[sel&(c==15)]=0
        if k in (2,3):exsign[sel&(c==0)]*=-1
        if k in (1,2):exsign[sel&(c==15)]*=-1
    assert np.array_equal(actual,expected) and np.array_equal(sign,exsign)
    counts={k:sum(op[0]==k for op in ops) for k in ('CX','T','CCZ')}
    assert counts['T']==101 and counts['CCZ']==9  # 3x phase 31 + 8 descriptor AND
    total_t=456+12+counts['T']                  # W + base + phase programmes
    assert total_t==569

    # Full original Fourier factors and all four physical material field maps.
    pairs,_,S=original_reference();assert S==256
    bdd=BDD();roots=[bdd.compile([(k[r]>>bit)&1 for k in pairs])
                     for r in range(4) for bit in (0,1)]
    coords=list(product(range(4),repeat=4));chi=np.zeros((S,128))
    for yi,z in enumerate(coords):
        for j,k in enumerate(pairs):
            out,sgn=schedule(bdd,roots,j,z,0)
            phase=sum(k[r]*z[r] for r in range(4))%4
            assert out==phase%2 and sgn==(-1 if phase&2 else 1)
            chi[yi,2*j+out]=sgn/128
    assert np.array_equal(np.einsum('yi,yj->ij',chi,chi,optimize=False),np.eye(128)/128)
    p=(math.sqrt(5)-1)/2;theta=math.asin(p);A=p*math.sin(712*theta)
    filler=-p*math.cos(712*theta);a=math.sqrt(p)
    G=np.array([[a,-p],[p,a]]);X=np.array([[0.,1.],[1.,0.]])
    base=car.mat_one(0,G)
    for b in (1,2,3):base=car.mm(car.mat_one(b,X),base)
    for b in (1,2,3):base=car.mm(car.mat_cx(0,b),base)
    base=car.mm(car.rotation(14,0,-712*theta),base)
    seed=base[:,1]
    assert np.linalg.norm(seed-np.eye(16)[:,1]*a-np.eye(16)[:,0]*A-np.eye(16)[:,14]*filler)<1e-12
    field=[];gram_err=0.0
    for u,v in product((0,1),repeat=2):
        m=[];f=[]
        for z in coords:
            n=(z[1]+u*z[0]+v*z[2])%4
            U=car.mm(car.rotation(0,15,n*math.pi/2),base)
            assert np.linalg.norm(car.mm(U.T,U)-np.eye(16))<1e-12
            m.append(U[:,1]); f.append((U[0,1],U[15,1]))
        m=np.asarray(m);field.append(np.asarray(f))
        C=(chi[:,None,:]*m[:,:,None]).reshape(S*16,128)
        gram_err=max(gram_err,float(np.max(np.abs(np.einsum('yi,yj->ij',C,C,optimize=False)-np.eye(128)/128))))
    assert gram_err<1e-14
    # product order: (u,v)=(0,0),(0,1),(1,0),(1,1)
    A2=A*A
    du=field[2]-field[0];dv=field[1]-field[0]
    Gram=np.array([[np.sum(du*du),np.sum(du*dv)],[np.sum(du*dv),np.sum(dv*dv)]])
    assert np.linalg.det(Gram)>1e-10
    lookup={z:i for i,z in enumerate(coords)};H=.25
    def q(field):
        vals=[]
        for z in coords:
            i=lookup[z];v=0.0
            for r in range(4):
                zn=list(z);zn[r]=(zn[r]+1)%4;j=lookup[tuple(zn)]
                dv=(field[j]-field[i])/H
                v+=(1 if r==0 else -1)*float(np.dot(dv,dv))/16
            vals.append(v)
        return np.asarray(vals)
    q_fields=[q(f) for f in field]
    for idx,(u,v) in enumerate(product((0,1),repeat=2)):
        assert np.max(np.abs(q_fields[idx]-2*A2*(u-1-v)))<1e-13
    I_fields=[-qi for qi in q_fields]  # coefficient k0/a* > 0 factored out
    assert np.max(np.abs(I_fields[2]-I_fields[0]+2*A2))<1e-13
    assert np.max(np.abs(I_fields[1]-I_fields[0]-2*A2))<1e-13
    # Two separately supplied descriptor pairs represent independent copies:
    # E_{independent}(D Psi_1 dot D Psi_2)=D E(Psi)^2. Sharing a single
    # descriptor instead produces E[q(Psi)] and generally differs.
    s,t=sp.symbols('s t',real=True)
    B=lambda x:1-2*x+2*x*x
    qmean=-sp.expand((B(s)-s*s)*B(t)+t*t*B(s))
    qshared=-1+s-t
    ref={s:sp.Rational(1,4),t:sp.Rational(1,4)}
    assert qmean.subs(ref)==-sp.Rational(25,64)
    assert sp.diff(qmean,s).subs(ref)==1
    assert sp.diff(qmean,t).subs(ref)==sp.Rational(1,4)
    assert qshared.subs(ref)==-1
    # Explicit numerical mixture vs independent-copy field calculus.
    w=[(1-.25)*(1-.25),(1-.25)*.25,.25*(1-.25),.25*.25]
    mean=sum(wi*fi for wi,fi in zip(w,field))
    qmix=q(mean)
    assert abs(float(qmix.mean())/(2*A2)+25/64)<1e-12
    def bilinear(left,right):
        out=[]
        for z in coords:
            i=lookup[z];val=0.0
            for r in range(4):
                zn=list(z);zn[r]=(zn[r]+1)%4;j=lookup[tuple(zn)]
                dl=(left[j]-left[i])/H;dr=(right[j]-right[i])/H
                val+=(1 if r==0 else -1)*float(np.dot(dl,dr))/16
            out.append(val)
        return np.asarray(out)
    independent=sum(w[i]*w[j]*bilinear(field[i],field[j])
                    for i in range(4) for j in range(4))
    assert np.max(np.abs(independent-qmix))<1e-13
    shared=sum(wi*qi for wi,qi in zip(w,q_fields))
    assert abs(float(shared.mean())/(2*A2)+1)<1e-12
    ds=.75*(field[2]-field[0])+.25*(field[3]-field[1])
    dt=.75*(field[1]-field[0])+.25*(field[3]-field[2])
    interior_gram=np.array([[np.sum(ds*ds),np.sum(ds*dt)],
                            [np.sum(dt*ds),np.sum(dt*dt)]])/(S*A2)
    assert np.max(np.abs(interior_gram-np.array([[1.25,.25],[.25,1.25]])))<1e-12
    assert abs(np.linalg.det(interior_gram)-1.5)<1e-12
    # Two fixed reference recipes have 113 T and 9 additional CCZ. Independent
    # fresh plus and heralded gate factorization are explicit assumptions.
    iv.dps=80;one=iv.mpf(1);pp=(iv.sqrt(5)-one)/2
    b0=one-(one-2*pp**3)**16;b2=one-(one-4*pp**3)**32;b3=one-(one-16*pp**9)**32
    mat=b0**226*(b2**4*b3)**113*b3**9
    w64=(one-pp**40)*((one-pp**384)**6*(one-(one-16*pp**9)**64))**456
    plus14=(one-pp**384)**14
    ready=mat*w64*plus14
    assert ready>iv.mpf('.93080028') and ready<iv.mpf('.93080029')
    print(json.dumps({
      'status':'PASS','L':4,'CAR_dimension':16,'descriptor_values':4,
      'site_descriptor_CAR_columns':count,'site_u_v_and_oldRIGHT_preserved_on_success':True,
      'T_phase_programme':counts['T'],'CCZ_phase_programme':counts['CCZ'],
      'CX_phase_programme':counts['CX'],'T_base_CAR':12,'T_original_Fourier_W':456,
      'T_total_Fourier_CAR':total_t,'CCZ_total_CAR':9,
      'new_descriptor_clean_ancillas':1,'fourier_full_gram_error_float':gram_err,
      'A_squared':A2,'field_tangent_gram_determinant':float(np.linalg.det(Gram)),
      'metric_signature':'+---',
      'four_exact_q_over_2A_squared':['-1','-2','0','-1'],
      'secant_u_q_over_2A_squared':1,'secant_v_q_over_2A_squared':-1,
      'secant_u_I_over_2k0A_squared_div_a':-1,
      'secant_v_I_over_2k0A_squared_div_a':1,
      'independent_descriptor_two_copy_q_over_2A_squared':str(qmean),
      'all_16_descriptor_pairs_checked_cellwise':True,
      'shared_descriptor_q_over_2A_squared':str(qshared),
      'interior_example_s_t':'1/4,1/4','independent_q_over_2A_squared':'-25/64',
      'independent_dq_ds_over_2A_squared':'1',
      'independent_dq_dt_over_2A_squared':'1/4',
      'interior_mean_field_tangent_gram_over_A_squared':[['5/4','1/4'],['1/4','5/4']],
      'interior_mean_field_tangent_gram_determinant_over_A_fourth':'3/2',
      'shared_q_over_2A_squared':'-1',
      'material_factory_readiness_conditional':str(mat),
      'full_Fourier_material_readiness_conditional':str(ready),
      'j_eight_setting_same_CAR_circuit_separate_preparations':True,
      'descriptor_initial_state_and_independent_preparation_physically_derived':False,
      'full_failure_clock_Book_cost_and_GR_closed':False,
    },indent=2,sort_keys=True))


if __name__=='__main__':main()

"""L=16 native phase carries, wrap and exact local geometric rebalance.

The two long G powers are certified as integer run lengths, not physically
replayed. Site-dependent coframe preparation, clock and Book cost remain open.
"""
from fractions import Fraction as F
from math import comb
import json, math
import mpmath as mp

mp.mp.dps=100
p=(mp.sqrt(5)-1)/2;theta=mp.atan2(p,mp.sqrt(p));z=mp.mpf(1)/2**20
L=16;H=mp.mpf(1)/L;eps=mp.mpf(1)/4096;step=eps/8;sM=mp.mpf(8)


def report(x,y):
    E=p*p*(1+x);LL=4*E*(1-E);u=p+p*p*y
    B=4*u*u*(1-u*u);A=LL+(1-LL)*B
    return z*(A+B)-z*z*A*B


rf=mp.diff(lambda x:report(x,0),0);rq=mp.diff(lambda y:report(0,y),0);k0=rq/rf
amp=p*mp.sin(712*theta)
t=F(1,32);v=F(1,320)
ca=(1+t*t)/(1-t*t);sa=2*t/(1-t*t)
cb=(1-v*v)/(1+v*v);sb=2*v/(1+v*v)
Fexact=sa*sb*(2+(ca-1)*(1-cb))/(2*F(1,16)**2)
Fh=mp.mpf(Fexact.numerator)/Fexact.denominator
dmat=4*amp**2*mp.sin(mp.pi/L)**2/(H**2*sM**2)
d0=eps*dmat
delta=(16*12624688*theta-mp.pi/8-2*mp.pi*21418601,
       16*(-4421679)*theta-mp.pi/4-2*mp.pi*(-7501665),mp.mpf(0),mp.mpf(0))


def eta_for_n(n):
    if n==L-1:return -sum(delta)
    q=0
    while n&(1<<q):q+=1
    return delta[q]-sum(delta[:q])


def b_for_n(n):
    return mp.sin(mp.pi/L+eta_for_n(n)/2)**2/mp.sin(mp.pi/L)**2


def main():
    iv=mp.iv;iv.dps=70;one=iv.mpf(1);pp=(iv.sqrt(5)-one)/2
    th=iv.atan2(pp,iv.sqrt(pp));pi=iv.pi
    e0=16*12624688*th-pi/8-2*pi*21418601
    e1=16*(-4421679)*th-pi/4-2*pi*(-7501665)
    upper0=math.nextafter(max(abs(float(e0.a)),abs(float(e0.b))),math.inf)
    upper1=math.nextafter(max(abs(float(e1.a)),abs(float(e1.b))),math.inf)
    eta=math.nextafter(upper0+upper1,math.inf)
    etai=iv.mpf(eta);si=iv.sin(pi/L)
    xii=etai*iv.cos(pi/L)/si+etai**2/(4*si**2)
    xi=math.nextafter(float(xii.b),math.inf)
    max_b=mp.mpf(0);carries=[]
    for n in range(L):
        phase=lambda j:2*mp.pi*j/L+sum(((j>>k)&1)*delta[k] for k in range(4))
        nn=(n+1)%L
        exact=abs(mp.e**(1j*phase(nn))-mp.e**(1j*phase(n)))**2
        expected=4*mp.sin(mp.pi/L+eta_for_n(n)/2)**2
        assert abs(exact-expected)<mp.mpf('1e-90')
        b=b_for_n(n);max_b=max(max_b,abs(b-1))
        carries.append(str(mp.nstr(b,35)))
    assert float(max_b)<xi and eta<2*math.pi/L
    # Uniform derivative certificate for r(0,y) on [-1/1000,1/1000].
    y=iv.mpf([-0.001,0.001]);uu=pp+pp**2*y;LL=4*pp**3;zz=one/2**20
    BB=4*uu**2*(one-uu**2);By=8*pp**2*uu*(one-2*uu**2)
    deriv=By*(zz*(2-LL)-zz**2*(LL+2*(one-LL)*BB))
    assert float(deriv.a)>0 and float(deriv.b)/float(deriv.a)<1.01
    reference=report(0,d0)-report(0,-d0)
    assert reference>0
    weights=[mp.mpf((-1)**(j-1)*comb(8,j))/j for j in range(1,9)]
    r0=report(0,0);total=mp.mpf(0);target=mp.mpf(0);oldres=mp.mpf(0)
    max_rel=mp.mpf(0);scales=[];ws=[];nsites=0
    for n0 in range(L):
     for n1 in range(L):
      # A two-coordinate slice repeated over the two spectator directions;
      # sum rho=256, hence constant coordinate weight 1/256.
      rho=1+mp.sin(2*mp.pi*n0/L)/10+mp.cos(2*mp.pi*n1/L)/20
      vol=mp.mpf(1)/256
      f=mp.sin(2*mp.pi*n0/L)*mp.mpf('.03')+mp.cos(2*mp.pi*n1/L)*mp.mpf('.02')
      matter=mp.cos(2*mp.pi*n0/L)*mp.mpf('.0008')+mp.sin(2*mp.pi*n1/L)*mp.mpf('.0003')
      dy=report(0,d0*b_for_n(n1))-report(0,-d0*b_for_n(n0))
      assert dy>0
      w=dy/reference
      sf2=2*eps*rf*Fh/dy
      assert sf2>0
      xref=eps*Fh/sf2
      dx=report(xref,0)-report(-xref,0)
      assert abs(dx-dy)<mp.mpf('1e-90')
      max_rel=max(max_rel,abs(w-1));scales.append(mp.sqrt(sf2));ws.append(w)
      oldres+=vol*(w-1)*f
      for j in range(1,9):
       arg=j*step/(w*rho)
       total+=weights[j-1]*vol*rho*(dy*(report(arg*f,0)-r0)
                                 +dx*(report(0,-arg*matter)-r0))
      target+=vol*(f-k0*matter);nsites+=1
    expected=step*rf*reference*target
    relerr=abs(total-expected)/(abs(step*rf*reference)+mp.mpf('1e-90'))
    assert relerr<mp.mpf('1e-70')
    assert float(max_rel)<1.01*xi
    # The chosen 8-scale exceeds 4*sqrt(rho_max) for nu_* <=1.
    assert min(scales)>4*mp.sqrt(mp.mpf('1.15'))
    s0=2*p**3;s2=4*p**3;s3=16*p**9
    b0=1-(1-s0)**16;b2=1-(1-s2)**32;b3=1-(1-s3)**32
    ready=b0**158*(b2**4*b3)**79*b3**3
    # Each of two 4-control Gray words uses 16|k| G, 16|k| CX for
    # inverse G, 16 Gray CX and 24 CX for the six controlled swaps.
    runG=16*(12624688+4421679)
    skeletonG=719+runG
    skeletonCX=71+runG+2*(16+24)
    assert (skeletonG,skeletonCX)==(272742591,272742023)
    result={'schema':'d0.carry-compensated-local-geometry/1','status':'PASS',
      'L':L,'site_slice_points':nsites,'all_carries_and_wrap_checked':True,
      'F_H_exact':str(Fexact),'phase_run_lengths':[12624688,-4421679],
      'phase_error_intervals':[str(e0),str(e1)],'eta_upper':eta,'xi_upper':xi,
      'actual_max_relative_edge_error':float(max_b),
      'actual_max_relative_dy_error':float(max_rel),
      'reference_derivative_interval':str(deriv),
      'sample_w_min':float(min(ws)),'sample_w_max':float(max(ws)),
      'sF_min':float(min(scales)),'sF_max':float(max(scales)),
      'normalized_eight_point_identity_error':float(relerr),
      'identity_residual_is_100_digit_numerical_test':True,
      'one_loader_factory_success':str(ready),
      'skeleton_G_calls_before_factories_and_routing':skeletonG,
      'skeleton_CX_calls_before_factories_and_routing':skeletonCX,
      'long_run_lengths_counted_not_replayed':True,
      'native_Toffoli':79,'native_CCZ':3,
      'site_dependent_coframe_compiled':False,'full_geometry_loader_compiled':False,
      'independent_source_rows_bound_physically':False,'Book_cost_info_derived':False,
      'GR_closed':False}
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()

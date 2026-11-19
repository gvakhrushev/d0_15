"""Site-local full-CAR tensor majorants and finite high-frequency reference."""
from fractions import Fraction as F
from itertools import product
from mpmath import iv
import json

from check_bandlimit_joint_hq import curvature_witness


def regularity_test():
    # One SITE controls ten independently regenerated local CAR states:
    # two groups of x, x+e0,...,x+e3. Test the full 128-term q sum.
    L=4; H=F(1,L)
    sites=list(product(range(L),repeat=4))
    xvals={x:(F(sum((i+1)*v for i,v in enumerate(x))%7-3,100),
              F(sum((5-i)*v for i,v in enumerate(x))%9-4,120)) for x in sites}
    eta=(1,-1,-1,-1)
    u=[[F((1 if r==a else 0)*eta[r],4) for a in range(4)] for r in range(4)]
    for x in sites:
        Ds={}
        for r,A in product(range(4),(0,1)):
            y=list(x);y[r]=(y[r]+1)%L;y=tuple(y)
            Ds[r,A]=(xvals[y][A]-xvals[x][A])/H
        direct=sum(eta[a]*u[r][a]*u[s][a]*Ds[r,A]*Ds[s,A]
                   for A,r,s,a in product((0,1),range(4),range(4),range(4)))
        diagonal=sum(eta[r]*F(1,16)*Ds[r,A]**2
                     for A,r in product((0,1),range(4)))
        assert direct==diagonal
    return len(sites)


def factory_cap(N):
    # For each logical Toffoli or counted two-test/phase/plus factory,
    # failure <= 7*(4/5)^L. One fixed initial known-1 factory uses 3 trials.
    L=0
    while 28*N*4**L > 5**L:
        L+=1
    assert 28*N*4**L <= 5**L
    return L


def main():
    nsites=regularity_test()
    B=512;V=2*B
    E=4*V**2+1
    # Entrywise l1 majorant for R2(M)=M(I-E/2+3E²/8).
    R=4*V*(1+E+2*E**2)
    exterior_bound=24*R**4
    # Six faces, CAR trace over 16² entries, dGamma N <= 32 B² per
    # entry, four 16x16 exterior factors have three internal sums, 1/8.
    Cf=(6*16**2*32*B**2*16**3*exterior_bound**4)//8
    Cq=256*B**2  # 128 B²/p < 256 B², since p>1/2
    exponent=max(Cf,Cq).bit_length()
    C=1<<exponent
    assert exponent==973 and Cf<C and Cq<C
    coeff=curvature_witness()*16
    assert coeff==F(16448,65025)
    # Exactly reproduce time and space checkerboard gradients, including wrap.
    L=4;H=F(1,L); a2=F(1,137)
    cnt=0
    for mu in (0,1):
        for x in product(range(L),repeat=4):
            for r in range(4):
                y=list(x);y[r]=(y[r]+1)%L
                grad_factor=F((-1)**y[mu]-(-1)**x[mu],1)/H
                assert grad_factor**2*a2==(4*a2/H**2 if r==mu else 0)
                cnt+=1
    assert cnt==2048
    iv.dps=80
    p=(iv.sqrt(5)-1)/2;z=iv.mpf(1)/2**20;L0=4*p**3
    rf=4*p**2*(1-2*p**2)*z*(1-z*L0)*(1-L0)
    rq=8*p**3*(1-2*p**2)*(z*(2-L0)-z**2*(L0+2*(1-L0)*L0))
    k0=rq/rf
    c=iv.mpf(coeff.numerator)/coeff.denominator
    a=iv.sqrt(c/k0)/2
    assert a*a<iv.mpf(1)/100 and 1-p-a*a>iv.mpf(1)/3
    delta=c/(64*iv.mpf(C)*16*k0)
    assert delta>0 and delta<iv.mpf(1)/2560
    # A strict global SC1 derivative bound on |y|<=1/2560 proves
    # delta*rq <= r(0,delta)-r(0,-delta) <= 3*delta*rq.
    y=iv.mpf([-1,1])/2560;u=p+p*p*y;BB=4*u*u*(1-u*u)
    deriv=8*p*p*u*(1-2*u*u)*(z*(2-L0)-z*z*(L0+2*(1-L0)*BB))
    derivative_ratio=deriv/rq
    assert derivative_ratio>iv.mpf('0.5') and derivative_ratio<iv.mpf('1.5')
    cos2=1-2*p*p
    for _ in range(9):cos2=2*cos2*cos2-1
    vis=(1-cos2)*p**7/2
    b2=1-p**384;b3=1-(1-16*p**9)**64
    beta24=(1-p**40)*(b2**6*b3)**1452
    assert beta24>iv.mpf('.9996') and beta24<1
    gain_lower=beta24*840*p**27*vis*rf**2*c/(131072*16*iv.mpf(C)**2)
    gain_upper=12*gain_lower
    assert gain_lower>iv.mpf('4.2945e-613') and gain_lower<iv.mpf('4.2947e-613')
    # Generic predeclared N: Lcap ensures the union bound <=1/4, p^3<1/4.
    caps={str(N):factory_cap(N) for N in (1,1000000,1000000000000)}
    assert p**3<iv.mpf(1)/4 and 1-16*p**9<iv.mpf(4)/5 and p**6<iv.mpf(4)/5
    print(json.dumps(dict(status='PASS', full_CAR_spacetime_cells_exact=nsites,
      local_matter_groups=2, local_CAR_sites_per_group=5,
      local_CAR_copies_per_Hq_query=10, original_global_Fourier_resource_unchanged=False,
      local_full32_Choi_address_count=32,source_input_nu=1,site_rho=1,
      Hf_normal_projected_degree=82,Hf_all_column_coefficient_bound_bits=exponent,
      full_Hf_and_Hq_candidate_norm_bound='2^973 / H^2',
      Hq_coefficient_bound_less_than='2^26',
      global_Fourier_S256_A32_norm_coefficient_upper='2^40 / H^2',
      global_Fourier_norm_bound_formula='32*(16*A)^2*S^2/(p*H^2), for the explicitly specified unsymmetrized tensor-monomial realization',
      global_S_and_A_scaling='S and A are actual carrier values; S=H^-4 is a particular expanded lattice, not asserted for original Fourier128',
      max_report_fock_blocks=16,high_curvature_F_times_H_squared=str(coeff),
      high_ref_material_amplitude=str(a),high_ref_material_slack_lower='1/3',
      checkerboard_reference_forward_edges_exact=cnt,
      constant_reference_argument_delta=str(delta),
      SC1_y_derivative_ratio_on_safe_interval=str(derivative_ratio),
      selector24_ready_probability=str(beta24),
      gain_lower_coefficient_times_H_squared=str(gain_lower),
      gain_upper_coefficient_times_H_squared=str(gain_upper),
      uniform_bank_ready_lower_if_factory_interface_and_budget_admitted='1/2',
      example_factory_attempt_caps=caps,
      actual_local_state_writer_price_measured=False,
      original_full_physical_COST_INFO_and_GR_closed=False),indent=2,sort_keys=True))

if __name__=='__main__':main()

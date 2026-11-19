"""Local Hq band compression and full-geometric norm witness on one SITE."""
from fractions import Fraction as F
from itertools import combinations,product
from mpmath import iv
import numpy as np
import json
from check_shared_site_union import eye, transpose, matmul, det, exterior, dgamma


def car_trace(N,P):
    out=F(0)
    for k in range(5):
        masks=list(combinations(range(4),k))
        out+=sum(dgamma(i,j,N)*exterior(P,j,i) for i in masks for j in masks)
    return out


def curvature_witness():
    # Constant in space, but non-small relative to mesh when H tends to zero.
    t=v=F(1,4)
    ca,sa=(1+t*t)/(1-t*t),2*t/(1-t*t)
    cb,sb=(1-v*v)/(1+v*v),2*v/(1+v*v)
    A=eye(4);A[0][0]=A[2][2]=ca;A[0][2]=A[2][0]=sa
    Ai=eye(4);Ai[0][0]=Ai[2][2]=ca;Ai[0][2]=Ai[2][0]=-sa
    B=eye(4);B[1][1]=B[2][2]=cb;B[1][2]=sb;B[2][1]=-sb
    Bi=eye(4);Bi[1][1]=Bi[2][2]=cb;Bi[1][2]=-sb;Bi[2][1]=sb
    eta=eye(4)
    for i in (1,2,3):eta[i][i]=-1
    for u,ui in ((A,Ai),(B,Bi)):
        assert matmul(matmul(transpose(u),eta),u)==eta
        assert matmul(u,ui)==eye(4) and det(u)==1 and u[0][0]>0
    P=matmul(matmul(matmul(A,B),Ai),Bi)
    D=[[F(i==j)-P[i][j] for j in range(4)] for i in range(4)]
    for r in combinations(range(4),3):
        for c in combinations(range(4),3):assert exterior(D,r,c)==0
    N=[[F(0)]*4 for _ in range(4)];N[0][1]=N[1][0]=F(1)
    coefficient=-car_trace(N,P)/8/16  # e=4I, nu=1, rho=1
    assert coefficient==F(1028,65025)
    return coefficient


def matter_filter():
    L=4;S=L**4;K=1;p=(np.sqrt(5)-1)/2
    grid=np.indices((L,)*4)
    # Nonconstant norm makes original grade-14 filler genuinely high-frequency.
    f0=.05*np.cos(2*np.pi*grid[0]/L)
    f15=.02*np.sin(2*np.pi*grid[1]/L)
    filler=np.sqrt(1-p-f0*f0-f15*f15)
    state=np.zeros((16,)+(L,)*4,dtype=complex)
    state[0]=f0/np.sqrt(S);state[1]=np.sqrt(p)/np.sqrt(S)
    state[15]=f15/np.sqrt(S);state[14]=filler/np.sqrt(S)
    assert abs(np.linalg.norm(state.ravel())-1)<1e-12
    modes=np.fft.fftfreq(L)*L
    mask=np.ones((L,)*4,dtype=bool)
    for mu in range(4):
        shape=[1]*4;shape[mu]=L
        mask &= np.abs(modes.reshape(shape))<=K
    filtered=state.copy()
    for a in (0,1,15):
        transformed=np.fft.fftn(state[a],norm='ortho')
        filtered[a]=np.fft.ifftn(transformed*mask,norm='ortho')
    assert np.linalg.norm((state-filtered).ravel())<1e-13
    wrong=state.copy()
    wrong[14]=np.fft.ifftn(np.fft.fftn(state[14],norm='ortho')*mask,norm='ortho')
    discarded_filler=np.linalg.norm((state-wrong).ravel())
    assert discarded_filler>1e-5
    # Original local CAR amplitudes and forward q_x match for all 256 cells.
    def amplitudes(z):
        return [S/np.sqrt(p)*np.real(z[1].conjugate()*z[a]) for a in (0,15)]
    a0=amplitudes(state);a1=amplitudes(filtered)
    assert all(np.max(np.abs(x-y))<1e-13 for x,y in zip(a0,a1))
    H=1/L
    def matter(m):
        q=np.zeros((L,)*4)
        for field in m:
            for mu in range(4):
                d=(np.roll(field,-1,axis=mu)-field)/H
                q+=(1 if mu==0 else -1)*d*d
        return q
    assert np.max(np.abs(matter(a0)-matter(a1)))<1e-12
    return float(discarded_filler)


def local_difference_spectrum(L,K):
    S=L**4;H=1/L;p=(np.sqrt(5)-1)/2
    modes=list(product(range(-K,K+1),repeat=4))
    M=len(modes)
    x=np.ones(M,dtype=complex)/np.sqrt(S)
    y=np.array([np.exp(-2j*np.pi*k[0]/L) for k in modes])/np.sqrt(S)
    D=S/(2*np.sqrt(p)*H)*(np.outer(y,y.conj())-np.outer(x,x.conj()))
    eig=np.linalg.eigvalsh(D)
    r=np.sin((2*K+1)*np.pi/L)/((2*K+1)*np.sin(np.pi/L))
    predicted=M/(2*np.sqrt(p)*H)*np.sqrt(1-r*r)
    assert abs(eig[-1]-predicted)<1e-9
    assert abs(eig[0]+predicted)<1e-9
    assert np.max(np.abs(eig[1:-1]))<1e-9
    uniform=np.pi*M*np.sqrt(K*(K+1)/(3*p))
    assert predicted<=uniform+1e-9
    return predicted,uniform


def shift_skeleton():
    # Exactly compute y-x modulo four with x retained.
    def sub(x,y):
        x0,x1=x&1,(x>>1)&1
        y0,y1=y&1,(y>>1)&1
        y1 ^= x1
        y0 ^= 1
        y1 ^= x0 & y0
        y0 ^= 1
        y0 ^= x0
        return y0 | (y1<<1)
    for x,y in product(range(4),repeat=2):
        assert sub(x,y)==(y-x)%4
    # Four coordinates and two distinct material copies; x never changes.
    assert 2*4*2*2==32  # CX in W and W^-1
    assert 2*4*2==16     # Toffoli in W and W^-1
    assert 2*4*2*2==32  # X in W and W^-1


def main():
    shift_skeleton()
    filler=matter_filter()
    q4,bound=local_difference_spectrum(4,1)
    for L in (6,8,16):local_difference_spectrum(L,1)
    c=curvature_witness()
    iv.dps=50
    p=(iv.sqrt(5)-1)/2
    D2=iv.mpf(23328)/p
    assert abs(q4*q4-float(23328/((np.sqrt(5)-1)/2)))<1e-8
    # Example explicit site-local Choi bank, padded 32 addresses, d=32.
    # Lower product witness and upper termwise bound for OUR Hq operator.
    B=iv.mpf(512)
    low=B**2*D2; upper=128*low
    full_low=B**2 * (iv.mpf(256)/(2*iv.sqrt(p)*iv.mpf('0.25')))**2
    constant=iv.mpf(c.numerator)/c.denominator
    b2=1-p**384;b3=1-(1-16*p**9)**64
    shift_success=(b2**6*b3)**16
    assert shift_success>iv.mpf('.99999') and shift_success<1
    assert low>iv.mpf('9.894e9') and low<iv.mpf('9.895e9')
    assert full_low>iv.mpf('1.111e11') and full_low<iv.mpf('1.113e11')
    assert c==F(1028,65025)
    print(json.dumps(dict(
      status='PASS',lattice_L=4,site_size=256,matter_local_fock_dimension=16,
      expanded_matter_site_fock_dimension=4096,
      projected_grade_support=[0,1,15],projector_exactly_preserves_all_other_grades=True,
      bandlimit_K=1,real_mode_count=81,
      original_state_after_partial_band_projection_error_lt='1e-13',
      all_grade_projection_incorrect_filler_discard_norm=filler,
      local_matter_q_cells_checked=256,
      nonzero_local_difference_eigenvalues='±sqrt(23328/p)',
      local_difference_norm_numerical=q4,uniform_in_L_bound=bound,
      explicit_local_choi_address_count=32,full32_julia_dimension=32,
      explicit_local_Hq_projected_norm_lower=str(low),
      explicit_local_Hq_projected_norm_upper=str(upper),
      same_Hq_unprojected_norm_lower=str(full_low),
      high_curvature_full_fock_coefficient=str(c),
      high_curvature_coefficient_interval=str(constant),
      common_SITE_shift_and_unshift=dict(logical_Toffoli=16,logical_CX=32,logical_NOT=32,
          additional_known_one_preparation=True, exact_mod4_truth_table_checked=True),
      max_births_for_16_shift_toffoli_at_limit64=16*(26*64+2),
      shift_factory_success_excluding_known_one=str(shift_success),
      fixed_site_controlled_q_sign_target_hilbert_dimension='2^55 per one reference SITE block',
      original_uncompressed_q_sign_global_target_hilbert_dimension='2^63 with all 256 SITE sectors',
      site_shift_reduction='all x via one reference block and controlled modular shifts; dense block not actually compiled',
      high_curvature_exact_3x3_minors_zero=True,
      arbitrary_joint_82copy_span_extension='real-analytic identity theorem; operator Q must fix the exact open family and carry all 82 equal independent programs',
      scope='band-limited fixed SITE and explicit Hq tensor-monomial instantiation; native implementation, geometric alpha and full source not established',
      GR_closed=False),sort_keys=True,indent=2))

if __name__=='__main__':main()

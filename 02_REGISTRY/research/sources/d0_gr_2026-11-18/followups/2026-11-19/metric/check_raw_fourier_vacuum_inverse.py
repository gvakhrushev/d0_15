"""Direct unary Fourier128 lookup and all-column SourceI G inverse.

Exact Boolean test; numerical 16-column operator check. Factory expansions,
physical births, and full coherent U/raw clock are not numerically replayed.
"""
import itertools,json,math
import numpy as np
import mpmath as mp
from check_fourier_fresh_localization import original_reference

def main():
    chosen,_,S=original_reference();assert S==256 and len(chosen)==64
    # j-index unary decoder with clean scratch: a1..a5 then erase a4..a1.
    def decoder(j,label):
        inp=[(j>>i)&1 for i in range(6)]
        bits=[inp[i]^((label>>i&1)^1) for i in range(6)]
        a=[0]*5;a[0]^=bits[0]&bits[1]
        for i in range(1,5):a[i]^=a[i-1]&bits[i+1]
        flag=a[4]
        for i in range(3,0,-1):a[i]^=a[i-1]&bits[i+1]
        a[0]^=bits[0]&bits[1]
        assert a==[0,0,0,0,flag]
        # reversing the precise computation clears the remaining flag
        for i in range(4):
            if i==0:a[0]^=bits[0]&bits[1]
            else:a[i]^=a[i-1]&bits[i+1]
        for i in range(4,0,-1):a[i]^=a[i-1]&bits[i+1]
        a[0]^=bits[0]&bits[1]
        assert not any(a)
        return flag
    for j,label in itertools.product(range(64),repeat=2):
        assert decoder(j,label)==(j==label)
    bitweight=sum(sum(bin(v).count('1') for v in k) for k in chosen)
    for j in range(64):
        reg=[0]*8
        for label,k in enumerate(chosen):
            f=decoder(j,label)
            for r in range(4):
                for b in range(2):reg[2*r+b]^=f*((k[r]>>b)&1)
        assert all(reg[2*r+b]==((chosen[j][r]>>b)&1) for r in range(4) for b in range(2))
        for y in itertools.product(range(4),repeat=4):
            q=[reg[2*r]*(y[r]&1) for r in range(4)]
            b0=sum(q)%2;b1=0
            for r in range(4):
                b1^=reg[2*r+1]*(y[r]&1)
                b1^=reg[2*r]*((y[r]>>1)&1)
                for u in range(r+1,4):b1^=q[r]*q[u]
            v=sum(chosen[j][r]*y[r] for r in range(4))%4
            assert b0+2*b1==v
    # Full target, port, Spin. Port/Spin may be correlated with oldRIGHT.
    p=(math.sqrt(5)-1)/2;a=math.sqrt(p)
    G=np.array([[a,-p],[p,a]]); Li=np.array([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    src=np.zeros((16,16));swap=np.zeros((16,16));Z=np.zeros((16,16))
    for t,port,spin in itertools.product(range(2),range(2),range(4)):
        col=(t*2+port)*4+spin
        swap[(port*2+t)*4+spin,col]=1
        Z[col,col]=(-1)**t
        for out in range(4):
            src[(t*2+port)*4+out,col]=(int(out==spin) if port==0 else Li[out,spin])
    mm=lambda a,b: np.einsum("ij,jk->ik",a,b,optimize=False)
    routed=mm(mm(mm(swap,src),src),swap)
    Gfull=np.kron(np.kron(G,np.eye(2)),np.eye(4))
    zerr=float(np.linalg.norm(routed-Z,ord=2))
    inv_err=float(np.linalg.norm(mm(mm(routed,Gfull),routed)-Gfull.T,ord=2))
    assert zerr<1e-14 and inv_err<1e-14
    # 64 unary selectors (18 Toffoli each) in each direction.
    lookup_tof=64*18*2;tof=lookup_tof+36
    lookup_cx=2*(384+bitweight); cx=lookup_cx+15
    assert tof==2340
    # 14 direct pluses; 2 H/Toffoli and one plus for each H.
    plus=14+2*tof;nh=2*tof;nccz=tof
    mp.mp.dps=100;pm=(mp.sqrt(5)-1)/2
    s0=2*pm**3;s2=4*pm**3;s3=16*pm**9
    log_gamma=plus*mp.log10(s0)+2*nh*mp.log10(s2)+nccz*mp.log10(s3)
    log_iterations_approx=mp.log10(4*mp.pi)-log_gamma/2
    print(json.dumps({'status':'PASS','L':4,'fourier_labels':64,
      'selector_input_tests':64*64,'address_pair_tests':64*256,
      'lookup_kappa_total_one_bits':bitweight,'logical_Toffoli':tof,
      'logical_CX_lookup_and_b_excluding_births_and_matter':cx,
      'logical_SourceI_lookup_phase':2,'clean_scratch_bits':19,
      'independent_plus_resources_including_14_fourier':plus,
      'H_factory_calls':nh,'CCZ_factory_calls':nccz,
      'all_ready_log10_probability_conditional':str(log_gamma),
      'fourier_localization_a':'gamma/256',
      'amplification_iterations_log10_asymptotic':str(log_iterations_approx),
      'Z_route_matrix_error_16_columns':zerr,'G_inverse_matrix_error_16_columns':inv_err,
      'G_inverse_per_letter_G':1,'G_inverse_per_letter_CX':12,
      'G_inverse_per_letter_SourceI':4,
      'factory_expansions_and_birth_history_replayed':False,
      'field_general_U_C_compiled':False,'equality_or_reflection_compiled':False,
      'physical_admission_port_routes_proved':False,'GR_closed':False},indent=2))

if __name__=='__main__':main()

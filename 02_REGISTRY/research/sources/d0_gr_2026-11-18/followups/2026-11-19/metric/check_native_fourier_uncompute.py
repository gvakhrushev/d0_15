"""Literal Boolean schedule for the original 64-pair real Fourier purifier."""
from itertools import product
from fractions import Fraction
from mpmath import iv
import json
from check_fourier_fresh_localization import original_reference

class BDD:
    def __init__(self):
        self.nodes={};self.unique={}
    def mk(self,depth,lo,hi):
        if lo==hi:return lo
        key=(depth,lo,hi)
        if key not in self.unique:
            ident=2+len(self.nodes);self.nodes[ident]=key;self.unique[key]=ident
        return self.unique[key]
    def compile(self,values):
        def walk(depth,prefix):
            if depth==6:return values[prefix]
            return self.mk(depth,walk(depth+1,prefix*2),walk(depth+1,prefix*2+1))
        return walk(0,0)


def schedule(diagram,roots,j,y,type_in):
    # The eight kappa roots remain live as reversible BDD scratch; no copy.
    bits=[(j>>(5-i))&1 for i in range(6)]
    tmp={0:0,1:1}
    for v in sorted(diagram.nodes):
        depth,l,h=diagram.nodes[v]; x=bits[depth]
        tmp[v]=tmp[l] ^ (x & tmp[l]) ^ (x & tmp[h])
    vals=[tmp[r] for r in roots]
    kap=[vals[2*r]+2*vals[2*r+1] for r in range(4)]
    # Four products q_r, then b0 and the 14-Toffoli b1 sum.
    q=[(kap[r]&1)*(y[r]&1) for r in range(4)]
    b0=0
    for qv in q:b0 ^= qv
    b1=0
    for r in range(4):
        b1 ^= ((kap[r]>>1)&1)*(y[r]&1)
        b1 ^= (kap[r]&1)*((y[r]>>1)&1)
    for r in range(4):
        for s in range(r+1,4):b1 ^= q[r]*q[s]
    b=b0+2*b1
    assert b==sum(kap[r]*y[r] for r in range(4))%4
    type_out=type_in^b0
    phase=-1 if b1 else 1  # SWAP, SourceI^2, SWAP: exact Z on b1
    # Inverse b1, b0 and q computation restores the six scratch bits.
    for r in reversed(range(4)):
        for s in reversed(range(r+1,4)):b1 ^= q[r]*q[s]
    for r in reversed(range(4)):
        b1 ^= (kap[r]&1)*((y[r]>>1)&1)
        b1 ^= ((kap[r]>>1)&1)*(y[r]&1)
    for qv in reversed(q):b0 ^= qv
    for r in reversed(range(4)):q[r] ^= (kap[r]&1)*(y[r]&1)
    assert b0==b1==0 and not any(q)
    for v in sorted(diagram.nodes,reverse=True):
        depth,l,h=diagram.nodes[v];x=bits[depth]
        tmp[v] ^= x&tmp[h]
        tmp[v] ^= x&tmp[l]
        tmp[v] ^= tmp[l]
        assert tmp[v]==0
    return type_out,phase


def main():
    chosen,outside,S=original_reference()
    d=BDD()
    roots=[d.compile([(k[r]>>b)&1 for k in chosen]) for r in range(4) for b in (0,1)]
    assert len(d.nodes)==105
    assert all(l<v and h<v for v,(_,l,h) in d.nodes.items())
    # All columns of the full (Y mod 4, six-bit j, type) unitary.
    for y in product(range(4),repeat=4):
        for j,k in enumerate(chosen):
            b=sum(k[r]*y[r] for r in range(4))%4
            for t in (0,1):
                out,sign=schedule(d,roots,j,y,t)
                assert out==(t^(b&1)) and sign==(-1 if b&2 else 1)
            # Actual Fourier component type=b0 has input phase (-1)^b1.
            out,sign=schedule(d,roots,j,y,b&1)
            assert out==0 and sign*(-1 if b&2 else 1)==1
    # Z from actual SourceI: L_i^2=-I on all four spin columns.
    Li=((0,-1,0,0),(1,0,0,0),(0,0,0,-1),(0,0,1,0))
    for i,j in product(range(4),repeat=2):
        assert sum(Li[i][k]*Li[k][j] for k in range(4))==(-1 if i==j else 0)
    # Exact all-column route of Z from the SOURCE port A to b1, retaining
    # an arbitrary initial A and the full four-coordinate quaternion Spin.
    # Index is (A, b1, spin); SWAP has the actual three-CX implementation.
    size=16
    src=[[0]*size for _ in range(size)]
    swap=[[0]*size for _ in range(size)]
    expect=[[0]*size for _ in range(size)]
    for a,b,spin in product((0,1),(0,1),range(4)):
        col=(a*2+b)*4+spin
        swap[(b*2+a)*4+spin][col]=1
        expect[col][col]=1 if b==0 else -1
        for outspin in range(4):
            src[(a*2+b)*4+outspin][col]=(int(outspin==spin) if a==0 else Li[outspin][spin])
    def mm(A,B):
        return [[sum(A[i][k]*B[k][j] for k in range(size)) for j in range(size)] for i in range(size)]
    assert mm(mm(mm(swap,src),src),swap)==expect
    n=len(d.nodes)
    ntof=4*n+36;ncx=2*n+15
    assert ntof==456 and ncx==225
    # 105 BDD nodes, 4 product bits, 2 accumulator bits, and one zero.
    scratch=n+4+2+1
    assert scratch==112
    iv.dps=70
    p=(iv.sqrt(5)-1)/2;b2=1-p**384;b3=1-(1-16*p**9)**64
    ready=(1-p**40)*(b2**6*b3)**ntof
    assert ready>iv.mpf('.9998770') and ready<iv.mpf('.9998771')
    total80=ready**80
    assert total80>iv.mpf('.9902') and total80<iv.mpf('.9903')
    # Exact refinement identity for the separately selected Fourier+Choi
    # localizations; this does not include actual writer or equality readiness.
    for L in (4,8,16):
        H=Fraction(1,L); S0=L**4
        lhs=Fraction(1,S0)**80*Fraction(21,8*S0+1)**180
        rhs=(Fraction(21,1)/(8+H**4))**180*H**1040
        assert lhs==rhs
    # Gate factories 26L+2 births per Toffoli, plus known-one <= 80
    # and 112 fresh clean scratch wires; excludes routes and source copies.
    births=ntof*(26*64+2)+80+scratch
    assert births==759888
    print(json.dumps(dict(status='PASS',original_fourier_kappa_pairs=64,
      original_reference_L4=S,exact_full_input_columns=S*64*2,
      exact_real_fourier_components_checked=S*64,
      fixed_kappa_lookup_BDD_nodes=n,
      kappa_table_output_bits=8,selector_reads_only_low_site_bits=8,
      cleaned_scratch_bits=scratch,
      literal_logical_toffoli_count=ntof,
      literal_CX_count_excluding_scratch_preparation=ncx,
      literal_SourceI_count_excluding_routes=2,
      scratch_preparation_known_one_conditional=dict(golden_G=scratch,CX=2*scratch),
      exact_Spin_identity_all_four_columns=True,
      exact_routed_sourceI_square_all_port_scratch_spin_columns=16,
      full_uncompute_on_every_bitstring=True,
      per_copy_heralded_W_ready_probability=str(ready),
      eighty_independent_W_ready_probability=str(total80),
      max_listed_births_per_W=births,
      birth_count_excludes='raw Fourier source, physical routing, actual unused programme/circuit ancillas and other source factories',
      exact_refinement_readiness_exponent=1040,
      ideal_conditional_source_upper_exponent=2082,
      refinement_identity_dyadic_levels_checked=[4,8,16],
      operation_order='W_y on original Y, then controlled subtraction and equality filter',
      preserves='site-Y, pair-index j, full unspecified oldRIGHT; type becomes 0 only on the declared Fourier subfamily',
      physical_fresh_purifier_access_proved=False,
      true_original_global_field_writer_cost_computed=False,
      full_cost_info_and_GR_closed=False),indent=2,sort_keys=True))

if __name__=='__main__':main()

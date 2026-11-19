"""Construct a full-column native dyadic smooth CAR reference loader.

The enormous signed G powers are encoded as integer run lengths and checked
by exact integer Walsh/Gray identities. Toffoli is the retained-abort native
factory in check_balanced_factory.py, not a new primitive. Full physical
field-bank price and a common measured clock are not identified.
"""
import json
import math
import numpy as np
import mpmath as mp

mp.mp.dps=120
p=(mp.sqrt(5)-1)/2
theta=mp.atan2(p,mp.sqrt(p))
z=mp.mpf(1)/2**20


def report(x,y):
    E=p**2*(1+x);L=4*E*(1-E);u=p+p**2*y
    B=4*u*u*(1-u*u);A=L+(1-L)*B
    return z*(A+B)-z*z*A*B


rf=mp.diff(lambda x:report(x,0),0)
rq=mp.diff(lambda y:report(0,y),0)
k0=rq/rf
F=mp.mpf(16517734400)/162621047169
H=mp.mpf(1)/4
amp=H*mp.sqrt(F/k0)/(2*mp.sin(mp.pi*H))
beta=mp.asin(amp/p)
epsilon=mp.mpf('0.000001')
threshold=int(mp.ceil(9*mp.pi/epsilon))


def approximant(mult,target):
    x=mult*theta/(2*mp.pi)
    n0,n1,d0,d1=0,1,1,0
    while True:
        a=int(mp.floor(x)); num=a*n1+n0; den=a*d1+d0
        if den>=threshold:break
        n0,n1,d0,d1=n1,num,d1,den
        x=1/(x-a)
    desired=int(mp.nint(target/(2*mp.pi)*den))
    k=(desired*pow(num,-1,den))%den
    choices=[]
    for candidate in (k,k-den):
        turns=int(mp.nint((mult*candidate*theta-target)/(2*mp.pi)))
        error=mult*candidate*theta-target-2*mp.pi*turns
        if abs(error)<epsilon/3:
            choices.append((abs(candidate),candidate,turns,error))
    assert choices
    _,k,turns,error=min(choices)
    return {'mult':mult,'den':den,'numerator':num,'k':k,'turns':turns,
            'error':error,'target':target}


def scalar_interval_checks(approx):
    iv=mp.iv;iv.dps=75
    one=iv.mpf(1);pi=iv.pi;pp=(iv.sqrt(5)-one)/2;zz=one/(2**20)
    rr_f=4*pp**2*(one-2*pp**2)*zz*(one-zz*4*pp**3)*(one-4*pp**3)
    rr_q=8*pp**3*(one-2*pp**2)*(zz*(2-4*pp**3)-zz**2*(4*pp**3+2*(one-4*pp**3)*4*pp**3))
    kval=rr_q/rr_f; f=iv.mpf(16517734400)/iv.mpf(162621047169)
    HH=one/4;am=HH*iv.sqrt(f/kval)/(2*iv.sin(pi*HH))
    ratio=am/pp
    ba=iv.atan2(ratio,iv.sqrt(one-ratio**2))
    th=iv.atan2(pp,iv.sqrt(pp));targets=(ba,)
    bounds=[]
    for v,targ in zip(approx,targets):
        err=v['mult']*v['k']*th-targ-2*pi*v['turns']
        lo,hi=float(err.a),float(err.b)
        bounds.append({'interval':str(err),
                       'abs_upper':math.nextafter(max(abs(lo),abs(hi)),math.inf)})
    assert sum(x['abs_upper'] for x in bounds)<float(epsilon)
    return bounds


def toffoli(bits,c1,c2,t):
    if bits[c1] and bits[c2]:bits[t]^=1


def verify_adjacent_swap(u,v):
    diff=u^v
    assert diff and diff&(diff-1)==0
    target=diff.bit_length()-1
    controls=[i for i in range(4) if i!=target]
    negative=[i for i in controls if not ((u>>i)&1)]
    for state in range(16):
        bits=[(state>>j)&1 for j in range(4)]+[0]
        for i in negative:bits[i]^=1
        toffoli(bits,controls[0],controls[1],4)
        toffoli(bits,4,controls[2],target)
        toffoli(bits,controls[0],controls[1],4)
        for i in negative:bits[i]^=1
        output=sum(bits[j]<<j for j in range(4))
        assert bits[4]==0
        assert output==(v if state==u else u if state==v else state)


def gray_checks(r):
    g=[j^(j>>1) for j in range(1<<r)]
    for target_pattern in range(1<<r):
        signs=[-1 if bin(target_pattern & x).count('1')%2 else 1 for x in g]
        for b in range(1<<r):
            s=sum(sign*(-1 if bin(b & x).count('1')%2 else 1)
                  for sign,x in zip(signs,g))
            assert s==((1<<r) if b==target_pattern else 0)
        for j in range(len(g)):
            dx=g[j]^g[(j+1)%len(g)]
            assert dx and dx&(dx-1)==0


def mat_one(k,M):
    out=np.zeros((16,16))
    for col in range(16):
        b=(col>>k)&1;base=col&~(1<<k)
        for rowb in (0,1):out[base|(rowb<<k),col]=M[rowb,b]
    return out


def mat_cx(c,t):
    out=np.zeros((16,16))
    for j in range(16):out[j^(((j>>c)&1)<<t),j]=1
    return out


def rotation(u,v,angle):
    out=np.eye(16);c,s=math.cos(angle),math.sin(angle)
    out[u,u]=out[v,v]=c;out[v,u]=s;out[u,v]=-s
    return out


def swap_basis(u,v):
    out=np.eye(16);out[u,u]=out[v,v]=0;out[u,v]=out[v,u]=1
    return out


def mm(A,B):
    return np.einsum('ij,jk->ik',A,B,optimize=False)


def mv(A,x):
    return np.einsum('ij,j->i',A,x,optimize=False)


def verify_routed_rotations():
    q=.314159
    # Actual chronological swaps 14<->6,6<->2; its reverse follows the
    # 2<->0 adjacent rotation. Each swap is independently checked as three
    # Toffoli on every CAR column with a returned clean scratch bit.
    P=mm(swap_basis(6,2),swap_basis(14,6))
    made=mm(mm(P.T,rotation(2,0,q)),P)
    assert np.max(np.abs(made-rotation(14,0,q)))<1e-14
    # Literal +G on the target bit rotates |0> toward |2>, so it is
    # R_(0,2)(+q), equivalently R_(2,0)(-q); do not invert that sign.
    made=mm(mm(P.T,rotation(0,2,q)),P)
    assert np.max(np.abs(made-rotation(14,0,-q)))<1e-14
    # 0->1->3->7; the remaining adjacent pair is 7<->15.
    P=mm(mm(swap_basis(3,7),swap_basis(1,3)),swap_basis(0,1))
    made=mm(mm(P.T,rotation(7,15,q)),P)
    assert np.max(np.abs(made-rotation(0,15,q)))<1e-14


def verify_exact_site_phases():
    # SITE bit s is never a target. a,b are fresh zero scratch qubits.
    # pi/2 on adjacent CAR pair 7,15: compute a=c0&c1,b=c2&s;
    # CCZ(a,b,c3) then Toffoli(a,b,c3), then uncompute.
    for car in range(16):
     for s in (0,1):
      x=[(car>>i)&1 for i in range(4)]+[s,0,0]
      toffoli(x,0,1,5);toffoli(x,2,4,6)
      sign=-1 if x[5] and x[6] and x[3] else 1
      toffoli(x,5,6,3)
      toffoli(x,2,4,6);toffoli(x,0,1,5)
      actual=sum(x[j]<<j for j in range(4))
      assert (x[4],x[5],x[6])==(s,0,0)
      assert (actual,sign)==((15,1) if s and car==7 else
                             (7,-1) if s and car==15 else (car,1))
    # pi on nonadjacent pair 0,15 is two diagonal 5-control signs.
    # For each CAR pattern compute two pairs into a,b; CCZ(a,b,s);
    # undo pairs and the four X gates used for the zero pattern.
    for car in range(16):
     for s in (0,1):
      x=[(car>>i)&1 for i in range(4)]+[s,0,0];sign=1
      for desired in (0,15):
       for i in range(4):
        if not ((desired>>i)&1):x[i]^=1
       toffoli(x,0,1,5);toffoli(x,2,3,6)
       if x[5] and x[6] and x[4]:sign*=-1
       toffoli(x,2,3,6);toffoli(x,0,1,5)
       for i in range(4):
        if not ((desired>>i)&1):x[i]^=1
      assert sum(x[j]<<j for j in range(4))==car
      assert (x[4],x[5],x[6])==(s,0,0)
      assert sign==(-1 if s and car in (0,15) else 1)


def verify_base_sign():
    # Phase -1 on CAR states with low bits 10: X(bit0), CZ(0,1), X(bit0).
    # This flips |14> but not |0>,|1>,|15>; four minus signs preserve SO(16).
    for car in range(16):
        x=[(car>>i)&1 for i in range(4)]
        x[0]^=1
        sign=-1 if x[1] and x[0] else 1
        x[0]^=1
        assert sum(x[j]<<j for j in range(4))==car
        assert sign==(-1 if car in (2,6,10,14) else 1)


def test_complete_loader(approx):
    pp=float(p);aa=math.sqrt(pp);gg=np.array([[aa,-pp],[pp,aa]])
    xx=np.array([[0.,1.],[1.,0.]])
    word=mat_one(0,gg)
    for bit in (1,2,3):word=mm(mat_one(bit,xx),word)
    for bit in (1,2,3):word=mm(mat_cx(0,bit),word)
    original=np.eye(16)[:,1]
    first=mv(word,original)
    assert np.max(np.abs(first-np.eye(16)[:,1]*aa+np.eye(16)[:,14]*pp))<1e-14
    # Return the actual unwrapped certified residual before using a small
    # trigonometric argument; no huge lossy floating-point angle is needed.
    errs=[float(x['error']) for x in approx]
    ideal_beta=float(beta);actual_beta=ideal_beta+errs[0]
    phase=np.eye(16)
    for i in (2,6,10,14):phase[i,i]=-1
    Ubase=mm(mm(phase,rotation(14,0,-ideal_beta)),word)
    Abase=mm(mm(phase,rotation(14,0,-actual_beta)),word)
    wanted_amp=float(amp)
    norms=[];vectors=[];blocks=[]
    for n in range(4):
        phase=2*math.pi*n/4
        actual_phase=phase  # both site phases are exact finite gate words
        ideal=mm(rotation(0,15,phase),Ubase)
        actual=mm(rotation(0,15,actual_phase),Abase)
        blocks.append(actual)
        norms.append(float(np.linalg.norm(actual-ideal,2)))
        target=np.zeros(16);target[1]=aa;target[0]=wanted_amp*math.cos(phase)
        target[14]=math.sqrt(1-pp-wanted_amp**2)
        target[15]=wanted_amp*math.sin(phase)
        vectors.append(float(np.linalg.norm(mv(ideal,original)-target)))
        assert np.linalg.norm(mm(ideal.T,ideal)-np.eye(16))<1e-13
        assert np.linalg.det(ideal)>0.999999999999
    assert max(vectors)<1e-13
    assert max(norms)<=sum(abs(x) for x in errs)+1e-14
    U=np.zeros((64,64))
    for n,B in enumerate(blocks):U[16*n:16*(n+1),16*n:16*(n+1)]=B
    for n in range(4):
        P=np.zeros((64,64));P[16*n:16*(n+1),16*n:16*(n+1)]=np.eye(16)
        assert np.max(np.abs(mm(U,P)-mm(P,U)))==0
    return {'all_16_columns_each_site':True,'site_values_tested':4,
            'max_target_vector_error':max(vectors),
            'observed_full_column_operator_error':max(norms)}


def main():
    approx=[approximant(8,beta)]
    # 14->6->2->0, and 0->1->3->7->15. Each adjacent swap is
    # a three-Toffoli clean-ancilla word plus at most six controlled X.
    for u,v in ((14,6),(6,2),(0,1),(1,3),(3,7)):
        verify_adjacent_swap(u,v)
    gray_checks(3);gray_checks(4)
    verify_routed_rotations()
    verify_exact_site_phases()
    verify_base_sign()
    full=test_complete_loader(approx)
    bounds=scalar_interval_checks(approx)
    # Base: 4 adjacent swaps x3 Toffoli; one direct CZ corrects its sign.
    # Site bit 0: six swaps
    # x3 plus controlled exact quarter-turn 5 =23. Site bit 1: two
    # exact selected phases, each 4 Toffoli =8. Total 43, 3 CCZ and 1 CZ.
    ntof=12+23+8
    s0=2*p**3;s2=4*p**3;s3=16*p**9
    b0=1-(1-s0)**16;b2=1-(1-s2)**32;b3=1-(1-s3)**32
    factory_ready=b0**(2*ntof)*(b2**4*b3)**ntof*b3**3*b2
    totalG=8*abs(approx[0]['k'])
    # Checked actual signs/control patterns: target pair 2,0 has 3 zero
    # controls and the chosen k is positive, so all eight powers are +G^k.
    assert approx[0]['k']>0
    def swap_control_X(u,v):
        target=(u^v).bit_length()-1
        return 2*sum(not ((u>>j)&1) for j in range(4) if j!=target)
    base_flips=2*(swap_control_X(14,6)+swap_control_X(6,2))
    site0_flips=2*sum(swap_control_X(u,v) for u,v in ((0,1),(1,3),(3,7)))
    site1_flips=8  # four zero-controls, pre- and post-phase
    # Initial uses +G rather than G^-1 (-2 CX), and phase |14> adds 2 CX.
    skeleton_cx=19+8+base_flips+site0_flips+site1_flips+2
    assert (base_flips,site0_flips,skeleton_cx)==(12,24,73)
    iv=mp.iv;iv.dps=70;one=iv.mpf(1);pp=(iv.sqrt(5)-one)/2
    bb0=one-(one-2*pp**3)**16
    bb2=one-(one-4*pp**3)**32
    bb3=one-(one-16*pp**9)**32
    ready_iv=bb0**(2*ntof)*(bb2**4*bb3)**ntof*bb3**3*bb2
    result={'schema':'d0.dyadic-smooth-car-loader/1','status':'PASS',
      'L':4,'site_bits_for_one_direction':2,'CAR_dimension':16,
      'source_two_reference_components':True,'geometric_reference_F':str(F),
      'known_one_and_clean_CAR_prep':'required and explicitly charged',
      'controlled_plane_rotation_approximants':[{'gray_block_size':v['mult'],
        'CF_denominator':v['den'],'G_run_length':v['k'],'wraps':v['turns'],
        'certified_angle_error':b} for v,b in zip(approx,bounds)],
      'sum_certified_error_upper':sum(v['abs_upper'] for v in bounds),
      'maximum_Toffoli_in_each_attempt':ntof,
      'maximum_additional_CCZ_in_each_attempt':3,
      'maximum_additional_CZ_in_each_attempt':1,
      'both_SITE_phase_words_exact':True,
      'explicit_G_calls_in_gray_rotation_runs':totalG,
      'G_calls_outside_heralded_factories_including_prep':totalG+7,
      'CX_calls_outside_heralded_factories_including_prep':skeleton_cx,
      'born_CAR_and_two_clean_scratch_outside_factories':6,
      'plus_resource_pairs_before_field':2*ntof,
      'success_probability_for_fresh_capped_factories':str(factory_ready),
      'success_probability_interval':str(ready_iv),
      'success_probability_for_32_independent_fresh_loaders':str(factory_ready**32),
      'full_column_check':full,'unselected_site_projectors_exact':True,
      'all_aborts_retained':True,'full_geo_bank_loaded':False,
      'paid_clock_compiled':False,'Book_cost_info_identified':False,
      'GR_closed':False}
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()

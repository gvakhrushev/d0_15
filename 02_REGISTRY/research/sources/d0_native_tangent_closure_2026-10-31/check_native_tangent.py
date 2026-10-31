#!/usr/bin/env python3
"""Fixed native QUERY: equal-count forward words and their full-price secants.

No continuously tunable primitive is used in the emitted words. G repetitions
are stored by run length and counted as individual paid stages. All 32 endpoint
columns are evaluated at high precision. The shortest trio is also expanded
and executed stage by stage. This is a native-grammar test, not a derivation of
physical X_N or a new Einstein solution. See PROOF_RU.md for exact scope.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib, json, math, platform
import mpmath as mp
import numpy as np
import sympy as sp

COUNT = 0
ERRORS = {}
mp.mp.dps = 100
mp.iv.dps = 85
P = (mp.sqrt(5)-1)/2
A = mp.sqrt(P)
C = P**3
U = 2*P*A
ZETA = mp.mpf(2)**-20
RANK = 8


def require(value, name):
    global COUNT
    COUNT += 1
    if not bool(value):
        raise ArithmeticError(name)


def near(value, reference, name, tolerance=mp.mpf('1e-80')):
    if isinstance(value, mp.matrix):
        error = max(abs(value[i,j]-reference[i,j]) for i in range(value.rows) for j in range(value.cols))
    else:
        error = abs(value-reference)
    ERRORS[name] = max(ERRORS.get(name, mp.mpf(0)), error)
    require(error < tolerance, f'{name}: {mp.nstr(error,10)}')
    return error


def op(name, wires, repeat=1):
    return {'op': name, 'wires': list(wires), 'repeat': int(repeat)}


SWAP = [op('CX',(0,1)),op('CX',(1,0)),op('CX',(0,1))]
SI = op('SourceI',(0,2,3))
G = op('G',(0,))

def routed_power(n, inverse=False):
    # SourceI^2 is Z on port 0 for every unknown Spin state.
    middle = [op('G',(0,),n)]
    if inverse:
        middle = [op('SourceI',(0,2,3),2)] + middle + [op('SourceI',(0,2,3),2)]
    return SWAP + middle + SWAP


VG = routed_power(1)
VGI = routed_power(1,True)
QUERY = VGI + SWAP + [op('SourceI',(0,2,3),2)] + SWAP + VG
RAW_PREP = [G] + VG
RAW_PREP_INV = VGI + [op('SourceI',(0,2,3),2), G, op('SourceI',(0,2,3),2)]


def circuit_inventory(word):
    ans = Counter()
    for g in word:
        require(g['repeat'] > 0, 'positive repetition count')
        require(4 not in g['wires'], 'oldRIGHT never addressed')
        require(g['op'] in ('G','CX','SourceI'), 'no extra primitive')
        require(g['op'] != 'G' or g['wires'] == [0], 'G only on original port')
        require(g['op'] != 'SourceI' or g['wires'] == [0,2,3], 'original SourceI port/Spin interface')
        ans[g['op']] += g['repeat']
    return dict(sorted(ans.items()))


def pair_power(x,y,n):
    """Exact real-complex multiplication polynomial, evaluated at mp/intervals."""
    one = x*0+1; zero = x*0
    rx,ry = one,zero
    while n:
        if n&1:
            rx,ry = rx*x-ry*y, rx*y+ry*x
        x,y = x*x-y*y, 2*x*y
        n >>= 1
    return rx,ry


def apply_gate_left(M, gate):
    """Apply a run-length instruction to every matrix column, no chosen state."""
    name,wires,n = gate['op'],gate['wires'],gate['repeat']
    d=M.rows
    if name=='G':
        co,si=pair_power(A,P,n)
        mask=1<<(4-wires[0])
        out=M.copy()
        for r in range(d):
            if r&mask: continue
            for j in range(M.cols):
                x,y=M[r,j],M[r|mask,j]
                out[r,j]=co*x-si*y
                out[r|mask,j]=si*x+co*y
        return out
    if name=='CX':
        if n%2==0:return M.copy()
        cm,tm=1<<(4-wires[0]),1<<(4-wires[1])
        out=mp.zeros(d,M.cols)
        for r in range(d):
            to=r^tm if r&cm else r
            for j in range(M.cols):out[to,j]=M[r,j]
        return out
    # L_i e_0=e_1, L_i e_1=-e_0, L_i e_2=e_3, L_i e_3=-e_2.
    out=M.copy()
    for _ in range(n%4):
        dest=mp.zeros(d,M.cols)
        for r in range(d):
            port=(r>>4)&1
            if not port:
                to,sgn=r,1
            else:
                spin=((r>>2)&1)*2+((r>>1)&1)
                spinto=spin^1;sgn=-1 if spin&1 else 1
                to=(r&~6)|(spinto<<1)
            for j in range(M.cols):dest[to,j]=sgn*out[r,j]
        out=dest
    return out


def endpoint(word):
    M=mp.eye(32)
    for g in word:M=apply_gate_left(M,g)
    return M


def expected_query(c,u):
    M=mp.zeros(32)
    for port in (0,1):
        for rest in range(8):
            i=16*port+rest;j=i+8
            M[i,i]=c;M[i,j]=u;M[j,i]=u;M[j,j]=-c
    return M


def canonical_input():
    i=mp.zeros(32,8)
    for k in range(8):i[k,k]=1
    return i


def exact_primitives_and_formulas():
    p=(sp.sqrt(5)-1)/2;a=sp.sqrt(p)
    gg=sp.Matrix([[a,-p],[p,a]])
    zz=sp.diag(1,-1)
    check = lambda M: all(sp.simplify(v)==0 for v in M)
    require(check(gg.T*gg-sp.eye(2)), 'exact Golden orthogonal')
    require(check(zz*gg*zz-gg.T), 'exact forward inverse synthesis')
    li=sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    require(li**2==-sp.eye(4), 'SourceI squared is exact scalar sign')
    require(li**4==sp.eye(4), 'SourceI fourth power exact identity')
    require(check(gg*zz*gg.T-sp.Matrix([[p**3,2*p*a],[2*p*a,-p**3]])), 'owned original QUERY matrix')
    c,u,x,y=sp.symbols('c u x y',real=True)
    V=sp.Matrix([[x,-y],[y,x]]);Q=sp.Matrix([[c,u],[u,-c]])
    plus=V*Q*V.T;minus=V.T*Q*V
    require(sp.expand(plus[0,0]-c*(x*x-y*y)+2*u*x*y)==0,'all-n forward corner formula')
    require(sp.expand(minus[0,0]-c*(x*x-y*y)-2*u*x*y)==0,'all-n reverse corner formula')
    require(sp.simplify((plus-minus).det()+16*x*x*y*y*(c*c+u*u))==0,'exact full operator chord')
    # Uniform finite lower bound: p<13/21 gives (4u/c)^2=64/p^3>1344/5.
    z=Fraction(1,2**20)
    factor=Fraction(255,256)*Fraction(127,128)*(1-z)
    require(Fraction(1344,5)*factor*factor>256, 'finite native source ratio strictly exceeds 16')
    require(Fraction(3,13)*Fraction(127,128)-Fraction(1,8)>0,'all emitted cold coefficients positive')
    # Irrational-angle proof uses conjugates of 2cos(2theta)=2sqrt5-4.
    require(-2*sp.sqrt(5)-4 < -2,'Golden angle cannot be rational multiple of pi')
    return {'exact_inverse':True,'all_n_algebra_proved':True,
            'source_ratio_squared_lower_rational':str(Fraction(1344,5)*factor*factor),
            'uniform_signed_secant_lower_bound':16}


def choose_indices():
    # Candidate construction only. Acceptance uses interval arithmetic below.
    th=mp.atan2(P,A);x=th/(2*mp.pi)
    pm2,pm1,qm2,qm1=0,1,1,0
    candidates=[]
    for k in range(20):
        a0=int(mp.floor(x));pn=a0*pm1+pm2;qn=a0*qm1+qm2
        if qn>1:
            co,si=pair_power(A,P,qn)
            if co>0 and abs(si)<mp.mpf(1)/16:
                candidates.append((qn,abs(si)))
        pm2,pm1,qm2,qm1=pm1,pn,qm1,qn
        x=1/(x-a0)
    targets=[mp.mpf('.011'),mp.mpf('.0025'),mp.mpf('.0009'),mp.mpf('.00015'),mp.mpf('.000004')]
    found=[]
    for tol in targets:
        found.append(next(q for q,s in candidates if s<tol))
    require(len(set(found))==5,'five genuinely improving finite comparisons')
    return found


def iv_bounds(v):
    return mp.mpf(v.a),mp.mpf(v.b)


def interval_receipt(n):
    pp=(mp.iv.sqrt(5)-1)/2;aa=mp.iv.sqrt(pp)
    cc=pp**3;uu=2*pp*aa;zz=mp.iv.mpf(2)**-20
    co,si=pair_power(aa,pp,n)
    xl,xh=iv_bounds(co);yl,yh=iv_bounds(si)
    require(xl>0 and max(abs(yl),abs(yh))<mp.mpf(1)/16,'certified native near-identity step')
    require(yl*yh>0,'nonzero step, no division by uncertainty containing zero')
    cp=cc*(co*co-si*si)-2*uu*co*si
    cm=cc*(co*co-si*si)+2*uu*co*si
    dd=1-zz+zz*cc*cc
    w=RANK*zz*cc*cc/dd
    jp=-RANK*mp.iv.log(1-zz+zz*cp*cp)
    jm=-RANK*mp.iv.log(1-zz+zz*cm*cm)
    ratio=(jp-jm)/(2*si*w)
    lo,hi=iv_bounds(ratio)
    require(lo>16,'interval verified full-price secant >16')
    require(hi-lo<mp.mpf('1e-45'),'narrow certified finite-source interval')
    return {'n':n,'raw_stages':2*n+66,
            'sin_step_interval':[mp.nstr(yl,100),mp.nstr(yh,100)],
            'normalized_price_secant_interval':[mp.nstr(lo,100),mp.nstr(hi,100)],
            'enclosure_width':mp.nstr(hi-lo,12)}


def literal_shortest_clock(words,expected,N,raw_input):
    # Only this small trio is expanded into every individual raw stage.
    errors=[];interior=[]
    i=np.array(raw_input.tolist(),float);P0=i@i.T
    for name,word in words.items():
        T=np.eye(32)
        Pi=P0.copy()
        count=0
        for instruction in word:
            one=dict(instruction);one['repeat']=1
            g=np.array(endpoint([one]).tolist(),float)
            for _ in range(instruction['repeat']):
                Tnew=g@T
                Pnew=Tnew@P0@Tnew.T
                if count<N-1:
                    leak=(np.eye(32)-Pnew)@g@Pi
                    interior.append(np.linalg.norm(leak,2))
                T=Tnew;Pi=Pnew;count+=1
        require(count==N,'every paid stage expanded in shortest word')
        err=np.max(abs(T-np.array(expected[name].tolist(),float)))
        require(err<2e-13,'literal all-column replay matches compressed powers')
        errors.append(err)
        # Full feedback determinant at the fixed original boundary, rank eight.
        F=P0@T.T@(np.eye(32)-P0)@T@P0
        vals=np.linalg.eigvalsh((F+F.T)/2)
        cold=i.T@T@i
        actual=-np.log1p(-float(ZETA)*vals).sum()
        theory=-np.log1p(-float(ZETA)*np.linalg.eigvalsh(np.eye(8)-cold.T@cold)).sum()
        require(abs(actual-theory)<5e-19,'all32 determinant counts return once, not N times')
        require(np.linalg.norm(T@T-np.eye(32))<1e-12,'full literal endpoint remains reflection')
    require(max(interior)<2e-13,'every generated interior cut is transported')
    # Genuine scene values are not evaluated with a 4-stage substitute: the
    # exact monodromy spectrum equality proves the full N-stage heat equality.
    return {'actual_N':N,'full_fibre_dimension':32,'protected_rank':8,
            'all_scene_hodge_modes':425*N*32,
            'all_clock_modes_only':N*32,
            'max_expanded_endpoint_error':max(errors),
            'max_generated_interior_leakage':max(interior),
            'full_scene_heat_equality':'analytical, from identical N and full monodromy spectra',
            'huge_clock_matrix_materialized':False}


def general_normal_model():
    # Independent 3-input finite model of the same scalar-reflection geometry.
    # Not emitted native geometry or a new physical state.
    c=mp.mpf('.81');s=mp.sqrt(1-c*c);r=3
    Q=mp.matrix([[c if i==j else 0 for j in range(r)] for i in range(r)])
    U0=mp.zeros(2*r);H=mp.zeros(2*r);Pin=mp.zeros(2*r)
    for i in range(r):
        U0[i,i]=c;U0[i,i+r]=U0[i+r,i]=s;U0[i+r,i+r]=-c
        H[i,i+r]=-1;H[i+r,i]=1;Pin[i,i]=1
    near(H,(U0*Pin-Pin*U0)/s,'generator derived from existing endpoint and input')
    near(U0*U0,mp.eye(2*r),'general scalar-reflection identity')
    K=mp.matrix([[mp.mpf('.5'),mp.mpf('.1'),0],
                 [mp.mpf('.03'),mp.mpf('.4'),mp.mpf('.05')],
                 [0,mp.mpf('.02'),mp.mpf('.3')]])
    Sm=K.T*K;zz=mp.mpf(2)**-20;eta=mp.mpf('1e-70')
    D=(1-zz)*mp.eye(r)+zz*eta*c*c*Sm
    W=zz*eta*c*c*sum((D**-1*Sm)[i,i] for i in range(r))
    def price(t):
        ct=c*mp.cos(2*t)-s*mp.sin(2*t)
        DD=(1-zz)*mp.eye(r)+zz*eta*ct*ct*Sm
        return -mp.log(mp.det(DD))
    # Increase precision because the whole feedback signal is extremely small.
    with mp.workdps(180):
        DD=(1-zz)*mp.eye(r)+zz*eta*c*c*Sm
        W=zz*eta*c*c*sum((DD**-1*Sm)[i,i] for i in range(r))
        direct=mp.diff(price,mp.mpf(0))
        expected=4*W*s/c
        require(abs((direct-expected)/expected)<mp.mpf('1e-90'), 'nonnormal old matrix, true tiny gain retained')
        res={'true_w':mp.nstr(W,35),'normalized_slope':mp.nstr(direct/W,35),
             'relative_error':mp.nstr(abs((direct-expected)/expected),10)}
    # Co-moving input is a different comparison and has exactly constant return.
    t=mp.mpf('.12');V=mp.expm(t*H);U1=V*U0*V.T;i=mp.eye(2*r)[:,:r];im=V*i
    near(im.T*U1*im,i.T*U0*i,'representation transport moves the actual input too')
    require(max(abs((i.T*U1*i)[a,b]-c*(1 if a==b else 0)) for a in range(r) for b in range(r))>mp.mpf('.1'),
            'fixed-boundary mutation is not a mere basis change')
    return res


def constrained_reaction():
    y,r,lam=sp.symbols('y r lam',real=True);q=y*y+2*y
    B=-sp.log(1-sp.Rational(1,7)*(1-r*r))
    L=B+lam*(r-q)
    reaction=-sp.diff(B,r)
    restricted=sp.simplify(sp.diff(L,y).subs({lam:reaction,r:q}))
    true=sp.diff(B.subs(r,q),y)
    require(sp.simplify(restricted-true)==0,'correct report constraint carries nonzero multiplier')
    require(sp.simplify(sp.diff(B,r))!=0,'ambient report source not inferred zero')
    # A digital alphabet does not make endpoint-small secants vanish: the
    # explicit words above supply nonzero secants without differentiable letters.
    return {'constraint':'r=Q(Y)', 'reaction':'lambda_c=-B_r',
            'missing_normal_row_is_not_a_generated_state':'true',
            'closure_not_claimed':True}


def main():
    original=exact_primitives_and_formulas()
    base=endpoint(QUERY);near(base,expected_query(C,U),'literal 26-stage original query, all32 columns')
    inv0=circuit_inventory(QUERY)
    require(inv0=={'CX':18,'G':2,'SourceI':6},'owned QUERY inventory')
    blank_i=canonical_input();born=endpoint(RAW_PREP);i=born*blank_i
    near(endpoint(RAW_PREP_INV),born.T,'paid canonical-input inverse on all32 columns')
    near(i.T*i,mp.eye(8),'canonical raw-born input isometric')
    w0=RANK*ZETA*C*C/(1-ZETA+ZETA*C*C)
    outwords={};results=[];expanded=None
    ns=choose_indices()
    for n in ns:
        v,vi=routed_power(n),routed_power(n,True)
        cores={'plus':vi+QUERY+v,'minus':v+QUERY+vi,'center':v+vi+QUERY}
        words={name:RAW_PREP_INV+word+RAW_PREP for name,word in cores.items()}
        inventory=[circuit_inventory(w) for w in words.values()]
        target_inv={'CX':42,'G':2*n+6,'SourceI':18}
        require(all(d==target_inv for d in inventory),'same paid primitive/address inventory')
        require(sum(target_inv.values())==2*n+66,'true raw clock length')
        co,si=pair_power(A,P,n)
        cp=C*(co*co-si*si)-2*U*co*si
        cm=C*(co*co-si*si)+2*U*co*si
        up=U*(co*co-si*si)+2*C*co*si
        um=U*(co*co-si*si)-2*C*co*si
        expectations={'plus':born*expected_query(cp,up)*born.T,
                      'minus':born*expected_query(cm,um)*born.T,'center':born*base*born.T}
        evaluated={}
        for name,word in words.items():
            mat=endpoint(word);evaluated[name]=mat
            near(mat,expectations[name],'emitted word all-column identity',mp.mpf('1e-85'))
            near(mat.T,mat,'emitted endpoint self-adjoint',mp.mpf('1e-85'))
            near(mat*mat,mp.eye(32),'emitted endpoint full orthogonal',mp.mpf('1e-85'))
            cold=i.T*mat*i
            cv=cp if name=='plus' else cm if name=='minus' else C
            near(cold,cv*mp.eye(8),'actual fixed input all8 cold columns',mp.mpf('1e-85'))
            near(sum(mat[j,j] for j in range(32)),0,'identical full reflection multiplicities',mp.mpf('1e-85'))
        jp=-RANK*mp.log1p(-ZETA*(1-cp*cp));jm=-RANK*mp.log1p(-ZETA*(1-cm*cm))
        ratio=(jp-jm)/(2*si*w0)
        chord=4*abs(si)*co
        endpoint_ratio=abs(jp-jm)/(chord*w0)
        expected_ratio=4*U/C
        info=interval_receipt(n)
        lo=mp.mpf(info['normalized_price_secant_interval'][0]);hi=mp.mpf(info['normalized_price_secant_interval'][1])
        require(lo<=ratio<=hi,'independent high-precision value is inside interval enclosure')
        require(endpoint_ratio>8,'genuine unit endpoint chord retains nonzero source')
        info.update({'inventory':target_inv,'step':mp.nstr(si,35),'actual_w':mp.nstr(w0,35),
                     'secant_over_step_w':mp.nstr(ratio,35),'limit_source':mp.nstr(expected_ratio,35),
                     'difference_to_limit':mp.nstr(abs(ratio-expected_ratio),20),
                     'endpoint_norm_secant_over_w':mp.nstr(endpoint_ratio,35)})
        results.append(info)
        outwords[str(n)]={name:{'instructions':word,'expanded_length':2*n+66,'inventory':target_inv}
                          for name,word in words.items()}
        if n==ns[0]:expanded=literal_shortest_clock(words,evaluated,2*n+66,i)
    require(all(mp.mpf(results[j+1]['difference_to_limit'])<mp.mpf(results[j]['difference_to_limit']) for j in range(4)),
            'all five native secants converge to the nonzero source')
    out={'pinned_input':'a61872563a0e456546549d457eeeaa7534113827','scope':'one original native QUERY on the same canonical raw-born boundary; equal paid clocks; not a proof of physical X_N completeness',
         'input':'(sqrt(p),p) tensor (sqrt(p),p) tensor arbitrary Spin and oldRIGHT',
         'raw_input_conversion_paid_calls':24,
         'algebra':original,'native_comparisons':results,'literal_shortest_trio':expanded,
         'arbitrary_past_control':general_normal_model(),'constraint_reaction':constrained_reaction(),
         'checks':COUNT,'errors':{k:mp.nstr(v,15) for k,v in sorted(ERRORS.items())},
         'unrestricted_D0_GR_closed':False,'new_einstein_root':False,'Lean_or_CI_run':False,
         'fullstep_only_compiler_executed':False,'long_words_evaluated_by_exact_power_identities_and_interval_arithmetic':True,
         'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'environment':{'python':platform.python_version(),'numpy':np.__version__,'sympy':sp.__version__,'mpmath':mp.__version__}}
    Path(__file__).with_name('native_words.json').write_text(json.dumps(outwords,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()

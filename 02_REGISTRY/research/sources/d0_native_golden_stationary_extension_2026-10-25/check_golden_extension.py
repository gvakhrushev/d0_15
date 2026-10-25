#!/usr/bin/env python3
"""New native Golden code, integral-ring and logical-herald controls.

Only the new16-column native code is evaluated. The old parent/13-qubit
extension is counted, not matrix-replayed. The64-column Boolean target
model is not a replay of the960-stage raw Boolean factory.
"""
import argparse
from dataclasses import replace
from datetime import datetime, timezone
from functools import reduce
import hashlib
import importlib.util
import json
from math import factorial
from pathlib import Path
import sys
import mpmath as mp
import sympy as sp

PACKET=Path(__file__).resolve().parent
SOURCES=PACKET.parent
REPO=SOURCES.parents[2]
DOMAIN=SOURCES/'d0_native_execution_domain_2026-10-24'
sys.path.insert(0,str(DOMAIN))
import native_execution as ne
spec=importlib.util.spec_from_file_location('_complete_record_parent',SOURCES/'d0_known_port_complete_record_price_2026-10-25/helper.py')
parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
CHECKS=[]


def check(label,condition):
    if not condition:raise AssertionError(label)
    CHECKS.append(label)


def eq(a,b):
    if not isinstance(a,sp.MatrixBase):a,b=sp.Matrix([[a]]),sp.Matrix([[b]])
    return ne.exact_matrix_equal(a,b)


def num(x):return mp.mpf(str(sp.N(x,110)))


def sign5(x):
    cs=sp.to_number_field(x,sp.sqrt(5)).coeffs()
    b,a=(sp.Rational(0),cs[0]) if len(cs)==1 else cs
    if b==0:return int(sp.sign(a))
    if a==0 or a*b>0:return int(sp.sign(b))
    delta=a*a-5*b*b
    return int(sp.sign(delta) if a>0 else -sp.sign(delta))


def mul(a,b):
    out=0
    while b:
        if b&1:out^=a
        b>>=1;a<<=1
    for power in range(out.bit_length()-1,3,-1):
        if out&(1<<power):out^=0b10101<<(power-4)
    return out


REDUCE_CACHE={}
def ring(x):
    if x in REDUCE_CACHE:return REDUCE_CACHE[x]
    out=0
    for c in sp.to_number_field(x,ne.A).coeffs():
        if c.q!=1:raise ValueError('not an integral Golden polynomial')
        out=mul(out,2)^(int(c)%2)
    REDUCE_CACHE[x]=out
    return out


def row_sums(M):
    return tuple(reduce(int.__xor__,(ring(M[i,j]) for j in range(M.cols)),0) for i in range(M.rows))


def embed(M,wire,n):
    out=sp.zeros(1<<n);mask=1<<(n-1-wire)
    for col in range(1<<n):
        bit=int(bool(col&mask))
        for new in (0,1):out[(col&~mask)|new*mask,col]=M[new,bit]
    return out


def logical_gate(op,qs,n=6):
    """Owned logical factory TARGET, never an extra native letter."""
    out=sp.zeros(1<<n)
    for col in range(1<<n):
        bits=[(col>>(n-1-q))&1 for q in range(n)];row=col;sign=1
        if op=='X':row^=1<<(n-1-qs[0])
        elif op=='CCX':
            if bits[qs[0]] and bits[qs[1]]:row^=1<<(n-1-qs[2])
        elif op=='CCZ':
            if all(bits[q] for q in qs):sign=-1
        else:raise ValueError(op)
        out[row,col]=sign
    return out


def coin_word():
    return ne.Execution(4,(0,1,2,3),(),
        (ne.Gate('G',(0,)),ne.Gate('CX',(0,1)),ne.Gate('CX',(0,3))),ne.G_CX,
        report_bits=(1,2,3))


def herald_controls():
    # Order(c,u,v,DATA,GOOD,scratch); predicate semantics use scratch0.
    recipe=[('X',(0,)),('X',(1,)),('X',(2,)),
            ('CCX',(0,1,5)),('CCX',(5,2,4)),('CCX',(0,1,5)),
            ('X',(0,)),('X',(1,)),('X',(2,)),('CCX',(0,2,4)),
            ('CCX',(0,1,5)),('CCZ',(5,2,3)),
            ('CCX',(5,2,3)),('CCX',(0,1,5))]
    U=sp.eye(64)
    for op,qs in recipe:U=logical_gate(op,qs)*U
    check('logical TARGET recipe is full64-column orthogonal with7Toffoli1CCZ6X',
          U.T*U==sp.eye(64) and sum(op=='CCX' for op,_ in recipe)==7
          and sum(op=='CCZ' for op,_ in recipe)==1 and sum(op=='X' for op,_ in recipe)==6)
    correct=True
    for c in (0,1):
        for u in (0,1):
            for v in (0,1):
                for d in (0,1):
                    col=(c<<5)|(u<<4)|(v<<3)|(d<<2)
                    g=int((not c and not u and not v) or (c and v))
                    new_d=d^(c*u*v);sign=(-1)**(c*u*v*d)
                    row=(c<<5)|(u<<4)|(v<<3)|(new_d<<2)|(g<<1)
                    correct &= U[row,col]==sign and sum(abs(U[k,col]) for k in range(64))==1
    check('GOOD and controlledJ are correct on ALL16 initialized scratch/input columns',correct)
    prep=ne.Execution(6,(1,2,4,5),(),(ne.Gate('G',(1,)),ne.Gate('G',(2,))),ne.G_CX)
    P=ne.word_matrix(prep,max_qubits=6,max_expanded_stages=100)
    init=ne.input_isometry(prep,max_qubits=6,max_expanded_stages=100)
    M=U*P*init
    p,a=ne.P,ne.A;X=sp.Matrix([[0,1],[1,0]])
    ks={'00':p**3*sp.eye(2),'10':a*p*(sp.eye(2)+X),
        '01':-a*p*(sp.eye(2)-X),'11':sp.zeros(2)}
    check('COMPLETE raw X-cycle alphabet includes failed and zero branches',
          eq(sum((k.T*k for k in ks.values()),sp.zeros(2)),sp.eye(2)))
    effects={};maps={};total=sp.zeros(4)
    for tu,ku in ks.items():
        for tv,kv in ks.items():
            raw=embed(ku,1,6)*embed(kv,2,6)*M
            for g in (0,1):
                selected=sp.Matrix(raw)
                for i in range(64):
                    if ((i>>1)&1)!=g:selected[i,:]=sp.zeros(1,4)
                effect=selected.T*selected
                effects[g,tu,tv]=effect;maps[g,tu,tv]=selected;total+=effect
    check('all GOOD/X outcomes together have EXACT full logical GramI4',eq(total,sp.eye(4)))
    CG=sp.diag(sp.eye(2),ne.G_LOCAL);Q=sp.zeros(64,4)
    for c in (0,1):
        for d in (0,1):
            for u in (0,1):
                for v in (0,1):Q[(c<<5)|(u<<4)|(v<<3)|(d<<2)|2,2*c+d]=sp.Rational(1,2)
    good=maps[1,'10','10'];gamma=4*p**8
    check('successful raw-X transfer is2p4CG with retained plus resources',
          eq(good,2*p**4*Q*CG) and eq(good.T*good,gamma*sp.eye(4)))
    check('FULL remaining GOOD/X failure effect is1minus4p8, not discarded',
          eq(total-good.T*good,(1-gamma)*sp.eye(4)))
    bad=effects[0,'10','10']
    w0=4*p**6*(2*a*p+p**2)**2;w1=4*p**6*a**2*(a+p)**2
    check('a nonready record has control-dependent effect despite scalar success',
          eq(bad,sp.diag(w0,w0,w1,w1)) and not eq(w0,w1)
          and eq(w0-w1,4*p**7*(a+p-1)*(3*a*p+1)))
    s0,s2,s3=2*p**3,4*p**3,16*p**9
    gamma_bool=s0**14*s2**28*s3**8
    check('successful herald factor is annihilated in integral mod2 quotient',
          all(ring(x)==0 for x in 2*p**4*CG))
    return dict(logical_columns=64,initialized_truth_columns=16,logical_input_rank=4,
                logical_counts={'CCX':7,'CCZ':1,'X':6},
                raw_X_success_scalar='2p^4',success_probability='4p^8 Gamma_Bool',
                Gamma_Bool='(2p^3)^14 (4p^3)^28 (16p^9)^8',
                gamma_total_noninterval=mp.nstr(num(gamma*gamma_bool),65),
                raw_boolean_recipe_inventory={'G':274,'CX':686,'stages':960},
                scope='logical Boolean TARGET plus complete raw-X instrument conditioned on BooleanREADY;960-stage counts are analytic recipes, no full raw word emitted or matrix-replayed',
                nonready_effect_noninterval=[mp.nstr(num(w0),60),mp.nstr(num(w1),60)])


def run():
    CHECKS.clear();mp.mp.dps=100
    t=0b111;lam=0b110
    check('characteristic2 quotient has NONZERO squarezero t',t!=0 and mul(t,t)==0 and mul(lam,lam)==1)
    G=ne.G_LOCAL;CG=sp.diag(sp.eye(2),G);CG2=sp.diag(sp.eye(2),G*G)
    check('odd controlledG has nonuniform row sums; native evenpower passes',
          row_sums(CG)==(1,1,lam,lam) and row_sums(CG2)==(1,1,1,1))
    check('native source-I signed permutation preserves residue ones',row_sums(ne.SOURCE_I_LOCAL)==(1,)*8)
    code=coin_word();V=ne.word_matrix(code,max_qubits=4,max_expanded_stages=10)
    check('actual3stage coin-writer is full16-column unitary and respects ring invariant',
          eq(V.T*V,sp.eye(16)) and row_sums(V)==(lam,)*16)
    initial=ne.input_isometry(code,max_qubits=4,max_expanded_stages=10)
    expected=sp.zeros(16,1);expected[0]=ne.A;expected[13]=ne.P
    check('actual coin and typed000/101 containers have exactly p,p2 probabilities',
          eq(V*initial,expected) and eq((V*initial).T*(V*initial),sp.ones(1)))
    encoder=replace(code,gates=code.gates[1:],blank_wires=(1,2,3))
    E=ne.word_matrix(encoder,max_qubits=4,max_expanded_stages=10)
    j=ne.input_isometry(encoder,max_qubits=4,max_expanded_stages=10)
    length=sp.diag(*(1+(i&1) for i in range(16)))
    check('actual full-input original0/10 length effect isIpluscoin1',eq(j.T*E.T*length*E*j,sp.diag(1,2)))
    check('real code corner is sqrtp; all container columns stay in the carrier',
          eq(initial.T*V*initial,sp.Matrix([[ne.A]]))
          and ne.inventory(code,max_qubits=4,max_expanded_stages=10).full_dimension==16)
    X=sp.Matrix([[0,1],[1,0]])
    parity=embed(X,1,4)*embed(X,3,4);even=(sp.eye(16)+parity)/2;odd=sp.eye(16)-even
    Gz=embed(ne.G_LOCAL,0,4);ZGz=embed(sp.diag(1,-1)*ne.G_LOCAL,0,4)
    check('full parity sectors give phases0,pi,plus/minustheta withmultiplicity4',
          eq((V-Gz)*even,sp.zeros(16)) and eq((V-ZGz)*odd,sp.zeros(16))
          and even.trace()==odd.trace()==8 and eq(V*V*odd,odd) and eq((V*odd).trace(),0))
    O=sp.Matrix(4,4,sp.symbols('o:16'));iold=sp.eye(4)[:,:2]
    inew=sp.kronecker_product(iold,initial)
    check('tensor word transports EVERY old protected corner by sqrtp',
          eq(inew.T*sp.kronecker_product(O,V)*inew,ne.A*(iold.T*O*iold)))
    base=parent.execution(1,recorded=True);n=base.qubits
    extra=(ne.Gate('G',(n,)),ne.Gate('CX',(n,n+1)),ne.Gate('CX',(n,n+3)))
    full=replace(base,qubits=n+4,blank_wires=(*base.blank_wires,*range(n,n+4)),
                 gates=base.gates+extra,report_bits=(*base.report_bits,n+1,n+2,n+3))
    inv=ne.inventory(full,max_qubits=13,max_expanded_stages=10000)
    check('actual parent plus3stage extension keeps true135clock8192carrier rank4',
          (inv.g_count,inv.source_i_count,inv.cx_count,inv.gate_count,inv.full_dimension,inv.cut_rank)==(21,40,74,135,8192,4)
          and 2*inv.gate_count*inv.full_dimension==2211840)
    old=parent.data(1)
    check('the actual parent satisfies the compact input needed for the new source bound',
          sign5(old['q'])>0 and sign5(sp.Rational(1,4)-old['q'])>0
          and sign5(old['s']**2-sp.Rational(9,16))>0)
    u,z,T,r=sp.symbols('u z T r',positive=True);Q0=1-z+z*(1-u)*T
    J=-r*sp.log(Q0);w=r*z*(1-u)*T/Q0
    check('independent coin Book source is its ACTUAL weight over1minusu',sp.cancel(sp.diff(J,u)-w/(1-u))==0)
    q,d,ga=sp.symbols('q d gamma',positive=True)
    S=1-d*ga*q;Jq=-r*sp.log(1-z+z*ne.P*S*S)
    wq=r*z*ne.P*S*S/(1-z+z*ne.P*S*S)
    check('original field source keeps its report coefficient with NEW weight',sp.cancel(sp.diff(Jq,q)-wq*(2*d*ga/S))==0)
    check('Golden code price and first source vanish by EXACT Kraft identities',
          eq(ne.P+ne.P**2,1) and eq(ne.P+2*ne.P**2,1+ne.P**2))
    check('actual generator row has a strict configured allmode heat remainder bound',
          sp.Rational(64,2**135*factorial(135))<sp.Rational(1,2**129)
          and sp.Rational(9,4*2**20)>sp.Rational(1,2**19)
          and sp.Rational(1,2**129)<sp.Rational(1,2**19))
    herald=herald_controls()
    p=num(ne.P);ell=-mp.log(p);h=-p*mp.log(p)-p*p*mp.log(p*p)
    check('separately evaluated Golden entropy equals declared code charge',abs(ell*(1+p*p)-h)<mp.mpf('1e-90'))
    return dict(status='PASS',checks=len(CHECKS),check_names=list(CHECKS),
                coin_native=dict(stages=3,full_columns=16,phase_multiplicities={'0':4,'pi':4,'+theta':4,'-theta':4},
                    whole_parent_stages=135,whole_parent_dimension=8192,cut_rank=4,paired_modes=2211840),
                code_info_increment_noninterval=mp.nstr(h,80),code_length_increment_noninterval=mp.nstr(1+p*p,80),
                ring=dict(modulus='x4+x2+1=(x2+x+1)^2',nilpotent_t=t,one_plus_t=lam,
                          scope='integral reduction of actual finite words; clean all-input gate obstruction only'),
                heralded=herald,
                scope=['actual16-column native coin-writer and full-input length effect',
                    'parent13-qubit word validated/counted; no8192 matrix/clock simulation',
                    'logical64 Boolean target and complete raw-X outcomes conditional on BooleanREADY',
                    'herald success doesnot give clean native gate or full raw Book corner',
                    'code component neutral; independent Book controller row retained; no fullCost/GR promotion'])


def pin(p):
    b=p.read_bytes();return dict(path=str(p.relative_to(REPO)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())


def section_pin(heading):
    b=(REPO/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md').read_bytes();s=b.index(heading.encode());e=b.find(b'\n## ',s+1);b=b[s:e if e>=0 else None]
    return dict(heading=heading,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())


def main():
    pa=argparse.ArgumentParser(description=__doc__);pa.add_argument('--output',type=Path);args=pa.parse_args();result=run()
    paths=[PACKET/n for n in ('check_golden_extension.py','CLEAN_BOUNDARY.md','HERALDED_CONTROL.md','ALL_BRANCHES.md')]
    paths += [DOMAIN/n for n in ('native_execution.py','book_price.py')]
    paths += [SOURCES/'d0_known_port_complete_record_price_2026-10-25'/n for n in ('helper.py','CQ_SOURCE.md','COMPLETION_MAP.md','CHECK_RESULT.json')]
    paths += [SOURCES/'d0_known_port_task_source_2026-10-25'/n for n in ('TASK_MAP.md','HEAT_TRANSFER.md')]
    paths += [SOURCES/'d0_native_gr_completion_synthesis_2026-10-20/book_source/GOLDEN_EXACT_DETECTOR.md',
              SOURCES/'d0_native_gr_completion_synthesis_2026-10-20/book_source/DETERMINANT_PREPARATION_BANK.md',
              SOURCES/'d0_native_terminal_code_writer_2026-10-25/WRITER_PROOF.md',
              SOURCES/'d0_known_port_native_cofield_2026-10-25/SOURCE_TRANSFER.md',
              SOURCES/'d0_native_price_cofield_forks_2026-10-25/COFIELD_THEOREM.md',
              SOURCES.parent/'A4D_LITERAL_GOLDEN_CNOT_ACTIVE_LIE_COMPLETENESS_AND_C2_SOURCE_2026_10_19.md',
              SOURCES.parent/'A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md']
    result['source_pins']=[pin(p) for p in paths];result['section_pins']=[section_pin('## '+s+'.') for s in ('7j','7y','7ai','7aj','7ak','7al')]
    result['generated_utc']=datetime.now(timezone.utc).isoformat()
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')


if __name__=='__main__':main()

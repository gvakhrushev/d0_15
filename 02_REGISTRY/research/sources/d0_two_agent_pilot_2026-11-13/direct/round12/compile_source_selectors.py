#!/usr/bin/env python3
"""Exact source-DAG mass and common-readiness Golden-prefix selector tables.

Tables specify coherent reversible classical targets; no Boolean primitive or
completed native writer is inferred. Original Lambda=2^1525 is unchanged.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import lcm
from pathlib import Path
import hashlib
import json


@dataclass(frozen=True)
class K:
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self,'a',F(self.a));object.__setattr__(self,'b',F(self.b))
    @staticmethod
    def of(x):return x if isinstance(x,K) else K(x)
    def __add__(self,y):
        y=K.of(y);return K(self.a+y.a,self.b+y.b)
    __radd__=__add__
    def __neg__(self):return K(-self.a,-self.b)
    def __sub__(self,y):return self+-K.of(y)
    def __rsub__(self,y):return K.of(y)+-self
    def __mul__(self,y):
        y=K.of(y);return K(self.a*y.a+self.b*y.b,self.a*y.b+self.b*y.a-self.b*y.b)
    __rmul__=__mul__
    def __truediv__(self,y):
        y=K.of(y);norm=y.a*y.a-y.a*y.b-y.b*y.b
        assert norm
        return self*K((y.a-y.b)/norm,-y.b/norm)
    def __pow__(self,n):
        assert type(n) is int and n>=0
        ans=K(1);base=self
        while n:
            if n&1:ans=ans*base
            base=base*base;n//=2
        return ans
    def sign(self):
        # 2(a+bp)=(2a-b)+b sqrt(5); compare exact rational squares.
        x,y=2*self.a-self.b,self.b
        if not y:return (x>0)-(x<0)
        if not x:return (y>0)-(y<0)
        if (x>0)==(y>0):return 1 if x>0 else -1
        bigger=x*x>5*y*y
        return (1 if x>0 else -1) if bigger else (1 if y>0 else -1)
    def absolute(self):return self if self.sign()>=0 else -self
    def encode(self):return [str(self.a),str(self.b)]


P=K(0,1);ONE=K(1);ZERO=K();PHI=K(1,1)


def fib(n):
    a,b=0,1
    for _ in range(n):a,b=b,a+b
    return a


def compile_palette(partitions):
    """One ready probability D/2^r for every coherently supplied palette index."""
    D=1
    for part in partitions:
        assert sum(part,ZERO)==ONE and all(w.sign()>=0 for w in part)
        for w in part:D=lcm(D,w.a.denominator,w.b.denominator)
    r=(D-1).bit_length()
    # D clears all fractions. Abort is retained; its mass is 1-D/2^r.
    tables=[[[int(D*w.a),int(D*w.b)] for w in part]+[[2**r-D,0]] for part in partitions]
    n=0
    while any(a<0 or b<0 for table in tables for a,b in table):
        tables=[[[a+b,a] for a,b in table] for table in tables];n+=1
        assert n<10000
    capacities=[2**r*fib(n+1),2**r*fib(n)]
    for part,table in zip(partitions,tables):
        assert [sum(pair[i] for pair in table) for i in (0,1)]==capacities
        for w,(a,b) in zip(part,table[:-1]):
            assert (K(a,b)*(P**n))/2**r==w*F(D,2**r)
        assert K(*table[-1])*(P**n)/2**r==K(1-F(D,2**r))
    return {'common_D_integer':str(D),'fair_bits_r':r,'golden_coins_n':n,
            'ready_probability_rational':str(F(D,2**r)),
            'capacity_by_prefix_kind':[str(x) for x in capacities],
            'partitions':[{'weights':[w.encode() for w in part],
                           'counts_ready_then_abort':[[str(x) for x in pair] for pair in table]}
                          for part,table in zip(partitions,tables)],
            'last_label_is_abort':True,
            'semantics':'all r fair and n Golden coins prepared; retain unconsumed suffix, labels and decode work coherently; readiness depends on neither field/data nor palette control'}


def add_poly(x,y):
    out=dict(x)
    for key,val in y.items():out[key]=out.get(key,ZERO)+val
    return {key:v for key,v in out.items() if v!=ZERO}


def scale_poly(x,c):return {key:v*c for key,v in x.items() if v*c!=ZERO}


def mul_poly(x,y):
    out={}
    for (a,b),v in x.items():
        for (c,d),w in y.items():out[a+c,b+d]=out.get((a+c,b+d),ZERO)+v*w
    return {key:v for key,v in out.items() if v!=ZERO}


def report_polynomial(sigma):
    one={(0,0):ONE};s={(1,0):ONE};t={(0,1):ONE}
    sub=lambda x,y:add_poly(x,scale_poly(y,-1))
    E=scale_poly(add_poly(one,scale_poly(s,F(1,64))),P**2)
    u=add_poly(scale_poly(one,P),scale_poly(t,sigma*(P**2)/64))
    ell=scale_poly(mul_poly(E,sub(one,E)),4);u2=mul_poly(u,u)
    B=scale_poly(mul_poly(u2,sub(one,u2)),4)
    A=add_poly(ell,mul_poly(sub(one,ell),B));z=F(1,2**20)
    out=sub(one,mul_poly(sub(one,scale_poly(B,z)),sub(one,scale_poly(A,z))))
    assert len(out)==27 and out[2,8]==-64*(P**20)*K(F(1,64))**10*K(z)**2
    return out


def main():
    here=Path(__file__).resolve().parent;previous=here.parent/'round11'
    dag_path=previous/'SOURCE_TENSOR_DAG.json';dag=json.loads(dag_path.read_text())
    binding=json.loads((previous/'PERIODIC_SOURCE_BINDING.json').read_text())
    assert binding['A_active']==2049
    A=2049;mass=[];visits=[];leaves=[]
    for i,node in enumerate(dag['nodes']):
        op=node['op']
        if op=='const':m=K(F(node['a']),F(node['b'])).absolute();v=1;l=0
        elif op=='var':
            m=K({'choi_coframe':16*A,'choi_link':32*A,'matter_X':1}[node['kind']]);v=1;l=1
        elif op=='add':
            m=sum((mass[k] for k in node['args']),ZERO)
            v=1+max(visits[k] for k in node['args']);l=max(leaves[k] for k in node['args'])
        else:
            m=ONE
            for k in node['args']:m=m*mass[k]
            v=1+sum(visits[k] for k in node['args']);l=sum(leaves[k] for k in node['args'])
        mass.append(m);visits.append(v);leaves.append(l)
    reachable=set()
    def mark(i):
        if i in reachable:return
        reachable.add(i)
        for k in dag['nodes'][i].get('args',[]):mark(k)
    for i in dag['roots'].values():mark(i)
    # One common rational palette even when an unused/dummy VM slot is reached.
    partitions=[[ONE]];cache={(ONE,):0};node_palette={}
    for i in sorted(reachable):
        node=dag['nodes'][i]
        if node['op']!='add':continue
        weights=tuple(mass[k]/mass[i] for k in node['args'])
        assert all(w.b==0 for w in weights)
        if weights not in cache:cache[weights]=len(partitions);partitions.append(list(weights))
        node_palette[str(i)]=cache[weights]
    internal=compile_palette(partitions)
    internal['node_to_palette']=node_palette
    top_parts=[];top_keys=[]
    for site in binding['site_bindings']:
        inverse_pf=F(site['inverse_PF_once'])
        for name,i in dag['roots'].items():
            w=mass[i]*inverse_pf/2**1525
            assert w.sign()>0 and (ONE-w).sign()>0
            top_parts.append([w,(ONE-w)/2,(ONE-w)/2]);top_keys.append([site['SITE_index'],name])
    top=compile_palette(top_parts);top['palette_keys']=top_keys
    top['ready_labels']=['execute_normalized_tensor_DAG','positive_identity','negative_identity']
    beta_parts=[];beta_keys=[];polys={}
    for sigma in (-1,1):
        poly=report_polynomial(sigma);polys[str(sigma)]={f'{a},{b}':v.encode() for (a,b),v in sorted(poly.items())}
        for mask in range(1024):
            signs=[1 if mask&(1<<i) else -1 for i in range(10)]
            beta=ZERO
            for (a,b),coefficient in poly.items():
                sign=1
                for x in signs[:a]+signs[2:2+b]:sign*=x
                beta+=coefficient*sign
            assert beta.sign()>0 and (ONE-beta).sign()>0
            beta_parts.append([beta,ONE-beta]);beta_keys.append([sigma,mask])
    post=compile_palette(beta_parts);assert post['ready_probability_rational']=='1'
    post['palette_keys']=beta_keys;post['ready_labels']=['REPORT_1','REPORT_0']
    for name,obj in [('INTERNAL_SELECTOR_PALETTE.json',internal),('TOP_SOURCE_SELECTOR_PALETTE.json',top),('TEN_SIGN_REPORT_PALETTE.json',post)]:
        (here/name).write_text(json.dumps(obj,separators=(',',':'))+'\n')
    ir=dag['roots']['H_f_before_inverse_PF'];iq=dag['roots']['H_q_before_inverse_PF']
    T=2*visits[ir]+8*visits[iq];L=2*leaves[ir]+8*leaves[iq]
    tau_i=F(internal['ready_probability_rational']);tau_t=F(top['ready_probability_rational'])
    Ki=Kt=1
    while T*(1-tau_i)**Ki>F(1,8):Ki+=1
    while 10*(1-tau_t)**Kt>F(1,8):Kt+=1
    # All attempts are paid, including after first success. The first ready
    # label is used coherently; other labels/raw prefixes remain retained.
    M=T*Ki*internal['fair_bits_r']+10*Kt*top['fair_bits_r']+post['fair_bits_r']+L
    G=T*Ki*internal['golden_coins_n']+10*Kt*top['golden_coins_n']+post['golden_coins_n']
    Kfair=1
    while M*F(53,100)**Kfair>F(1,4):Kfair+=1
    assert (ONE-2*P**3-K(F(53,100))).sign()<0
    union_bound=M*F(53,100)**Kfair+T*(1-tau_i)**Ki+10*(1-tau_t)**Kt
    assert union_bound<=F(1,2)
    result={
      'status':'EXACT_FULL_SOURCE_SELECTOR_TARGETS_WITH_COMMON_READY',
      'source_dag_sha256':hashlib.sha256(dag_path.read_bytes()).hexdigest(),
      'source_binding_sha256':hashlib.sha256((previous/'PERIODIC_SOURCE_BINDING.json').read_bytes()).hexdigest(),
      'A_active':A,'Lambda_h_unchanged':'2^1525',
      'source_root_masses_before_inverse_PF':{name:mass[i].encode() for name,i in dag['roots'].items()},
      'source_walk_max_node_visits':{name:visits[i] for name,i in dag['roots'].items()},
      'source_walk_max_X_leaves':{name:leaves[i] for name,i in dag['roots'].items()},
      'internal_palette_count':len(partitions),'internal_add_occurrence_types':len(node_palette),
      'internal_r':internal['fair_bits_r'],'internal_n':internal['golden_coins_n'],
      'top_palette_count':len(top_parts),'top_r':top['fair_bits_r'],'top_n':top['golden_coins_n'],
      'post_palette_count':len(beta_parts),'post_r':post['fair_bits_r'],'post_n':post['golden_coins_n'],
      'padded_interpreter_slots_per_ten_sign_report':T,
      'leaf_involution_fair_bits_per_report':L,
      'selector_fair_qubits_per_report':M,'selector_Golden_qubits_per_report':G,
      'retained_selector_caps':{'internal':Ki,'top':Kt,'fair_plus_bank':Kfair},
      'ready_probabilities':{'internal_slot':internal['ready_probability_rational'],
                             'top_slot':top['ready_probability_rational'],'postprocessor':'1'},
      'selector_readiness_exact':f"[1-(1-({internal['ready_probability_rational']}))^{Ki}]^{T} * [1-(1-({top['ready_probability_rational']}))^{Kt}]^10",
      'single_attempt_plus_bank_success':'s_F=2p^3',
      'selector_plus_bank_readiness':f'[1-(1-2p^3)^{Kfair}]^{M}',
      'combined_selector_and_fair_bank_ready_lower_bound':'1/2',
      'combined_failure_union_bound_rational':str(union_bound),
      'paid_fair_bank_attempts_per_report':M*Kfair,
      'full_native_READY_computed':False,
      'missing_for_full_READY':'actual Boolean/routing/H/Toffoli implementation and its additional fair resources, retained native controller/mark/readout schedule; source banks prepared separately',
      'original_report_coefficients':polys,
      'scope':'exact selector tables, scalar normalized-DAG contract and fair-bank component of readiness; not a completed physical gate word or chosen Info',
      'GR_closed':False}
    (here/'SELECTOR_COMPILATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in ['status','internal_palette_count','internal_r','internal_n','top_r','top_n','post_r','post_n','padded_interpreter_slots_per_ten_sign_report','selector_fair_qubits_per_report','selector_Golden_qubits_per_report']}))


if __name__=='__main__':main()

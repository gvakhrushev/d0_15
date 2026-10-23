#!/usr/bin/env python3
"""Original full128 PORT-first-return: exact scalar refinement and C1 source.

Actual pinned CAR16 matrices and analytic r/nu jets; arbitrary joint input
theorem; no reset, native cost or stopping predicate replacement. Direct
total-cap-3 stopped leaves are compared with a single-map all-pair formula.
"""
import argparse
import ast
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import time
import numpy as np
from scipy.linalg import expm, solve_sylvester

parser=argparse.ArgumentParser(description=__doc__)
siblings=Path(__file__).resolve().parent.parent
parser.add_argument('--native',type=Path,default=siblings/'d0_book_uniform_source_2026-10-21/check_uniform_book_source.py')
parser.add_argument('--entropy-owner',type=Path,default=siblings/'d0_native_complete_cq_source_2026-10-22/check_complete_history_source.py')
parser.add_argument('--json',type=Path)
parser.add_argument('--skip-direct',action='store_true',help='omit the bounded direct cap-3 replay')
args=parser.parse_args()
started=time.monotonic()
P=(np.sqrt(5)-1)/2; ELL=-np.log(P); T=2*P*P
I=np.eye(16,dtype=complex); ZERO=np.zeros_like(I)
checks=[]
def require(ok,why):
    if not bool(ok): raise ArithmeticError(why)
    checks.append(why)
def adj(x): return x.conj().T
def herm(x): return (x+adj(x))/2
def trace(x): return float(np.trace(x).real)
def load_functions(path,names,env,blob=None,sha256=None):
    raw=path.read_bytes()
    if blob:
        require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==blob,
                'immutable original CAR16 constructor blob')
    if sha256:
        require(hashlib.sha256(raw).hexdigest()==sha256,'immutable owned complete-CQ jet definitions')
    found=set()
    for node in ast.parse(raw.decode()).body:
        if isinstance(node,ast.FunctionDef) and node.name in names:
            exec(compile(ast.Module(body=[node],type_ignores=[]),str(path),'exec'),env)
            found.add(node.name)
    require(found==names,'only requested existing definitions loaded')

native={'np':np,'expm':expm,'solve_sylvester':solve_sylvester,'P':P,'EYE':I}
load_functions(args.native,{'adj','herm','tr','root','creators','native'},native,
               blob='ee8de4635d24c668949ac9a0186616ab7d59f2ed')
owner={'np':np,'expm':expm,'solve_sylvester':solve_sylvester,'P':P,'EYE':I}
load_functions(args.entropy_owner,{'adj','herm','native_joint_jet','prepared'},owner,
               sha256='cd0052f10bc43abb3736a1637c850c2a3d637f428dd116f6320f68bcf84e3931')
r=1/9;nu=3/5;theta=2*np.arctanh(r);dtheta=2/(1-r*r)
k,kr,_=owner['native_joint_jet'](native,theta,nu,dtheta,0.)
delta,ddelta,rho,drho,Z=owner['prepared'](k,kr)
h=16/Z
hr=16*trace(np.linalg.inv(delta)@ddelta@np.linalg.inv(delta))/Z**2
dn=-nu*hr/(2*h)
_,kv,_=owner['native_joint_jet'](native,theta,nu,dtheta,dn)
_,ddelta_v,_,drho_v,_=owner['prepared'](k,kv)
require(abs(trace(np.linalg.inv(delta)@ddelta_v@np.linalg.inv(delta)))<1e-11,
        'actual one-port-null v has dZ=0')
require(all(not np.count_nonzero(k[j]) and not np.count_nonzero(kv[j])
            for j in range(128) if (j//4)&1),'all exact dark physical slots and jets retained')

pair_rows=[j for j in range(1,64) if np.count_nonzero(k[2*j])]
require(len(pair_rows)==31,'31 live paired rows; all 63 physical paired rows retained')
pair=np.array([k[2*j]/P for j in pair_rows])
dpair_r=np.array([kr[2*j]/P for j in pair_rows])
dpair_v=np.array([kv[2*j]/P for j in pair_rows])
for j,M in zip(pair_rows,pair):
    require(np.linalg.norm(k[2*j]-P*M)<1e-15 and
            np.linalg.norm(k[2*j+1]-np.sqrt(P)*M)<1e-15,
            'actual original paired scalar refinement row '+str(j))
def forward(ks,x): return sum((a@x@adj(a) for a in ks),ZERO.copy())
def backward(ks,x): return sum((adj(a)@x@a for a in ks),ZERO.copy())
def backward_jet(ks,dks,x,dx):
    return sum((adj(da)@x@a+adj(a)@dx@a+adj(a)@x@da for a,da in zip(ks,dks)),ZERO.copy())
def effect(ks,dks):
    return (herm(backward(ks,I)),herm(backward_jet(ks,dks,I,ZERO)))
Cpair,_=effect(pair,dpair_v)
require(np.linalg.norm(Cpair-2*T*(delta-delta@delta))<2e-14,
        'exact original paired count effect numerical replay')
alpha=float(np.linalg.eigvalsh(Cpair).max())
require(alpha<P*P and alpha<.03,'actual paired map obeys global p squared and tighter fixture contraction')

def two_weight_entropy(a,b):
    total=a+b
    if not total: return 0.
    return sum(-x*np.log(x/total) for x in (a,b) if x)
def match_coefficient(n): return two_weight_entropy(P**(n+2),P**(2*n-2))
def abort_coefficient(n): return two_weight_entropy(P**(n+1),P**(2*n-1))
Hbit=-(P*P*np.log(P*P)+P*np.log(P))
require(abs(Hbit/ELL-(2-P))<1e-14,'unchanged Golden paired-bit entropy unit')

def lost_effect(cap,dps):
    power=I.copy();dpower=ZERO.copy();value=ZERO.copy();source=ZERO.copy()
    for n in range(1,cap+1):
        dpower=backward_jet(pair,dps,power,dpower)
        power=backward(pair,power)
        if n>=2:
            coefficient=match_coefficient(n)+(abort_coefficient(n) if n==cap else 0.)
            value+=coefficient*power;source+=coefficient*dpower
    return herm(value),herm(source)

def paired_count_effect(cap,dk):
    cp,dcp=effect(pair,np.array([dk[2*j]/P for j in pair_rows]))
    total=cp.copy();dtotal=dcp.copy()
    for anchor in (0,1):
        hit=k[anchor::2];dhit=dk[anchor::2]
        killed=k[1-anchor::2];dkilled=dk[1-anchor::2]
        power=cp.copy();dpower=dcp.copy();summed=ZERO.copy();dsummed=ZERO.copy()
        for n in range(cap-1):
            summed+=power;dsummed+=dpower
            dpower=backward_jet(killed,dkilled,power,dpower)
            power=backward(killed,power)
        total+=backward(hit,summed)
        dtotal+=backward_jet(hit,dhit,summed,dsummed)
    return herm(total),herm(dtotal)

def source_summary(cap,dk,dps,dr):
    D,dD=lost_effect(cap,dps)
    N,dN=paired_count_effect(cap,dk)
    A=(2-P)*N-D/ELL;dA=(2-P)*dN-dD/ELL
    eta_bound=2*np.sqrt(alpha*np.linalg.eigvalsh(herm(sum((adj(a)@a for a in dps),ZERO.copy()))).max())
    return {'total_tick_cap':cap,'lost_port_entropy':trace(D@rho),
            'lost_port_entropy_field_source_fixed_input':trace(dD@rho),
            'lost_port_entropy_preparation_source':trace(D@dr),
            'lost_port_entropy_total_source':trace(dD@rho+D@dr),
            'lost_information_effect_eigenvalue_bounds':np.linalg.eigvalsh(D)[[0,-1]].tolist(),
            'retained_anchor_lost_port_entropy':0.0,
            'expected_paired_events':trace(N@rho),
            'paired_count_total_source':trace(dN@rho+N@dr),
            'row_status_compensation':trace(A@rho),
            'row_status_compensation_total_source':trace(dA@rho+A@dr),
            'retained_anchor_compensation':(2-P)*trace(N@rho),
            'retained_anchor_compensation_source':(2-P)*trace(dN@rho+N@dr),
            'data_input_derivative_trace_norm':float(np.abs(np.linalg.eigvalsh(herm(dr))).sum()),
            'field_map_amplified_safe_Stinespring_norm_upper_bound':float(eta_bound)}

def entropy_spectral(lam,dlam,weight,eta=1e-24):
    if weight==0: return 0.,0.
    x=weight*lam;dx=weight*dlam
    logs=np.log(x+eta)
    return float(-np.sum(x*logs)),float(-np.sum(dx*(logs+x/(x+eta))))

def direct_cap3():
    """Every actual stopped fine PORT word, grouped only to reuse its SVD.

    A fine word's true amplitude is sqrt(product q_b)*M_word*sqrt(rho).
    Both costs and all singular modes are evaluated for each positive fine
    leaf, including cap aborts. This is not a pointer entropy substitution.
    """
    ms=[k[0],k[1],*pair];dms=[kv[0],kv[1],*dpair_v]
    weights=[(1.,0.),(0.,1.)]+[(P*P,P)]*len(pair)
    eff=[1.,2.]+[P**3]*len(pair)
    sqrt=native['root'](rho);dsqrt=solve_sylvester(sqrt,sqrt,drho_v)
    fine=merged=dfine=dmerged=0.;cost=dcost=net=dnet=0.
    mass=dmass=paircount=dpaircount=0.;comp=dcomp=0.
    normal=ZERO.copy();dnormal=ZERO.copy();direct_D=ZERO.copy();direct_dD=ZERO.copy()
    fine_leaves=merged_leaves=base_words=0
    for n in (2,3):
        for word in itertools.product(range(len(ms)),repeat=n):
            # Real first-return language: match at tick2, or one mismatch
            # followed at tick3 by match / capped abort. No extra words.
            statuses=('match',) if n==2 else ('match','abort')
            specs=[]
            for status in statuses:
                choices=[]
                for anchor in (0,1):
                    bits=(anchor,anchor) if n==2 else (anchor,1-anchor,anchor if status=='match' else 1-anchor)
                    q=float(np.prod([weights[label][bit] for label,bit in zip(word,bits)]))
                    if q: choices.append((q,n+sum(bits)))
                if choices: specs.append((status,choices))
            if not specs: continue
            W=I.copy();dW=ZERO.copy()
            for label in word:
                dW=dms[label]@W+ms[label]@dW;W=ms[label]@W
            amp=W@sqrt;damp=dW@sqrt+W@dsqrt
            U,singular,Vh=np.linalg.svd(amp,full_matrices=False)
            lam=singular*singular
            dlam=2*singular*np.diag(adj(U)@damp@adj(Vh)).real
            qbase=float(lam.sum());dqbase=float(dlam.sum())
            gram=adj(W)@W;dgram=adj(dW)@W+adj(W)@dW
            ceff=sum(eff[label] for label in word);npair=sum(label>=2 for label in word)
            base_words+=1
            for status,choices in specs:
                a=sum(q for q,c in choices)
                coarse_s,coarse_ds=entropy_spectral(lam,dlam,a)
                merged+=coarse_s;dmerged+=coarse_ds
                mass+=a*qbase;dmass+=a*dqbase
                costfactor=sum(q*c for q,c in choices)
                cost+=costfactor*qbase;dcost+=costfactor*dqbase
                net+=a*ceff*qbase;dnet+=a*ceff*dqbase
                paircount+=a*npair*qbase;dpaircount+=a*npair*dqbase
                compfactor=-a*np.log(a)/ELL
                comp+=compfactor*qbase;dcomp+=compfactor*dqbase
                hfactor=-sum(q*np.log(q/a) for q,c in choices)
                direct_D+=hfactor*gram;direct_dD+=hfactor*dgram
                martingale=costfactor+sum(q*np.log(q) for q,c in choices)/ELL-a*ceff
                normal+=martingale*gram;dnormal+=martingale*dgram
                for q,c in choices:
                    fs,fds=entropy_spectral(lam,dlam,q)
                    fine+=fs;dfine+=fds;fine_leaves+=1
                merged_leaves+=1
    D,dD=lost_effect(3,dpair_v)
    N,dN=paired_count_effect(3,kv)
    value=fine-merged;source=dfine-dmerged
    require(abs(mass-1)<3e-12 and abs(dmass)<3e-12,'actual complete cap3 stopped mass and field source')
    require(fine_leaves==133120,'all 133120 live original fine stopped leaves evaluated')
    require(np.linalg.norm(direct_D-D)<2e-13 and np.linalg.norm(direct_dD-dD)<2e-12,
            'direct all-leaf conditional entropy effect and complete field jet equal one-map polynomial')
    require(abs(value-trace(D@rho))<3e-12 and abs(source-trace(dD@rho+D@drho_v))<3e-11,
            'actual complete mixed-CQ entropy difference and source equal exact refinement effect')
    require(abs(paircount-trace(N@rho))<3e-12 and abs(dpaircount-trace(dN@rho+N@drho_v))<3e-11,
            'actual stopped paired count and preparation source equal killed-map occupation')
    require(np.linalg.norm(normal)<3e-12 and np.linalg.norm(dnormal)<3e-11,
            'full ambient optional-bit martingale operator and field jet vanish')
    require(abs(cost-fine/ELL-(net+comp-merged/ELL))<3e-12 and
            abs(dcost-dfine/ELL-(dnet+dcomp-dmerged/ELL))<3e-11,
            'actual stopped port price and full moving source equal compensated p cubed reduction')
    require(abs(comp-((2-P)*paircount-value/ELL))<3e-12 and
            abs(dcomp-((2-P)*dpaircount-source/ELL))<3e-11,
            'controller likelihood and exact all-pair information give same compensation/source')
    return {'total_tick_cap':3,'physical_alphabet':128,'live_fine_leaves':fine_leaves,
            'positive_merged_leaves':merged_leaves,'evaluated_quantum_base_words':base_words,
            'native_comparison_predicate':'PORT bit equality to initial PORT bit; not full128-label equality',
            'merged_interface':'merged row labels plus length and match/abort status, no extra anchor copy',
            'fine_CQ_entropy':fine,'merged_CQ_entropy':merged,
            'fine_CQ_source':dfine,'merged_CQ_source':dmerged,
            'lost_port_entropy':value,'lost_port_entropy_source':source,
            'actual_port_cost':cost,'actual_port_cost_source':dcost,
            'effective_p_cubed_count_cost':net,'effective_p_cubed_count_source':dnet,
            'controller_compensation':comp,'controller_compensation_source':dcomp,
            'ambient_operator_residual':float(np.linalg.norm(normal)),
            'ambient_operator_field_jet_residual':float(np.linalg.norm(dnormal)),
            'information_effect_residual':float(np.linalg.norm(direct_D-D)),
            'information_effect_field_jet_residual':float(np.linalg.norm(direct_dD-dD)),
            'smoothing_eta':1e-24,'all_quantum_singular_modes_retained':True,
            'floating_interval_certificate':False}

directions={}
uncapped_stationary={}
for name,dk,dps,dr in [('r',kr,dpair_r,drho),('v_one_port_null',kv,dpair_v,drho_v)]:
    directions[name]=[source_summary(cap,dk,dps,dr) for cap in (3,15,64)]
    a,b=directions[name][-2:]
    require(abs(a['lost_port_entropy']-b['lost_port_entropy'])<1e-18,
            'native cap15/cap64 loss value agrees below displayed precision '+name)
    require(abs(a['lost_port_entropy_total_source']-b['lost_port_entropy_total_source'])<1e-18,
            'native cap15/cap64 loss source agrees below displayed precision '+name)
    cp,dcp=effect(pair,dps)
    qpair=trace(cp@rho);dqpair=trace(dcp@rho+cp@dr)
    port1=k[1::2];dport1=dk[1::2]
    e1,de1=effect(port1,dport1)
    q1=trace(e1@rho);dq1=trace(de1@rho+e1@dr)
    uncapped_stationary[name]={
        'scope':'owned stationary first-return occupation, not cap64 clock convergence',
        'actual_paired_probability':qpair,'actual_paired_probability_source':dqpair,
        'expected_paired_events':3*qpair,'paired_count_source':3*dqpair,
        'actual_port_cost':3*(1+q1),'actual_port_cost_source':3*dq1,
        'lost_port_information_used':b['lost_port_entropy'],
        'lost_port_information_source_used':b['lost_port_entropy_total_source'],
        'information_error_control':'N64 global analytic C1 tail; does not bound clock/count tail',
        'row_status_compensation':(2-P)*3*qpair-b['lost_port_entropy']/ELL,
        'row_status_compensation_source':(2-P)*3*dqpair-b['lost_port_entropy_total_source']/ELL,
        'retained_anchor_compensation':(2-P)*3*qpair,
        'retained_anchor_compensation_source':(2-P)*3*dqpair}
require(directions['v_one_port_null'][-1]['row_status_compensation_total_source']>0 and
        uncapped_stationary['v_one_port_null']['row_status_compensation_source']<0,
        'native cap64 and actual uncapped clock compensation sources have opposite signs')

# Exact elementary global inequalities: alpha <= p^2 <2/5, r=alpha p<1/4.
pL=F(309,500);pU=F(6181,10000)
require(pL*pL+pL-1<0<pU*pU+pU-1,'exact rational bracket for Golden p')
require(pU*pU<F(2,5) and pU**3<F(1,4),'global pair CP contraction constants')
for cap in (2,3,15,64):
    rbr=F(1,4);abr=F(2,5)
    require(abr+abr*abr/(1-rbr)<1,'global value/preparation-tail coefficient below one')
    require(cap+abr*((cap+1)/(1-rbr)+rbr/(1-rbr)**2)<2*cap+1,
            'global field-tail coefficient below 2N+1 at N='+str(cap))
tail=F(1,2**126)
result={'scope':'original native PORT-sensitive stopped scalar refinement; full input and field-source composition',
        'native_constructor_git_blob':'ee8de4635d24c668949ac9a0186616ab7d59f2ed',
        'fixture':{'r':r,'nu':nu,'h':h,'h_r':hr,'dnu_v':dn,'pair_map_alpha':alpha},
        'directions':directions,
        'uncapped_stationary_occupation_diagnostic':uncapped_stationary,
        'direct_cap3':None if args.skip_direct else direct_cap3(),
        'global_C1_tail':{'cap_convention':'N total native ticks including anchor',
                          'uniform_scope':'all original Delta between 0 and I, any bounded input/field jet',
                          'value_bound_N64':str(tail),
                          'source_bound_N64':'2^-126 * (||D Omega_DATA||_1 + 129 ||DTheta||_(1->1,H))',
                          'correlated_reference_scope':'scalar correction depends only on DATA marginal; Stinespring norm upper bound is also amplified-safe',
                          'requires_probability_floor':False,'requires_stationary_input':False,
                          'is_full_merged_entropy_tail_bound':False},
        'arbitrary_correlated_input_theorem':True,'full_input_normal_is_explicit_effect':True,
        'retained_anchor_interface_lost_information':0,
        'extra_physical_controller_prep_heat_ledgers_waived':False,
        'compulsory_Book03_selected':False,'GR_closed':False,
        'checks_passed':len(checks),'checks':checks,'runtime_seconds':time.monotonic()-started}
encoded=json.dumps(result,indent=2)+'\n'
if args.json: args.json.write_text(encoded)
print(encoded,end='')

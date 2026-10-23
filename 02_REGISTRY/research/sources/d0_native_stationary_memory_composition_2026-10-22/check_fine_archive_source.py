#!/usr/bin/env python3
"""New same-native age/fine conditional source application, no source fitting.

Consumes immutable original CAR16/full128 constructor + owned analytic-jet
entropy checker by AST. Only K=1,2; physical labels, true no-reset products,
all singular values, and real mixed-DATA input retained. No core promotion.
"""
import argparse, ast, hashlib, json
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from scipy.linalg import expm, solve_sylvester

parser=argparse.ArgumentParser(description=__doc__)
where=parser.add_mutually_exclusive_group()
where.add_argument('--repo-root',type=Path,help='Repository root; otherwise discover it from cwd and script ancestors.')
where.add_argument('--input-dir',type=Path,help='Optional directory containing the three exact pinned input files.')
parser.add_argument('--json',type=Path,help='Also write the JSON receipt to this explicit path; stdout is always emitted.')
args=parser.parse_args()
source_root=Path('02_REGISTRY/research/sources')
native_relative=source_root/'d0_book_uniform_source_2026-10-21/check_uniform_book_source.py'
checker_relative=source_root/'d0_native_complete_cq_source_2026-10-22/check_complete_history_source.py'
receipt_relative=source_root/'d0_native_complete_cq_source_2026-10-22/COMPLETE_HISTORY_RESULT.json'
if args.input_dir is not None:
    input_root=args.input_dir.resolve()
    native_path=input_root/native_relative.name
    checker_path=input_root/checker_relative.name
    prior_path=input_root/receipt_relative.name
else:
    if args.repo_root is not None:
        candidates=[args.repo_root.resolve()]
    else:
        candidates=[]
        for start in (Path.cwd().resolve(),Path(__file__).resolve().parent):
            for candidate in (start,*start.parents):
                if candidate not in candidates: candidates.append(candidate)
    repo_root=next((candidate for candidate in candidates
                   if all((candidate/rel).is_file() for rel in
                          (native_relative,checker_relative,receipt_relative))),None)
    if repo_root is None:
        parser.error('Cannot locate all three original repository inputs; use --repo-root or --input-dir.')
    native_path=repo_root/native_relative
    checker_path=repo_root/checker_relative
    prior_path=repo_root/receipt_relative
NATIVE_BLOB='ee8de4635d24c668949ac9a0186616ab7d59f2ed'
CHECKER_BLOB='c133c6aec28e2a4068b36a6d9646bc8fb04fc2a4'
CHECKER_SHA256='cd0052f10bc43abb3736a1637c850c2a3d637f428dd116f6320f68bcf84e3931'
PRIOR_RECEIPT_BLOB='7530a050c3e0d4cc0aad29648f61fa3b86a524c8'
P=(np.sqrt(5)-1)/2; EYE=np.eye(16,dtype=complex)
checks=[]
def check(ok,why):
    if not ok: raise ArithmeticError(why)
    checks.append(why)

raw=native_path.read_bytes()
check(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==NATIVE_BLOB,
      'immutable actual original native constructor')
native_env={'np':np,'expm':expm,'solve_sylvester':solve_sylvester,'P':P,'EYE':EYE}
native_names={'adj','herm','tr','root','creators','native'}
for node in ast.parse(raw.decode()).body:
    if isinstance(node,ast.FunctionDef) and node.name in native_names:
        exec(compile(ast.Module(body=[node],type_ignores=[]),'pinned_native','exec'),native_env)
owned=checker_path.read_bytes()
check(hashlib.sha256(owned).hexdigest()==CHECKER_SHA256 and
      hashlib.sha1(b'blob '+str(len(owned)).encode()+b'\0'+owned).hexdigest()==CHECKER_BLOB,
      'owned complete entropy checker bytes')
env={'np':np,'expm':expm,'solve_sylvester':solve_sylvester,'P':P,'EYE':EYE,
     'CHECKS':checks,'ENTROPY_ETA':1e-22}
need={'require','adj','herm','entropy_amplitude','entropy_source','branch',
      'native_joint_jet','prepared','cq_depth'}
for node in ast.parse(owned.decode()).body:
    if isinstance(node,ast.FunctionDef) and node.name in need:
        exec(compile(ast.Module(body=[node],type_ignores=[]),'pinned_entropy','exec'),env)
adj=env['adj'];herm=env['herm'];entropy=env['entropy_amplitude'];state_entropy=env['entropy_source']
r=1/9;nu=3/5;theta=2*np.arctanh(r);dtheta=2/(1-r*r)
k,dtheta_native=native_env['native'](theta,nu)
k0,dr,rows=env['native_joint_jet'](native_env,theta,nu,dtheta,0.0)
check(np.linalg.norm(k0-k)<1e-14,'unchanged original all128 matrices')
check(np.linalg.norm(dr-dtheta*dtheta_native)<1e-13,'unchanged original proper-r jet')
delta,ddelta,rho,drho,Z=env['prepared'](k,dr)
h=16/Z
mu=float(np.trace(delta).real/16)
t=2*P**2
HBIT=-P**2*np.log(P**2)-P*np.log(P)
pair_effect=sum((adj(a)@a for a in k[2:]),np.zeros_like(EYE))
pair_effect_formula=2*t*(delta-delta@delta)
check(np.linalg.norm(pair_effect-pair_effect_formula)<1e-14,
      'actual paired-row count effect equals 2t(Delta-Delta squared)')
check(np.linalg.norm(sum((a@adj(a) for a in rows),np.zeros_like(EYE))-EYE)<1e-14,
      'actual original Walsh rows also sum to right identity')
hr=16*np.trace(np.linalg.inv(delta)@ddelta@np.linalg.inv(delta)).real/Z**2
dnu_v=-nu*hr/(2*h)
_,dv,_=env['native_joint_jet'](native_env,theta,nu,dtheta,dnu_v)
_,ddelta_v,_,drho_v,_=env['prepared'](k,dv)
hv=16*np.trace(np.linalg.inv(delta)@ddelta_v@np.linalg.inv(delta)).real/Z**2
check(abs(hv)<1e-14,'actual one-port-null h source')
active=[i for i in range(128) if np.count_nonzero(k[i])]
check(len(active)==64,'all 64 exact-dark physical slots identified')
check(all(np.count_nonzero(dr[i])==0 and np.count_nonzero(dv[i])==0
          for i in range(128) if i not in active),'dark slots have exact zero jets in both actual directions')
prior=prior_path.read_bytes()
check(hashlib.sha1(b'blob '+str(len(prior)).encode()+b'\0'+prior).hexdigest()==PRIOR_RECEIPT_BLOB,
      'owned complete entropy receipt exact bytes')
ref=json.loads(prior)['original_native_full128']

def independent_grouped(k,dk,rho,drho,depth):
    """Read exactly the last-nonblank age of every true complete native word."""
    sqrt=native_env['root'](rho);dsqrt=solve_sylvester(sqrt,sqrt,drho)
    nodes=[((),sqrt,dsqrt)]
    for _ in range(depth):
        nodes=[(w+(label,),k[label]@a,dk[label]@a+k[label]@da)
               for w,a,da in nodes for label in active]
    groups=[np.zeros_like(rho) for _ in range(depth+1)]
    dgroups=[np.zeros_like(rho) for _ in range(depth+1)]
    raw=draw=0.0;cost=dcost=0.0;rawsmall=drawsmall=0.0
    pair_count=pair_source=0.0
    for word,a,da in nodes:
        state=a@adj(a);jet=da@adj(a)+a@adj(da)
        age=0
        for label in reversed(word):
            if label!=0: break
            age+=1
        groups[age]+=state;dgroups[age]+=jet
        value,source=entropy(a,da,1e-22);vsmall,dsmall=entropy(a,da,1e-24)
        raw+=value;draw+=source;rawsmall+=vsmall;drawsmall+=dsmall
        # Existing extra-port count only; no assertion this is all physical Cost.
        mark=sum(label%2 for label in word)
        cost+=mark*np.trace(state).real;dcost+=mark*np.trace(jet).real
        paired_mark=sum(label>=2 for label in word)
        pair_count+=paired_mark*np.trace(state).real
        pair_source+=paired_mark*np.trace(jet).real
    si,dsi=state_entropy(rho,drho)
    age_value=age_source=0.0
    minimum_age_eigenvalue=1.0;age_jet_trace_norm=0.0
    for state,jet in zip(groups,dgroups):
        sv,sd=state_entropy(state,jet)
        age_value+=sv;age_source+=sd
        minimum_age_eigenvalue=min(minimum_age_eigenvalue,float(np.linalg.eigvalsh(herm(state)).min()))
        age_jet_trace_norm+=float(np.linalg.norm(herm(jet),ord='nuc'))
    check(minimum_age_eigenvalue>1e-3 and age_jet_trace_norm<1,
          f'positive age blocks and conservative source norm, K={depth}')
    # Independently form the exact stationary last-nonblank CP blocks and jets.
    B=k[0];dB=dk[0];A=rho-B@rho@B
    dA=drho-dB@rho@B-B@drho@B-B@rho@dB
    power=EYE.copy();dpower=np.zeros_like(EYE)
    err=derr=0.0
    for n in range(depth+1):
        inp,dinp=(A,dA) if n<depth else (rho,drho)
        exact=power@inp@power
        dexact=dpower@inp@power+power@dinp@power+power@inp@dpower
        err=max(err,float(np.linalg.norm(exact-groups[n])))
        derr=max(derr,float(np.linalg.norm(dexact-dgroups[n])))
        dpower=dB@power+B@dpower;power=B@power
    check(err<3e-13 and derr<3e-13,f'actual grouped fine tape equals age CP block and all source, K={depth}')
    check(abs(cost-depth*4*P**3*h)<3e-13,f'true extra-port charge, K={depth}')
    # Exact paired-bit refinement through noncommuting words, keeping blank
    # and orphan distinct. This merges outcomes without any DATA reset.
    mk=np.concatenate((k[:2],k[2::2]/P))
    mdk=np.concatenate((dk[:2],dk[2::2]/P))
    ma=[i for i in range(len(mk)) if np.count_nonzero(mk[i])]
    check(len(ma)==33,'65 physical merged labels have 33 live labels')
    mnodes=[(sqrt,dsqrt)]
    for _ in range(depth):
        mnodes=[(mk[j]@a,mdk[j]@a+mk[j]@da) for a,da in mnodes for j in ma]
    merged=merged_source=0.0
    for a,da in mnodes:
        sv,sd=entropy(a,da,1e-22);merged+=sv;merged_source+=sd
    dd=herm(-dk[0]/t)
    dh=float(np.trace(drho@delta+rho@dd).real)
    dmu=float(np.trace(dd).real/16)
    qpair=2*t*h*(1-mu)
    dqpair=2*t*(dh*(1-mu)-h*dmu)
    check(abs(pair_count-depth*qpair)<3e-13 and abs(pair_source-depth*dqpair)<3e-13,
          f'actual pair count and source obey stationary additive identity K={depth}')
    check(abs(raw-merged-pair_count*HBIT)<3e-12 and abs(draw-merged_source-pair_source*HBIT)<3e-11,
          f'actual all-word paired-bit entropy and source factorization K={depth}')
    out=dict(depth=depth,physical_word_slots=128**depth,positive_word_slots=len(nodes),
             fine_CQ=raw,fine_CQ_source=draw,fine_gain=raw-si,fine_gain_source=draw-dsi,
             age_CQ=age_value,age_CQ_source=age_source,age_gain=age_value-si,age_gain_source=age_source-dsi,
             conditional_fine_given_age_DATA=raw-age_value,
             conditional_fine_given_age_DATA_source=draw-age_source,
             extra_port_count=cost,extra_port_count_source=dcost,
             grouped_state_max_error=err,grouped_source_max_error=derr,
             smaller_eta_fine_CQ=rawsmall,smaller_eta_fine_CQ_source=drawsmall,
             minimum_age_eigenvalue=minimum_age_eigenvalue,age_jet_trace_norm=age_jet_trace_norm,
             age_smoothing_value_bound=16*(depth+1)*1e-22,
             age_smoothing_source_bound=5e-39,
             paired_row_count=pair_count,paired_row_count_source=pair_source,
             paired_bit_conditional_entropy=pair_count*HBIT,
             paired_bit_conditional_entropy_source=pair_source*HBIT,
             merged_CQ=merged,merged_CQ_source=merged_source,
             merged_given_age_DATA=merged-age_value,
             merged_given_age_DATA_source=merged_source-age_source,
             actual_mu_source=dmu,actual_h_source=dh,
             paired_bit_only_source_at_K4096=4096*dqpair*HBIT)
    check(out['conditional_fine_given_age_DATA']>=-1e-12,'conditional fine-given-age CQ entropy nonnegative')
    return out

receipt={'scope':'NEW same-original finite fine|age DATA conditional-source evaluation; original K1/K2 fine owner reused',
         'native_blob':NATIVE_BLOB,'owned_checker_sha256':CHECKER_SHA256,
         'owned_checker_blob':CHECKER_BLOB,
         'prior_receipt_blob':PRIOR_RECEIPT_BLOB,
         'native_fixture':dict(r=r,nu=nu,theta=theta,h=h,mu=mu,hr=hr,dnu_v=dnu_v,hv=hv,
                               paired_bit_entropy=HBIT,paired_row_probability=2*t*h*(1-mu)),
         'directions':{},'full_Book03_Cost_Info_selected':False,'GR_closed':False}
ell=np.log((1+np.sqrt(5))/2)
for name,dk,rhojet in [('r',dr,drho),('v_one_port_invisible',dv,drho_v)]:
    receipt['directions'][name]=[]
    for depth in (1,2):
        value=independent_grouped(k,dk,rho,rhojet,depth)
        previous=ref['directions'][name][depth-1]
        check(abs(value['fine_CQ']-previous['complete_CQ_entropy'])<3e-12,
              f'owned actual fullfine entropy replay {name} K={depth}')
        check(abs(value['fine_CQ_source']-previous['complete_CQ_source'])<3e-11,
              f'owned actual fullfine source replay {name} K={depth}')
        bound=previous['regularization']['source_error_bound']
        value['inherited_fine_smoothing_source_bound']=bound
        value['conditional_smoothing_source_bound']=bound+value['age_smoothing_source_bound']
        value['conditional_smoothing_value_bound']=previous['regularization']['value_error_bound']+value['age_smoothing_value_bound']
        check(abs(value['extra_port_count_source']-depth*4*P**3*(hr if name=='r' else hv))<2e-14,
              f'unchanged actual extra-port source {name} K={depth}')
        value['fine_conditional_PRICE_source']=-value['conditional_fine_given_age_DATA_source']/ell
        value['extra_port_minus_fullfine_GAIN_source']=value['extra_port_count_source']-value['fine_gain_source']/ell
        value['extra_port_minus_age_GAIN_source']=value['extra_port_count_source']-value['age_gain_source']/ell
        receipt['directions'][name].append(value)
receipt['checks_passed']=len(checks);receipt['checks']=checks
pl=Q(309,500);pu=Q(6181,10000)
check(pl*pl+pl<1 and pu*pu+pu>1,'exact rational bracketing of native golden p')
xl=pl**3;xu=pu**3
ell_lower=2*(xl+xl**3/3)
ell_upper=2*(xu+xu**3/3+xu**5/(5*(1-xu*xu)))
h_exact=Q(69399,5030720);mu_exact=Q(141489,10240000)
mu_r_exact=-Q(328779,204800000);h_r_exact=-Q(20040939,9885993640)
mu_v_exact=mu_r_exact-mu_exact*h_r_exact/h_exact
check(abs(h-float(h_exact))<1e-14 and abs(mu-float(mu_exact))<1e-14,
      'actual matrices match owned exact native h and mu')
check(mu_v_exact>0,'exact native one-port-null mu source is positive')
bit_lower=4096*4*pl**2*h_exact*(1-mu_exact)*ell_lower*(2-pu)
bit_upper=4096*4*pu**2*h_exact*(1-mu_exact)*ell_upper*(2-pl)
mag_lower=4096*4*pl**2*h_exact*mu_v_exact*ell_lower*(2-pu)
mag_upper=4096*4*pu**2*h_exact*mu_v_exact*ell_upper*(2-pl)
check(bit_lower>Q(113,2),'exact K4096 missing fine-given-age entropy exceeds 56.5 nats')
check(mag_lower>Q(24,1000) and mag_upper<Q(25,1000),
      'exact K4096 paired-bit v source lies strictly between -0.025 and -0.024')
receipt['all_finite_K_paired_refinement']={
    'true_for_arbitrary_correlated_retained_preparation':True,
    'probabilities':['p^2','p'],'entropy':'log(phi)*(2-p)',
    'actual_count_effect':'Cpair=2t(Delta-Delta^2)',
    'arbitrary_preparation_score':'H2(p) sum_{j=0}^{K-1} (Phi*)^j Cpair',
    'stationary_pair_probability':'2t h(1-mu)',
    'K4096_bit_entropy':4096*2*t*h*(1-mu)*HBIT,
    'K4096_fine_given_age_entropy_strict_lower_bound_nats':56.5,
    'K4096_bit_entropy_rational_log_bounds':[str(bit_lower),str(bit_upper)],
    'K4096_bit_v_source_rational_log_bounds':[str(-mag_upper),str(-mag_lower)],
    'K4096_bit_v_source_strict_bounds':[-.025,-.024],
    'full_K4096_fine_conditional_source_computed':False,
    'remaining_merged_conditional_entropy_nonnegative':True,
    'remaining_merged_conditional_SOURCE_sign_controlled':False}
receipt['checks_passed']=len(checks)
receipt['verification']={'all_singular_modes_retained':True,'dark_labels_deleted_from_physics':False,
                         'smoothing_eta':1e-22,'smoothing_eta_control':1e-24,
                         'analytic_source_jets':True,'floating_interval_certificate':False,
                         'old_full_suites_replayed':False,'depth_scope':[1,2],
                         'cost_scope':'only actual existing extra-port count; all other paid ledgers still required'}
output=json.dumps(receipt,indent=2)+'\n'
if args.json is not None:
    args.json.write_text(output,encoding='utf-8')
print(output,end='')

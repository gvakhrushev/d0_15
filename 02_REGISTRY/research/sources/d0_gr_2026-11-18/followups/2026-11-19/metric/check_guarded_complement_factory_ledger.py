"""Finite four marked Toffoli success/abort ledger for guarded complemented word.

Consumes the actual logical circuit replay and previously certified physical
Toffoli instrument; this is not a simulation of every expanded microscopic
receipt, one compiled halt controller, the full Book03 price, or full clock.
"""
import json, math, subprocess, sys
from pathlib import Path
import numpy as np
import mpmath as mp
import sympy as sp
from check_source_price import need


def replay(name):
    path=Path(__file__).with_name(name)
    return json.loads(subprocess.check_output([sys.executable,'-B','-W','error',str(path)],text=True))


def main():
    # These are the actual published guarded word and the owner of every
    # explicit Toffoli success/failure isometry. Recheck both before composing.
    guarded=replay('check_guarded_complement_full_branch.py')
    factory=replay('check_factory_routing_cost.py')
    need(factory['all_four_teleport_sign_pairs_equal_exact_negative_Fredkin']==4,
         'actual factory success and sign corrections, all eight inputs')
    need(factory['abort_after_CZ_can_dephase_reduced_data_if_resource_traced'],
         'real first-failure environment cannot be reset')
    need(guarded['literal_gate_inventory_excluding_four_Toffoli_factories']['ideal_Toffoli']==4,
         'actual guarded target contains four marked Toffoli')
    x,y=sp.symbols('b2 b3',real=True)
    ff=[1-x,x*(1-x),x**2*(1-x),x**3*(1-x),
        x**4*(1-y),x**4*y*(1-x),x**5*y*(1-x)]
    beta=x**6*y
    need(sp.expand(sum(ff)+beta-1)==0,'all seven genuine first aborts and one success')
    r=sp.symbols('br',real=True)
    total=(1-r)+r*sum(beta**j*sum(ff) for j in range(4))+r*beta**4
    need(sp.expand(total-1)==0,'all 28 first-failure classes plus r failure and success')
    # A physically correct full-record isometry may entangle abort data with
    # retained factory resource. Verify the owner's CZ(|+>|+>) example.
    v=np.array([1.,1.])/math.sqrt(2);cz=np.diag([1.,1.,1.,-1.])
    ent=cz@np.kron(v,v);psi=ent.reshape(2,2);red=psi@psi.T
    need(np.max(abs(red-np.eye(2)/2))<1e-15,'tracing failed resource dephases input')
    mp.mp.dps=120;p=(mp.sqrt(5)-1)/2;a=mp.sqrt(p);ell=mp.log(1/p)
    s2=4*p**3;s3=16*p**9;theta=mp.atan2(p,a)
    H=lambda a:-sum(x*mp.log(x)/ell for x in a if x)
    f=lambda x:1+x-H((x,1-x))
    fX=2+s2-H((1-s2,s2/2,s2/2)); rows=[]
    for data in guarded['checks']:
        q=int(data['q']);turn=int(data['turn']);t=q*theta-2*mp.pi*turn
        d=abs(2*a*p*mp.sin(2*t));need(d>0 and d<1,'actual field secant')
        # Three explicit geometric-tail budgets, all positive retained aborts.
        L1=int(mp.ceil(mp.log(3/d**4)/mp.log(1/p)))
        L2=int(mp.ceil(mp.log(72/d**4)/(6*mp.log(1/p))))
        L3=int(mp.ceil(mp.log(12/d**4)/(-mp.log(1-s3))))
        br=1-p**L1;b2=1-p**(6*L2);b3=1-(1-s3)**L3;bt=b2**6*b3
        gamma=br*bt**4;epsilon=1-gamma
        fnums=[1-b2,b2*(1-b2),b2**2*(1-b2),b2**3*(1-b2),
               b2**4*(1-b3),b2**4*b3*(1-b2),b2**5*b3*(1-b2)]
        failclasses=[br*bt**j*f for j in range(4) for f in fnums]
        need(all(v>0 for v in failclasses),'none of physical first failures silently removed')
        need(abs(p**L1+sum(failclasses)+gamma-1)<mp.mpf('1e-110'),'total actual retained mass')
        bound=p**L1+24*p**(6*L2)+4*(1-s3)**L3
        need(epsilon<=bound and bound<=d**4,'explicit physical caps imply eps <= |delta q|^4')
        err=epsilon/(gamma*d)
        # The two actual h-branch operators from the compiled logical word.
        delta=2*a*p*mp.sin(2*t)
        success_signal=gamma*p**2*delta
        success_failure_dummy=-gamma*p*delta
        need(abs(success_failure_dummy/success_signal+1/p)<mp.mpf('1e-110'),
             'h=0 physical dummy signal is not a rare Toffoli failure')
        observed=float(data['h0_dummy_report_delta'])
        need(abs(observed-float(-p*delta))<1e-11,'literal guarded NC1/dummy replay agrees')
        # Conditional 0/10 record ledger of actual factory, not Book03 Info.
        n2=b2/s2;n3=b3/s3;Cplus=n2*fX;CH=n2*f(s2)+b2*n2*fX
        CT=(1+b2)*Cplus+b2**2*CH+b2**4*n3*f(s3)+b2**4*b3*CH
        factory_CQ=br*CT*sum(bt**j for j in range(4))
        need(abs(f(p**2))<mp.mpf('1e-100'),'one golden known-one record code minus CQ')
        rows.append({'q':q,'turn':turn,'abs_delta_q':mp.nstr(d,25),
          'known_one_cap':L1,'X_or_CZ_cap':L2,'CCZ_cap':L3,
          'r_and_all_four_physical_Toffoli_success_probability':mp.nstr(gamma,25),
          'any_separate_r_or_Toffoli_failure_probability':mp.nstr(epsilon,25),
          'certified_failure_union_bound':mp.nstr(bound,25),
          'failure_effect_secant_error_per_factory_gain':mp.nstr(err,25),
          'conditional_record_code_minus_CQ_of_four_factories':mp.nstr(factory_CQ,25),
          'success_h1H1_delta':mp.nstr(success_signal,25),
          'success_h0_dummy_test_delta':mp.nstr(success_failure_dummy,25),
          'dummy_to_success_signal_ratio':mp.nstr(-1/p,25)})
    print(json.dumps({'status':'PASS: physical-factory CP interface and retained finite first-failure ledger',
      'actual_guarded_logical_columns_replayed':True,'actual_first_Toffoli_physical_signs_and_failure_slices_replayed':True,
      'marked_Toffoli_count':4,'first_failure_types_per_Toffoli':7,'first_abort_classes_total':28,
      'factory_failure_env_may_entangle_data':True,
      'raw_full_physical_factory_expanded_clock_compiled':False,
      'independent_known_one_r_first_success_controller_compiled':False,
      'all_physical_fine_microscopic_Kraus_replayed':False,
      'true_Book03_Cost_and_Info_selected':False,
      'GR_closed':False,'finite_cases':rows},indent=2))

if __name__=='__main__':main()

"""Same-spectrum Golden work marks on the verified guarded LIVE carrier.

The priced histories are two conditional CW1/CQ models, not selected D0.
"""
import json,os,subprocess,sys
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent

def need(v,msg):
    if not v:raise RuntimeError(msg)

def main():
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1')
    proc=subprocess.run([sys.executable,'-B',str(HERE/'check_guarded_live_composition.py')],
        capture_output=True,text=True,env=env,check=True,timeout=120)
    result=json.loads(proc.stdout)
    frozen=json.loads((HERE/'guarded_live_composition_result.json').read_text())
    need(result==frozen and result['status']=='PASS','replay all 32 columns and intermediate effect')
    need(result['old_input_columns']==32 and result['first_route_work_mark_max_error']<1e-12,
         'same full protected input and actual intermediate CX')
    p=(sp.sqrt(5)-1)/2;r=sp.simplify(p**2);phi=1+p
    pi=sp.symbols('pi',real=True)
    expect=sp.simplify(p*pi+p**4)
    # Actual local mark acts after the last CX of the first CSWAP0. Its
    # 2-wire extension has identical positive spectrum on both labels.
    P1=sp.diag(0,1);P0=sp.eye(2)-P1
    Kplus=sp.eye(2)+p*P1;Kminus=sp.eye(2)+p*P0
    need(sp.simplify(Kplus.trace()-Kminus.trace())==0,'same trace')
    need(sp.simplify(Kplus.det()-Kminus.det())==0,'same determinant')
    X=sp.Matrix([[0,1],[1,0]])
    need(sp.simplify(X*Kplus*X-Kminus)==sp.zeros(2),'same spectrum by conjugation')
    need(sp.simplify(phi-(1/p))==0,'only Golden quantities used')
    # K=I on every one of 673 logical stages (including nine births),
    # replace the one fixed CX-stage mark by Kplus or Kminus.
    Pvisible=r*(4+pi)
    Wplus=sp.Integer(673)+p*expect
    Wminus=sp.Integer(673)+p*(1-expect)
    Splus=sp.simplify(Pvisible+Wplus)
    Sminus=sp.simplify(Pvisible+Wminus)
    dplus=sp.simplify(sp.diff(Splus,pi));dminus=sp.simplify(sp.diff(Sminus,pi))
    need(sp.simplify(dplus-2*r)==0 and dminus==0,'identical spectrum, different selected source')
    unit_cost_source=sp.simplify(sp.diff(Pvisible+sp.Integer(673),pi))
    need(sp.simplify(unit_cost_source-r)==0,'unit-step ledger leaves registered p² source')
    # Unique zero among the model family λ>=0, if (and only if) the graph
    # fixed-program row has zero derivative and no other price terms exist.
    lam=sp.symbols('lambda',nonnegative=True)
    eqminus=sp.solve(sp.Eq(r-lam*p,0),lam)
    need(len(eqminus)==1 and sp.simplify(eqminus[0]-p)==0,'unique lambda p')
    # Nine births before 664 square gates, 5-bit old input, 14-bit work.
    stages=int(result['logical_total_stages']);births=int(result['live_births'])
    need(stages==673 and births==9,'verified source program inventory')
    D=sum(1<<k for k in range(5,14))+(stages-births)*(1<<14)
    need(D==10895328,'fixed ideal growing-clock dimension')
    print(json.dumps({'status':'PASS','GR_closed':False,
      'native_source_sha256':result['source_sha256'],
      'parent_guarded_live_all_32_columns_replayed':True,
      'logical_clock_dimension_if_all_nine_births_first':D,
      'two_degree_modes':425*D,
      'stage_mark_eigenvalues':['1','phi'],
      'stage_marks_have_equal_trace_and_spectrum':True,
      'mark_plus_mean':'1+p*(p*pi+p^4)',
      'mark_minus_mean':'1+p*(1-p*pi-p^4)',
      'declared_guarded_CQ_code_source':'p^2*Dpi',
      'unit_step_ledger_extra_source_required_for_zero_graph_row':'-p^2*Dpi',
      'plus_model_total_source':'2*p^2*Dpi',
      'minus_model_total_source':'0',
      'fixed_ideal_clock_graph_source_wrt_input_pi':'0',
      'only_with_exact_graph_binding_minus_model_passes_this_row':True,
      'actual_D0_tariff_selected':False,
      'actual_full_terminal_factory_and_failure_clock_constructed':False,
      'physical_source_bridge_and_perturbative_bound_proved':False},indent=2,ensure_ascii=False))

if __name__=='__main__':main()

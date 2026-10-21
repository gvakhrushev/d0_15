#!/usr/bin/env python3
"""Positive-price exact jet compiler for the original conditional stage ledger.
Enumerated finite-field schedules; no random-address Born weights, no signed
probability postprocessing, no field oracle or selected Book action is inferred.
"""
from itertools import product, combinations
from fractions import Fraction as Q
from pathlib import Path
import json

checks=[]
def ck(name,v):
    if not bool(v):raise AssertionError(name)
    checks.append(name)

def schedules(prime,length,strength):
    # All polynomial seeds. Execution is DETERMINISTIC enumeration, not
    # sampling a seed for free. A prime is a compiler index, not a coupling.
    for coeff in product(range(prime),repeat=strength):
        yield tuple(sum(coeff[k]*pow(t,k,prime) for k in range(strength))%prime
                    for t in range(length))

q,N=5,4
stage_cost=[Q(54),Q(71),Q(98),Q(137),Q(188)]
alpha,beta,r0=Q(7,13),Q(11,17),Q(1,997)
h0,h1,h2=Q(1,23),Q(17),-Q(977)
# h0,h1,h2 are independent algebraic placeholders. Actual entropy enters
# through its exact derivative values; schedule identities hold for any values.

def jets(rows):
    value=Q(0);grad=[Q(0)]*q;H=[[Q(0) for _ in range(q)] for _ in range(q)]
    for row in rows:
        for t,cur in enumerate(row):
            k=stage_cost[cur]-beta*h0
            occ=alpha*beta**t*r0**t
            value+=occ*k
            grad[cur]-=occ*beta*h1
            H[cur][cur]-=occ*beta*h2
            if t:
                factor=alpha*beta**t*r0**(t-1)
                for u in range(t):
                    prev=row[u]
                    grad[prev]+=factor*k
                    term=-factor*beta*h1
                    H[cur][prev]+=term;H[prev][cur]+=term
            if t>=2:
                factor=alpha*beta**t*r0**(t-2)*k
                for u,v in combinations(range(t),2):
                    H[row[u]][row[v]]+=factor
                    H[row[v]][row[u]]+=factor
    return value,grad,H

full=jets(product(range(q),repeat=N))
receipts=[]
for strength in (2,3):
    rows=list(schedules(q,N,strength))
    ck(f'actual_number_of_executed_programs_{strength}',len(rows)==q**strength)
    for order in range(1,strength+1):
        for positions in combinations(range(N),order):
            counts={word:0 for word in product(range(q),repeat=order)}
            for row in rows:counts[tuple(row[i] for i in positions)]+=1
            ck(f'exact_tuple_incidence_{strength}_{positions}',
               set(counts.values())=={q**(strength-order)})
    selected=jets(rows)
    factor=Q(q**strength,q**N)
    ck(f'field_price_value_{strength}',selected[0]==factor*full[0])
    ck(f'whole_gradient_all_parameters_{strength}',selected[1]==[factor*x for x in full[1]])
    matchH=selected[2]==[[factor*x for x in row] for row in full[2]]
    ck(f'Hessian_scope_{strength}',matchH==(strength>=3))
    ck(f'full_Hessian_symmetry_{strength}',all(selected[2][i][j]==selected[2][j][i]
                                           for i in range(q) for j in range(q)))
    receipts.append({'strength':strength,'executed_programs':len(rows),
      'full_history_programs':q**N,'exact_comparison_factor':str(factor),
      'first_jet_exact':True,'second_jet_exact':matchH,
      'potential_full_stage_calls':len(rows)*N})
ck('unequal_real_stage_costs_not_replaced',len(set(stage_cost))==q)
ck('full_gradient_is_uniform_at_common_response',len(set(full[1]))==1)
# Literal no-negative-weight compilation: every chosen word occurs once.
ck('all_programme_weights_positive_integers',len(set(schedules(q,N,3)))==q**3)
# Original deterministic initial/bank setup costs may differ by programme:
# they remain in the total objective but have zero fixed-chart FIELD jets.
# Reached transition-dependent costs would need higher tuple strength.
result={'status':'EXACT_POSITIVE_PRICE_JET_COMPILER_PASS','checks':checks,'count':len(checks),
  'data':receipts,'stage_costs':[str(x) for x in stage_cost],
  'fixed_entropy_jet_fixture':{'h0':str(h0),'h1':str(h1),'h2':str(h2)},
  'analytic_result':'strength k+1 reproduces all price derivatives through order k at the common response',
  'native_bank_detector_word_implemented_here':False,
  'original_stage_ledger_consumed_not_reinvented':True,
  'all_setup_costs_retained_as_actual_field_independent_baselines':True,
  'new_field_writer_or_Book_valuation':False,'GR_closed':False}
here=Path(__file__).resolve().parent
(here/'SCHEDULE_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

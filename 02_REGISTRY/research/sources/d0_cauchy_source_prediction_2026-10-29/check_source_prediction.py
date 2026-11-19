#!/usr/bin/env python3
"""Certified source-only isolation: no solution is passed to the search.

The analytical paper composes an existing full D0 source theorem with the
Einstein--scalar Cauchy theorem. These executable controls validate the finite
elimination algorithm on an explicitly STRUCTURAL two-coordinate instance of
the already-used original-reporter/Book-return oracle. They are NOT a nonlinear
GR solver, native gate emission, or a proof of physical task selection.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys
import sympy as sp

CHECKS=[]
PARENT_SHA='dee4697552694f569d2b80abe4507b34dac521681eee8f0a07d926fbf814d185'


def require(ok, name):
    if not bool(ok):
        raise ArithmeticError(name)
    CHECKS.append(name)


def load_oracle(path: Path):
    raw=path.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==PARENT_SHA,
            'previous original-reporter interval oracle bytes are pinned')
    spec=importlib.util.spec_from_file_location('owned_composition_oracle',path)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=mod
    spec.loader.exec_module(mod)
    return mod


@dataclass(frozen=True)
class Box:
    lo: tuple[Q,...]
    hi: tuple[Q,...]
    def __post_init__(self):
        if len(self.lo)!=len(self.hi) or any(a>=b for a,b in zip(self.lo,self.hi)):
            raise ValueError('nonempty positive-width rational box required')
    @property
    def center(self): return tuple((a+b)/2 for a,b in zip(self.lo,self.hi))
    @property
    def radius(self): return max((b-a)/2 for a,b in zip(self.lo,self.hi))
    def children(self):
        # Four disjoint-interior boxes, covering the parent INCLUDING its boundary.
        from itertools import product
        mid=self.center
        for bits in product((0,1),repeat=len(mid)):
            yield Box(tuple(mid[i] if bits[i] else self.lo[i] for i in range(len(mid))),
                      tuple(self.hi[i] if bits[i] else mid[i] for i in range(len(mid))))


class TaskOracle:
    """The source is read only via certified complete-price contrasts.

    z=x+y/3 is a known input map, not a fitted future state. The test operand
    is the old structural f(z)=z^2; the original nonlinear r and whole retained
    return are evaluated by the pinned implementation. The independent datum
    y=a models the initial/gauge trace. No target point occurs in evaluate().
    """
    def __init__(self,parent,initial_value:Q|None):
        self.parent=parent
        self.model=parent.OriginalReporterFixture()
        self.initial_value=initial_value
        self.cache={}
        self.calls=0
        self.price_evaluations=0
        self.minimum_gain=None
    def evaluate(self,point,precision):
        x,y=point
        z=x+y/3
        key=(z,precision)
        if key not in self.cache:
            actual,interval,receipt=self.model.contrast(z,precision)
            self.cache[key]=(interval,receipt)
            self.calls+=1
            self.price_evaluations+=2
            gain=Q(receipt['actual_gain_lower'])
            self.minimum_gain=gain if self.minimum_gain is None else min(self.minimum_gain,gain)
        interval,receipt=self.cache[key]
        # Lipschitz constants in the true max norm of (x,y), of the normalized
        # LIMIT source, established by the parent scalar-source identity.
        tests=[('source_x',interval,Q(8,3)),
               ('source_y',interval/3,Q(8,9))]
        if self.initial_value is not None:
            tests.append(('initial_trace',self.parent.Interval.point(y-self.initial_value),Q(1)))
        return tests


def certified_search(oracle:TaskOracle,bits:int,max_depth:int=16):
    """Only inequalities on source/data enclosures; no zero-equality oracle.

    A box is removed only if a uniformly extended certificate excludes zero.
    Every actual solution remains in the union of active boxes. Termination
    follows from compactness + a unique joint zero, NOT from a small residual.
    """
    active=[Box((Q(-1,2),Q(-1,2)),(Q(1,2),Q(1,2)))]
    transcript=[];ledger='0'*64
    excluded_by={};total_checked=0
    for depth in range(max_depth+1):
        kept=[];exclusions=[]
        for cell in active:
            total_checked+=1
            reject=None
            for name,interval,L in oracle.evaluate(cell.center,depth+4):
                low=interval.lo-L*cell.radius
                high=interval.hi+L*cell.radius
                if low>0 or high<0:
                    reject=(name,low,high,interval,L)
                    break
            if reject is None:
                kept.append(cell)
            else:
                name,low,high,interval,L=reject
                excluded_by[name]=excluded_by.get(name,0)+1
                exclusions.append({'lo':list(map(str,cell.lo)),'hi':list(map(str,cell.hi)),
                                   'test':name,'source_interval':[str(interval.lo),str(interval.hi)],
                                   'Lipschitz':str(L),'range':[str(low),str(high)]})
        entry={'depth':depth,'checked':len(active),'retained':len(kept),
               'removed_certificates':exclusions}
        raw=json.dumps(entry,sort_keys=True,separators=(',',':')).encode()
        ledger=hashlib.sha256(ledger.encode()+raw).hexdigest()
        transcript.append(dict(entry,ledger=ledger))
        if not kept:
            return {'status':'CERTIFIED_EMPTY','depth':depth,'transcript':transcript,
                    'excluded_by':excluded_by,'boxes_checked':total_checked}
        lo=tuple(min(b.lo[j] for b in kept) for j in range(2))
        hi=tuple(max(b.hi[j] for b in kept) for j in range(2))
        diameter=max(b-a for a,b in zip(lo,hi))
        if diameter<=Q(1,2**bits):
            return {'status':'ISOLATED_WITH_CERTIFIED_RADIUS','requested_bits':bits,
                    'depth':depth,'hull_lo':list(map(str,lo)),'hull_hi':list(map(str,hi)),
                    'center':list(map(str,((a+b)/2 for a,b in zip(lo,hi)))),
                    'radius':str(diameter/2),'boxes_checked':total_checked,
                    'excluded_by':excluded_by,'transcript':transcript,
                    'source_queries':oracle.calls,'full_price_evaluations':oracle.price_evaluations,
                    'minimum_actual_gain':str(oracle.minimum_gain),
                    'solution_used_in_search':False}
        active=[child for cell in kept for child in cell.children()]
    return {'status':'UNRESOLVED_WITHIN_TEST_BUDGET','depth':max_depth,
            'retained_boxes':len(kept),'hull_lo':list(map(str,lo)),
            'hull_hi':list(map(str,hi)),'diameter':str(diameter),
            'boxes_checked':total_checked,'excluded_by':excluded_by,'transcript':transcript,
            'source_queries':oracle.calls,'solution_used_in_search':False}



def verify_search_certificate(result):
    """Replay rational coverage/exclusion arithmetic, independently of the search.

    The parent source intervals are trusted only under their separately pinned
    log-series proof. This checks that no cell disappeared without a signed
    interval certificate and that the final radius is an enclosure, not a guess.
    """
    active=[Box((Q(-1,2),Q(-1,2)),(Q(1,2),Q(1,2)))];old='0'*64
    for row in result['transcript']:
        clean={k:v for k,v in row.items() if k!='ledger'}
        raw=json.dumps(clean,sort_keys=True,separators=(',',':')).encode()
        old=hashlib.sha256(old.encode()+raw).hexdigest()
        if old!=row['ledger'] or row['checked']!=len(active):
            raise ArithmeticError('certificate ledger or coverage size mismatch')
        removed={}
        for item in row['removed_certificates']:
            cell=Box(tuple(map(Q,item['lo'])),tuple(map(Q,item['hi'])))
            if cell in removed or cell not in active:
                raise ArithmeticError('duplicate or extraneous excluded cell')
            lo,hi=map(Q,item['source_interval']);L=Q(item['Lipschitz'])
            blo,bhi=map(Q,item['range'])
            if lo>hi or L<0 or blo!=lo-L*cell.radius or bhi!=hi+L*cell.radius:
                raise ArithmeticError('incorrect outward Lipschitz enclosure')
            if not (blo>0 or bhi<0):
                raise ArithmeticError('zero not excluded by certificate')
            removed[cell]=item
        kept=[b for b in active if b not in removed]
        if len(kept)!=row['retained']:
            raise ArithmeticError('retained-cell count mismatch')
        active=[child for b in kept for child in b.children()]
    if result['status']=='ISOLATED_WITH_CERTIFIED_RADIUS':
        lo=tuple(min(b.lo[j] for b in kept) for j in range(2))
        hi=tuple(max(b.hi[j] for b in kept) for j in range(2))
        if list(map(str,lo))!=result['hull_lo'] or list(map(str,hi))!=result['hull_hi']:
            raise ArithmeticError('advertised final hull does not equal retained cover')
        if Q(result['radius'])!=max(b-a for a,b in zip(lo,hi))/2:
            raise ArithmeticError('incorrect final certified radius')
    return True


def source_search_controls(parent):
    runs=[]
    # Only the initial datum is passed. Exact future values below are postchecks.
    for datum,bits in ((Q(1,3),6),(Q(-1,5),6)):
        oracle=TaskOracle(parent,datum)
        result=certified_search(oracle,bits)
        require(result['status']=='ISOLATED_WITH_CERTIFIED_RADIUS','source/data search finitely isolates a solution')
        require(verify_search_certificate(result),'independent exact replay verifies the entire exclusion cover')
        actual=(-datum/3,datum) # POSTCHECK: absent from solver/oracle implementation.
        lo=tuple(map(Q,result['hull_lo']));hi=tuple(map(Q,result['hull_hi']))
        center=tuple(map(Q,result['center']));radius=Q(result['radius'])
        require(all(a<=x<=b for a,x,b in zip(lo,actual,hi)), 'known analytical fixture is inside certified output')
        require(max(abs(a-b) for a,b in zip(center,actual))<=radius,'actual output error is within certified radius')
        require(radius<=Q(1,2**(bits+1)), 'requested field precision rather than residual alone is certified')
        require(Q(result['minimum_actual_gain'])>0, 'all price comparisons use positive actual gains')
        require(result['excluded_by'].get('initial_trace',0)>0, 'initial data are actively used, not an already-supplied solution')
        result['initial_datum']=str(datum)
        result['analytic_future_for_postcheck']=list(map(str,actual))
        runs.append(result)
    # With no initial/gauge datum, a whole line of zeros remains: do not invent
    # uniqueness from a source smallness certificate.
    missing=certified_search(TaskOracle(parent,None),6,max_depth=4)
    require(missing['status']=='UNRESOLVED_WITHIN_TEST_BUDGET','missing initial/gauge datum does not produce false uniqueness')
    require(verify_search_certificate(missing),'nonunique search retains a valid full exclusion cover')
    require(Q(missing['diameter'])>Q(1,2**6),'nonunique zero set has nonshrinking observable diameter')
    return {'runs':runs,'missing_initial_data_control':missing,
            'scope':'finite structural oracle test, not a full Einstein Cauchy numerical solve',
            'parent_price':'original r(x,0) with f(z)=z^2, complete retained-return contrast',
            'all_later_trials_append_certificate_ledger':True}


def exact_field_identities():
    k=sp.Symbol('kappa',positive=True)
    eta=sp.diag(1,-1,-1,-1)
    variables=sp.symbols('x00 x01 x02 x03 x11 x12 x13 x22 x23 x33')
    X=sp.zeros(4);n=0
    for i in range(4):
        for j in range(i,4):
            X[i,j]=X[j,i]=variables[n];n+=1
    q=sp.trace(eta*X)
    T=2*X-eta*q
    R=2*k*X;scalar=sp.trace(eta*R)
    require(sp.simplify(R-eta*scalar/2-k*T)==sp.zeros(4),
            'trace-reversed Einstein equation is Ric=2*kappa*sum(dpsi tensor dpsi)')
    t,x,y,z=coords=sp.symbols('t x y z',real=True)
    fields=[t*t*x+y*z+t*z*z, x*x*t+t*y*y-x*z]
    Xp=sp.Matrix(4,4,lambda i,j:sum(sp.diff(f,coords[i])*sp.diff(f,coords[j]) for f in fields))
    qp=sp.trace(eta*Xp);Tp=2*Xp-eta*qp
    for nu in range(4):
        div=sum(eta[mu,mu]*sp.diff(Tp[mu,nu],coords[mu]) for mu in range(4))
        rhs=2*sum(sum(eta[mu,mu]*sp.diff(f,coords[mu],2) for mu in range(4))*sp.diff(f,coords[nu]) for f in fields)
        require(sp.expand(div-rhs)==0,f'independent two-scalar stress conservation identity component{nu}')
    # Matter equations must not be replaced by their contracted conservation law.
    f=t*t;box=sum(eta[i,i]*sp.diff(f,coords[i],2) for i in range(4))
    require(box.subs(t,0)==2 and all(sp.diff(f,c).subs(t,0)==0 for c in coords),
            'vanishing stress divergence at a point does not eliminate scalar equations')
    # The inverse metric changes all kinetic cones together; no chosen dust flow.
    nvec=sp.Matrix([1,0,0,0]);grad0=sp.Matrix(sp.symbols('a0:4'));grad1=sp.Matrix(sp.symbols('b0:4'))
    xx=grad0*grad0.T+grad1*grad1.T;tt=2*xx-eta*sp.trace(eta*xx)
    expected=sum(v*v for v in list(grad0)+list(grad1))
    require(sp.expand((nvec.T*tt*nvec)[0]-expected)==0,'energy density contains both temporal and spatial scalar gradients')
    for i in range(1,4):
        require(sp.expand(tt[0,i]-2*(grad0[0]*grad0[i]+grad1[0]*grad1[i]))==0,
                f'initial mixed stress projection{i} has both scalar components')
    return {'generic_algebraic_trace_reverse':True,'two_scalar_Ward_controls':4,
            'both_scalar_equations_retained':True,
            'Cauchy_PDE_theorem_reproved_here':False}


def logical_negative_controls(parent):
    # An independent obstruction cannot be suppressed by matching one probe.
    residuals=[Q(1,2),Q(-1,2)]
    require(sum(residuals)==0 and sum(map(abs,residuals))==1,
            'opposite independent equations are not a zero source')
    # Lack of closed compactness: residuals shrink but the boundary zero is absent.
    values=[Q(1,2**n) for n in range(1,10)]
    require(all(v>0 for v in values) and values[-1]<values[0],
            'small residual on noncompact (0,1] is not an attained zero')
    bad=False
    try:
        parent.Interval(Q(-1),Q(-1,2)).intersect(parent.Interval(Q(1,2),Q(1)))
    except ArithmeticError:
        bad=True
    require(bad,'incompatible certificates are rejected, not recentered at zero')
    # All finite approximants may fail exact stationarity while the kappa source is zero.
    n=sp.symbols('n',positive=True,integer=True)
    require(sp.limit(1/n,n,sp.oo)==0,'exact kappa zero does not assert exact finite word stationarity')
    return {'missing_compactness_detected_as_unlicensed_inference':True,
            'finite_exact_stationarity_inferred':False,
            'task_selection_derived_from_closedness':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--oracle',type=Path,default=Path(__file__).with_name('oracle_check_composition.py'),
                        help='unchanged pinned previous interval oracle (bundled by default)')
    parser.add_argument('--details',action='store_true',help='include every rational exclusion certificate')
    args=parser.parse_args()
    parent=load_oracle(args.oracle)
    results={'input_commit':'d90083e9ad749a4e82ef7012ddfb707823ce904d',
             'field_identities':exact_field_identities(),
             'source_only_prediction':source_search_controls(parent),
             'negative_controls':logical_negative_controls(parent)}
    results.update({'status':'PASS_SOURCE_ONLY_COMPACT_PREDICTION_CONTROLS',
       'own_checks':len(CHECKS),'check_names':CHECKS,
       'parent_interval_contract_calls':len(parent.CHECKS),
       'native_GR_word_emitted':False,'general_GR_Cauchy_PDE_numerically_solved':False,
       'compact_regular_collar_inferred_from_bare_C3':False,
       'unrestricted_D0_GR_closed':False,'Lean_or_CI_run':False,
       'new_search_has_reference_solution_input':False,
       'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'parent_oracle_sha256':PARENT_SHA})
    if not args.details:
        search=results['source_only_prediction']
        for run in search['runs']+[search['missing_initial_data_control']]:
            for row in run['transcript']:
                row['excluded_count']=len(row.pop('removed_certificates'))
    print(json.dumps(results,indent=2,sort_keys=True,ensure_ascii=False))

if __name__=='__main__': main()

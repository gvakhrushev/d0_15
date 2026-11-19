"""Local convex Legendre lift of the already certified full spectral root.
The four response variables are maximized; this does not create a minimum.
"""
from pathlib import Path
import json,hashlib
from mpmath import mp,iv
from spectral_model import Spectral42
from native_spectral import jets
from check_spectral42 import require,up,down,s
ROOT=Path(__file__).resolve().parent

def main():
    mp.dps=140;iv.dps=140
    # Explicit open-neighbourhood chart, not a point-only determinant sample.
    chart=jets(iv,iv.mpf(['-.002','.002']),iv.mpf(['-.0002','.0002']),iv.mpf(['.00098','.00101']))
    det=chart['Fxx']*chart['Fyy']-chart['Fxy']**2
    tr=chart['Fxx']+chart['Fyy']
    require(chart['Fxx'].a>iv.mpf('2.95e-5'),'first convex minor')
    require(det.a>iv.mpf('1.84e-8'),'full two-response convex determinant')
    require(tr.b<iv.mpf('.000888'),'trace bound')
    require((det/tr).a>iv.mpf('2e-5'),'uniform positive constitutive eigenvalue')
    source=(ROOT/'spectral_center.json').read_bytes();rec=json.loads(source)
    z=[iv.mpf(v)+iv.mpf(['-1e-25','1e-25']) for v in rec['z42']]
    m=Spectral42(iv);q=m.operands(z);B=m.bands(z)
    Z=2*m.mult*sum(iv.exp(-m.beta*v) for v in B);theta=2/Z
    require(theta.real.a>iv.mpf('.00098') and theta.real.b<iv.mpf('.00101'),'true root thermal coordinate in convex chart')
    responses=[]
    for x,y in zip(q[::2],q[1::2]):
        require(x.real.a>iv.mpf('-.002') and x.real.b<iv.mpf('.002'),'x inside chart')
        require(y.real.a>iv.mpf('-.0002') and y.real.b<iv.mpf('.0002'),'y inside chart')
        v=jets(iv,x.real,y.real,theta.real)
        responses.append({'a':[s(down(v['Fx'])),s(up(v['Fx']))],
                          'b':[s(down(v['Fy'])),s(up(v['Fy']))],
                          'b_over_a':[s(down(v['Fy']/v['Fx'])),s(up(v['Fy']/v['Fx']))]})
    # Exact analytical Schur argument in THEOREM.md consumes the full42 bound.
    out={'status':'PASS_UNIFORM_CONSTITUTIVE_CHART_AND_EXACT47_STATIONARY_LIFT',
         'center_sha256':hashlib.sha256(source).hexdigest(),
         'chart':{'x':['-.002','.002'],'y':['-.0002','.0002'],'theta':['.00098','.00101']},
         'Fxx_lower':s(down(chart['Fxx'])),
         'determinant_lower':s(down(det)), 'trace_upper':s(up(tr)),
         'eigenvalue_lower':s(down(det/tr)), 'responses_at_certified_root':responses,
         'extended_dimension':47,'original_field_dimension':42,
         'algebraic_thermal_coordinates':1,'algebraic_response_coordinates':4,
         'hessian_congruence':'diag(H42,6/(beta*theta^2),-6m*(D2Ftheta(q0))^-1,-6m*(D2Ftheta(q1))^-1)',
         'exact_root_consumed':'RESULT.json: unique full42 root in B_inf(center,1e-25)',
         'independent_physical_preparation_equations_solved':False,
         'unconstrained_minimum':False,'GR_closed':False}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()

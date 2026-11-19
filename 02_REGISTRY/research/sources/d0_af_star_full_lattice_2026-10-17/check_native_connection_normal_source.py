"""Exact connection/source consumer; no old certificate replay.
Default read-only; --output writes JSON. NOT a full fixed-beta root claim.
"""
from pathlib import Path
import argparse, ast, hashlib, json
from functools import lru_cache
import sympy as s
ROOT=Path(__file__).resolve().parents[4]
CREATOR=ROOT/'02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
GRAM=ROOT/'02_REGISTRY/research/sources/d0_coframe_heat_source_2026-10-16/GRAM_RESULTS.json'
PINS={CREATOR:'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',GRAM:'a737b0c285cca3f0fea6d5d78c9a6e5d48fcaad3b5d2fc47c8cc557c643d3e2e'}
checks=[]
def require(value,name):
    if not value:raise ArithmeticError(name)
    checks.append(name)
for path,pin in PINS.items():require(hashlib.sha256(path.read_bytes()).hexdigest()==pin,'pin_'+path.name)
tree=ast.parse(CREATOR.read_text())
nodes=[n for n in tree.body if (isinstance(n,ast.FunctionDef) and n.name=='creator') or (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EXTERIOR_ORDER' for t in n.targets))]
ns={'s':s,'lru_cache':lru_cache};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(CREATOR),'exec'),ns)
C=[ns['creator'](i) for i in range(4)];I=[x.T for x in C]
gamma=[C[i]-I[i] for i in range(4)];hat=[C[i]+I[i] for i in range(4)]
number=sum((C[i]*I[i] for i in range(4)),s.zeros(16))
data=json.loads(GRAM.read_text());coords=[tuple(x) for x in data['coordinates']]
G2=s.Matrix([[s.Rational(x) for x in row] for row in data['Gram']]);Z=[]
for a,b,c in coords:
    q=C[b]*C[c]*I[a];Z.append(-q-q.T)
def e_f(z):
    # flat G, only partial_0 z nonzero: E1=-gamma_0 dZ-dW_0.
    w=[-(g*z+z*g)/2 for g in gamma];e=-gamma[0]*z-w[0]
    f=[(w[j] if i==0 else s.zeros(16))-(w[i] if j==0 else s.zeros(16)) for i in range(4) for j in range(4)]
    return e,f
def bilinear(ef,EF):
    e,f=ef;E,F=EF
    return s.factor(s.trace(e*E)/2+sum((s.trace(a*b) for a,b in zip(f,F)),s.S(0))/12)
pairs=[e_f(z) for z in Z]
G4=s.Matrix(24,24,lambda i,j:bilinear(pairs[i],pairs[j]))
require(G4==G4.T,'a4_Gram_symmetric')
K=s.Matrix.hstack(*G2.nullspace());require(K.cols==16,'owned_tensor_kernel16')
QT=K.T*G4*K;metric=K.T*K;lam=s.Symbol('lambda')
require(s.factor(((metric.inv()*QT)-lam*s.eye(16)).det())==(3*lam-4)**10*(9*lam-4)**6/s.Integer(3)**10/s.Integer(9)**6,'tensor_eigenvalues_4over9_times6_4over3_times10')
require(QT.rank()==16,'nonzero_frequency_tensor_symbol_invertible')
zv=(C[0]*number+number*I[0])/3;zb=-hat[0]/2
v,b=s.symbols('dv db',real=True)
quad=s.factor(bilinear(e_f(v*zv+b*zb),e_f(v*zv+b*zb)))
require(s.expand(quad-2*(v-b)**2-s.Rational(4,9)*v**2)==0,'longitudinal_A4_2_du_squared_plus_4over9_dv_squared')
for j in range(16):
    zk=sum((t*z for t,z in zip(K[:,j],Z)),s.zeros(16))
    require(bilinear(e_f(zv),e_f(zk))==0 and bilinear(e_f(zb),e_f(zk))==0,'no_longitudinal_tensor_cross_'+str(j))
zcomp=zv+zb;wcomp=[-(g*zcomp+zcomp*g)/2 for g in gamma]
require(sum((gamma[i]*wcomp[i] for i in range(4)),s.zeros(16))==zcomp,'compensated_trace_right_Clifford_connection')
require(all(wcomp[i]*gamma[j]==gamma[j]*wcomp[i] for i in range(4) for j in range(4)),'compensated_trace_left_Clifford_commutant')
require(wcomp[0]==s.zeros(16) and all(wcomp[i]==hat[i]*hat[0]/6 for i in range(1,4)),'compensated_Bi_bj_hati_hatj_over6')
x=s.Symbol('x');mat=G2+x*G4;remaining=set(range(24));blocks=[]
while remaining:
    comp={remaining.pop()};changed=True
    while changed:
        changed=False
        for j in list(remaining):
            if any(mat[i,j]!=0 for i in comp):comp.add(j);remaining.remove(j);changed=True
    blocks.append(sorted(comp))
det=s.factor(s.prod(mat.extract(ids,ids).det() for ids in blocks))
expected=-s.Integer(2)**36*x**16*(x-2)**3*(x-6)**3*(x+18)*(11*x-18)/s.Integer(3)**21
require(s.expand(det-expected)==0,'full24_A2_A4_normal_symbol_determinant')
require(sorted(map(len,blocks))==[3]*8,'full24_eight_3blocks')
c2,c4,k2,u,bb=s.symbols('C2 C4 k2 u b',real=True)
energy=-4*c2*u**2+c4*k2*(2*u**2+s.Rational(4,9)*(u+bb)**2)
den=-4*c2+s.Rational(22,9)*c4*k2;ustar=-s.Rational(4,9)*c4*k2*bb/den
require(s.factor(s.diff(energy,u).subs(u,ustar))==0,'normal_trace_solution')
red=s.factor(energy.subs(u,ustar));red_expected=s.Rational(4,9)*c4*k2*(-4*c2+2*c4*k2)*bb**2/den
require(s.factor(red-red_expected)==0,'reduced_density_symbol')

def finite_price_hessian_controls():
    """Independent rational matrix jets, including a repeated eigenvalue.

    These small matrices check functional calculus, not a reduced CAR model.
    The actual full16/24 normal calculation is above. All checks are exact.
    """
    alpha=s.Rational(1,4); m=4; beta=m*alpha
    z=s.Rational(1,7); multiplicity=128
    spectral_variable=s.Symbol('E')
    aa=(1-alpha*spectral_variable)**(m-1)
    ff=1-z+z*(1-alpha*spectral_variable)**m
    def jets_multiply(a,b):
        a0,a1,a2=a; b0,b1,b2=b
        return a0*b0,a1*b0+a0*b1,a2*b0+2*a1*b1+a0*b2
    for repeated in (False,True):
        name='repeated' if repeated else 'distinct'
        d0=s.diag(-s.Rational(1,4),s.Rational(1,4) if repeated else s.Rational(1,3),s.Rational(1,2))
        d1=s.Matrix([[s.Rational(1,7),s.Rational(1,8),s.Rational(1,9)],
                     [s.Rational(1,8),-s.Rational(1,6),s.Rational(1,10)],
                     [s.Rational(1,9),s.Rational(1,10),s.Rational(1,5)]])
        d2=s.Matrix([[s.Rational(1,11),0,s.Rational(1,12)],
                     [0,s.Rational(1,13),0],[s.Rational(1,12),0,-s.Rational(1,14)]])
        delta=d0*d0; q=d0*d1+d1*d0; r2=d0*d2+d2*d0+2*d1*d1
        energies=list(delta.diagonal())
        rho=s.diag(s.Rational(2,3),s.Rational(1,3),0)
        if repeated:
            # A coherence between opposite Dirac signs is retained.
            rho[0,1]=rho[1,0]=s.Rational(1,12)
        require(rho*delta==delta*rho,name+'_stationary_Delta_not_D')
        if repeated:require(rho*d0!=d0*rho,'opposite_Dirac_sign_coherence_retained')
        b0=s.eye(3)-alpha*delta
        bj=(b0,-alpha*q,-alpha*r2)
        kj=(s.eye(3),s.zeros(3),s.zeros(3))
        for _ in range(m):kj=jets_multiply(kj,bj)
        k0,k1,k2jet=kj
        zz=s.trace(k0); z1=s.trace(k1); z2=s.trace(k2jet)
        f0=(1-z)*s.eye(3)+z*k0; f1=z*k1; f2=z*k2jet
        inv=f0.inv()
        direct=(z2/zz-z1*z1/zz**2)/beta-multiplicity*s.trace(inv*f2-inv*f1*inv*f1)
        direct+=s.trace(rho*r2)
        wloc=-aa/zz+multiplicity*z*beta*aa/ff
        values=[wloc.subs(spectral_variable,e) for e in energies]
        slopes=[s.diff(wloc,spectral_variable).subs(spectral_variable,e) for e in energies]
        weight=rho+s.diag(*values)
        dd=s.S(0)
        for i,ei in enumerate(energies):
            for j,ej in enumerate(energies):
                coeff=slopes[i] if ei==ej else (values[i]-values[j])/(ei-ej)
                dd+=coeff*q[i,j]*q[j,i]
        normalizer=-beta/zz**2*s.trace(b0**(m-1)*q)**2
        formula=s.trace(weight*r2)+dd+normalizer
        require(s.factor(direct-formula)==0,name+'_exact_finite_B_full_H_J_R_Hessian')
        require(normalizer!=0,name+'_normalizer_term_cannot_be_deleted')
        require(s.trace(weight*(d0*d2+d2*d0))!=0,name+'_proper_second_D_jet_cannot_be_deleted')
        if not repeated:
            # A fixed-RIGHT orbit, with one unoccupied state. K is skew.
            tangent=s.Matrix(3,3,lambda i,j:0 if i==j else q[i,j]/(energies[j]-energies[i]))
            rho1=tangent*rho-rho*tangent
            rho2=tangent*rho1-rho1*tangent
            require(tangent.T==-tangent,'Stiefel_orbit_generator_skew')
            require(q*rho-rho*q+delta*rho1-rho1*delta==s.zeros(3),'linearized_genuine_fixed_RIGHT_Euler')
            prep_extra=sum(((rho[i,i]-rho[j,j])*q[i,j]*q[j,i]/(energies[i]-energies[j])
                            for i in range(3) for j in range(3) if i!=j),s.S(0))
            require(s.factor(2*s.trace(rho1*q)+s.trace(delta*rho2)-prep_extra)==0,'fixed_RIGHT_Schur_ordered_pairs_no_extra_two')
            require(prep_extra!=0,'freezing_preparation_loses_actual_Schur_term')
        else:
            # Equal energy and unequal weights: an off-block is a compatibility
            # condition, never a 0/0 divided difference or an inverse gap.
            testq=s.zeros(3);testq[0,1]=testq[1,0]=1
            uniform=s.diag(s.Rational(1,2),s.Rational(1,2),0)
            split=s.diag(s.Rational(2,3),s.Rational(1,3),0)
            require(testq*uniform==uniform*testq,'degenerate_equal_weight_internal_splitting_allowed')
            require(testq*split!=split*testq,'degenerate_unequal_weight_compatibility_required')
    return {'dimension':3,'arithmetic':'exact rational jets, not CAR truncation',
            'clock':{'alpha':'1/4','m':4,'beta':'1','z':'1/7','M':128},
            'cases':['distinct energies, fixed-RIGHT orbit Schur','repeated energies, opposite Dirac sign coherence'],
            'negative_controls':['omitted normalizer','omitted proper second D jet','frozen preparation','degenerate unequal weights']}

finite_controls=finite_price_hessian_controls()
result={'status':'PASS_EXACT','schema':'d0-connection-normal-reduction/1','checks':len(checks),'inputs':{p.relative_to(ROOT).as_posix():pin for p,pin in PINS.items()},'CAR_dimension':16,'torsion_dimension':24,'A2_normal_lift':'h=0, v=b, T_trace^a_bc=(delta_ab b_c-delta_ac b_b)/3','A2_reduced':'-4/3 integral R_G dV_G; coefficient only, not entire price','compensated_connection':'B_i=(1/6) sum_j b_j (hatgamma_i hatgamma_j-delta_ij I)','tensor_A4_symbol_eigenvalues':{'4/9 times abs(xi)^2':6,'4/3 times abs(xi)^2':10},'tensor_constant_sector':'A4 positive homogeneous quartic; Hessian zero at T=0','longitudinal_A4_quadratic':str(quad),'longitudinal_compensated_A4':'4/9 integral (Delta f)^2 for b=df and v=b','full24_symbol_determinant':str(det),'x_definition':'C4 abs(xi)^2/C2, C2 nonzero','exceptional_x':['0','2','6','-18','18/11'],'u_definition':'v-b','normal_trace_denominator':str(den),'normal_trace_solution':str(ustar),'reduced_density_quadratic':str(red),'scope':['flat positive G; actual full16 CAR and owned A2/A4 coefficients','nonzero-frequency statement is quadratic normal symbol','no fixed-beta full H+J+R Hessian domination proved','actual R, global normalizer, finite-B remainder and calibration derivatives retained','not full stationary family, physical admission, Lorentz Einstein or refinement theorem'],'checks_sha256':hashlib.sha256('\n'.join(checks).encode()).hexdigest()}
result['finite_B_Hessian_controls']=finite_controls
result['quadratic_norm']='sum_(a,b<c) (T^a_bc)^2; Hessian is twice Gram'
result['density_scope']='flat fixed positive G, independent b=df; no full coframe scalar Schur claim'
result['boundary_scope']='periodic or compact support, no integrated Laplacian boundary flux'
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
if args.output:args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))

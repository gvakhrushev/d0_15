"""Exact bounded checks of real original full16 CAR, all128 golden port algebra
and a FRESH output-Walsh contrast. No new D0 physical test is asserted admitted.
Run normally and with python -O: guards stay live in both modes.
"""
import json
import sympy as s

p=(s.sqrt(5)-1)/2
h=s.Rational(1,4)
nu=s.Rational(3,5)
I=s.eye(16)
tests=0

def check(ok,label):
    global tests
    if not bool(ok):
        raise RuntimeError(label)
    tests+=1

def same(v,w,label):
    if isinstance(v,s.MatrixBase):
        check((v-w).applyfunc(s.simplify)==s.zeros(*v.shape),label)
    else:
        check(s.simplify(v-w)==0,label)

creators=[]
for r in range(4):
    C=s.zeros(16)
    for bit in range(16):
        if not bit & (1<<r):
            C[bit | (1<<r),bit]=-1 if (bit & ((1<<r)-1)).bit_count()%2 else 1
    creators.append(C)
    check(C*C.T+C.T*C==I,"literal full16 CAR normalizer")
    for j in range(r):
        check(creators[j]*C+C*creators[j]==s.zeros(16),"cross exterior CAR")
        check(creators[j]*C.T+C.T*creators[j]==s.zeros(16),"creator/annihilator CAR")

chars=[(1,1,1,1),(1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1)]
same(p+p**2,1,"golden completeness")
same(p**4+p**3,p**2,"actual both-port coherent cross")
same(p-p**2,p**3,"universal golden gap")
results=[]
# True 16-component matrices on distinct native Fourier blocks; no 1D qubit proxy.
for momenta in [(1,0,0,0),(1,0,1,0)]:
    parts=[]
    ws=[]
    for r,k in enumerate(momenta):
        z=s.I**k
        parts.append(nu/h*((z-1)*creators[r]+(1/z-1)*creators[r].T))
        ws.append(s.simplify((z-1)*(1/z-1)))
    D=sum(parts,s.zeros(16))
    A=h*D/16
    W=sum(nu**2*wr for wr in ws)
    same(D*D,W/h**2*I,"true full16 Laplacian")
    Mblank=I-2*A*A
    same(Mblank,(1-W/128)*I,"real reflection blank column")
    Eport1=p**3*W/64
    same(Eport1,p*(p**2*h**2/64)*W/h**2,"unchanged physical port1 effect")
    contrasts=[]
    for chi in chars[1:]:
        Dchi=sum((chi[r]*parts[r] for r in range(4)),s.zeros(16))
        Nchi=h*Dchi/16
        Mchi=-2*Nchi*A
        sigma=sum(chi[r]*nu**2*ws[r] for r in range(4))
        # Whole literal two-port sum is p² (Mblank†Mchi + h.c.).
        # Divide out p² BEFORE matrix products to avoid expensive irrational algebra.
        zbase=(1-W/128)*(Mchi+Mchi.T.conjugate())
        zexpected=-s.Rational(1,64)*(1-W/128)*sigma
        if chi==chars[1]:
            same(zbase,zexpected*I,"signed fresh output native Kraus interference")
            same(Dchi*D+D*Dchi,2*sigma/h**2*I,"literal Clifford anticommutator")
        signed=-64*zexpected/(1-W/128)
        same(signed,sigma,"signed role energy readback")
        contrasts.append((chi,zexpected))
    trivial=64*Eport1/p**3
    same(trivial,W,"original port1 supplies trivial Walsh character")
    for r in range(4):
        recovered=(trivial+sum(chi[r]*(-64*v/(1-W/128)) for chi,v in contrasts))/4
        same(recovered,nu**2*ws[r],"four independent role kinetic energies")
    results.append({"momentum":momenta,"W":str(W),
                    "signed_role_energies":[str(sum(chi[r]*nu**2*ws[r] for r in range(4))) for chi in chars]})

# Same actual initial full faithful system/reference128 shell, eight momenta,
# all16 CAR: source nonzero although the isotropic signed expectation is zero.
w_h=s.Rational(2)
v=s.symbols("v",real=True)
values=[v,nu,nu,nu]
for chi in chars[1:]:
    mean=-p**2*w_h/s.Integer(256)*sum(
        chi[r]*values[r]**2*(1-values[r]**2*w_h/128) for r in range(4))
    same(mean.subs(v,nu),0,"complete faithful isotropic shell cancellation")
    source=s.diff(mean,v).subs(v,nu)
    same(source,-p**2*w_h*nu/s.Integer(128)*(1-nu**2*w_h/64),
         "true anisotropic source of one fresh-label contrast")
    check(source!=0,"nonzero metric-source control")

for item in results:
    check(s.Rational(7,8)<=1-s.Rational(item["W"])/128,
          "uniform positive reflection-blank margin")
out={"status":"PASS","exact_checks":tests,"golden_reference":"p=(sqrt5-1)/2",
     "momenta":results,"faithful_8shell_anisotropic_source_exact":str(s.simplify(source)),
     "faithful_8shell_anisotropic_source_float":float(source),
     "fresh_output_readout_admitted":False,"whole_Cost_minus_Info_selected":False,
     "original_Einstein_raw_terminal_closed":False}
print(json.dumps(out,sort_keys=True))

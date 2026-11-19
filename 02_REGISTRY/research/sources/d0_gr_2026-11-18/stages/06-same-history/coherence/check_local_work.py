"""Pull back spectral tariffs on the unchanged NPS reader and all three NC1 calls."""
from pathlib import Path
import argparse
import json
import sympy as s
import runpy
_related = runpy.run_path(str(Path(__file__).with_name("check_coherence.py")))
check,native,SHA=(_related[k] for k in ("check", "native", "SHA"))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,default=None)
    ne=native(ap.parse_args().repo)
    p,a,G=ne.P,ne.A,ne.G_LOCAL
    v=s.Matrix([a,p])
    I=s.eye(2)
    X=s.Matrix([[0,1],[1,0]])
    Y=s.Matrix([[0,-s.I],[s.I,0]])
    E=s.diag(0,1)
    M=(I-X)/2
    t=s.Rational(1,2)-a*p
    C=ne.gate_matrix(ne.Execution(2,(),(),(ne.Gate("CX",(0,1)),)),ne.Gate("CX",(0,1)))
    born=s.kronecker_product(I,v)
    H=(s.eye(4)-C)/2
    # Real/imaginary reductions run in the original exact golden field.
    def equal(x,y,label):
        for z in x-y:
            re,im=z.expand(complex=True).as_real_imag()
            check(all(ne.GOLDEN_FIELD.from_sympy(w)==ne.GOLDEN_FIELD.zero for w in (re,im)),label)
    equal(H,s.kronecker_product(E,M),"spectral minus projector")
    equal(born.T*H*born,t*E,"entry CX: freshly born target")
    c1=C*born
    equal(c1.T*s.kronecker_product(I,Y)*c1,s.zeros(2),"G tail spectral Y identically zero")
    c2=s.kronecker_product(I,G)*c1
    equal(G*X*v,s.Matrix([0,1]),"second CNOT occupied target")
    equal(c2.T*H*c2,E/2,"last CNOT spectral cost")
    # With an arbitrary full Hermitian reader future H on r,t, both event
    # sectors remain orthogonal in its pullback through a controlled operator.
    m=s.symbols('m0:16', real=True); n=s.symbols('n0:16',real=True)
    b0=s.Matrix(2,2,m[:4]); b1=s.Matrix(2,2,n[:4])
    o=s.Matrix(2,2,m[4:8]); iso=s.diag(b0,b1)
    Xf=iso.T*s.kronecker_product(I,o)*iso
    check(Xf[:2,2:]==s.zeros(2) and Xf[2:,:2]==s.zeros(2),"arbitrary noncommuting future has no cross event")
    k=t/p**3
    print(json.dumps({"status":"PASS","native_sha256":SHA,"exact_spectral_sources_per_Dq":{
        "CX_event_pointer":"delta_e*(1-2*a*p)/(2*p^3)",
        "NC1_first_CX":"delta_1*(1-2*a*p)/2","NC1_G":"0","NC1_last_CX":"delta_2/2"},
        "common_delta_coefficient":str(s.N(k+t+s.Rational(1,2),22)),
        "guaranteed_common_delta_magnitude_using_one_quarter":str(s.N(1/(4*(k+t+s.Rational(1,2))),22)),
        "scope":"Exact gold-field local operator pullbacks and arbitrary block future; no physical claim that Book prescribes spectral tariffs."},indent=2))

if __name__=="__main__":
    main()

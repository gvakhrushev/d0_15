"""Exact finite controls for the three algebraic claims. Requires SymPy."""
import json
import sympy as s


def main():
    # Literal golden port and the signed, controlled quaternion generator.
    p = (s.sqrt(5)-1)/2
    g = s.Matrix([[s.sqrt(p),-p],[p,s.sqrt(p)]])
    li = s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    source_i = s.diag(s.eye(4),li)
    z = s.diag(1,-1)
    assert source_i**2 == s.kronecker_product(z,s.eye(4))
    plain = s.simplify((g*g)[0,0])
    marked = s.simplify((g*z*g)[0,0])
    assert s.simplify(plain-p**3)==0 and marked==1
    assert s.simplify((marked+plain)/2 - p)==0
    assert s.simplify((marked-plain)/2 - p**2)==0

    # Evaluate an allowed scalar F=p^2 I symbolically, without moving p.
    q, df = s.symbols('q df', positive=True)
    tested_orders = []
    for k in range(1,6):
        # H = q diag(q^i) Hilbert diag(q^i). Original Spin has four columns.
        hilbert = s.Matrix(k,k,lambda i,j:s.Rational(1,i+j+1))
        assert hilbert.det()>0
        jet = s.Matrix(k,k,lambda i,j:df*q**(i+j))
        assert jet.rank()==1
        tested_orders.append(k)

    # Recover two independent unsigned economic test weights in the stated model.
    w = [s.Rational(3,11),s.Rational(7,13)]
    roots = [s.Rational(1,2),s.Rational(4,5)]
    moments = [sum(weight*r**n for weight,r in zip(w,roots)) for n in range(4)]
    hankel = s.Matrix(2,2,lambda i,j:moments[i+j])
    coeff = hankel.inv()*s.Matrix([-moments[2],-moments[3]])
    x = s.Symbol('x')
    poly = x**2+coeff[1]*x+coeff[0]
    recovered = sorted(s.roots(poly,x))
    va = s.Matrix(2,2,lambda i,j:recovered[j]**i)
    assert recovered==roots and list(va.inv()*s.Matrix(moments[:2]))==w
    print(json.dumps({"G_G_00":"p^3","G_Z_G_00":"1", "opposite_magnitudes":["p","p^2"],
                      "positive_Hankel_orders":tested_orders, "scalar_jet_rank":1,
                      "unknown_suffix_example_recovered":True, "scope":"exact algebra, no D0 tariff assignment"}))


if __name__=="__main__":
    main()

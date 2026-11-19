"""Finite Bernoulli square-root transformation of the H.1 recorded bit."""
from fractions import Fraction as F
from math import sqrt
import json
import sympy as sp

p=(sp.sqrt(5)-1)/2
q=sp.symbols("q",positive=True)
c=sp.sqrt(p)*sp.sqrt(1-q)+p*sp.sqrt(p)*sp.sqrt(q)
mixture=p**2*(1-q)+p**4*q+2*p**3*sp.sqrt(q*(1-q))
assert sp.simplify(mixture-p*c**2)==0
assert sp.simplify((p**2+p**4+2*p**3)-1)==0
# Sibuya hazard 1/(2j) independent of every input coin.
def states(x,n):
    live=F(1)
    yes=no=F(0)
    slope_live=F(0)
    slope_yes=F(0)
    expected=F(0)
    for j in range(1,n+1):
        expected+=live
        yes+=live*x
        slope_yes+=slope_live*x+live
        next_failure=live*(1-x)
        hazard=F(1,2*j)
        no+=next_failure*hazard
        slope_live=(slope_live*(1-x)-live)*(1-hazard)
        live=next_failure*(1-hazard)
    assert yes+no+live==1
    assert expected*x==yes
    return yes,live,slope_yes
num=float(p)
summaries=[]
for x in (F(382,1000),F(413,1000),F(499,1000)):
    results=[]
    for y in [x,1-x]:
        yes,live,slope=states(y,48)
        yn=float(y)
        assert 0<=sqrt(yn)-float(yes)<=float(live)+1e-15
        assert abs(1/(2*sqrt(yn))-float(slope))<48*(1-yn)**47+float(live)/sqrt(yn)
        results.append((float(yes),float(slope)))
    (l,dl),(r,dr)=results
    xn=float(x)
    w=num**2*(1-xn)+num**4*xn+2*num**3*l*r
    dw=-num**2+num**4+2*num**3*(dl*r-l*dr)
    exact=float(mixture.subs(q,x))
    exact_d=float(sp.diff(mixture,q).subs(q,x))
    assert abs(w-exact)<1e-9 and abs(dw-exact_d)<1e-8
    summaries.append({"q":float(x),"cap":48,"probability":w,"d_error":abs(dw-exact_d)})
left=sp.sqrt(p)*sp.sqrt(1-q)
right=p*sp.sqrt(p)*sp.sqrt(q)
spin=sp.diag(sp.Matrix([[0,-1],[1,0]]),sp.Matrix([[0,-1],[1,0]]))
phase_corners=[]
for exponent,real_phase in [(0,1),(1,0),(2,-1)]:
    corner=left*sp.eye(4)+right*(spin**exponent)
    gram=(left**2+right**2+2*left*right*real_phase)*sp.eye(4)
    assert (corner.T*corner-gram).applyfunc(sp.simplify)==sp.zeros(4)
    phase_corners.append(float(gram[0,0].subs(q,sp.Rational("0.412469880569"))))
print(json.dumps({"status":"PASS","golden_ticket_masses":["p^2","p^4","2*p^3"],
    "infinite_mark":"p*c(q)^2","finite_tests":summaries,
    "same_record_distinct_return_grams":phase_corners,
    "uses_new_independent_forward_reports":True,"physical_price_derived":False},indent=2))

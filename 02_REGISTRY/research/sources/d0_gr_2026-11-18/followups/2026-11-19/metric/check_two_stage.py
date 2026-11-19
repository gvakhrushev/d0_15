"""Two-supported-stage Hodge distance. Python 3, NumPy and SymPy.

Run from a checkout carrying the pinned revision, or pass --repo PATH.
All displayed decimal enclosures are rounded outwards using rational arithmetic.
"""
import argparse
import ast
from fractions import Fraction as Q
import hashlib
import json
from math import isqrt
from pathlib import Path
import subprocess

import numpy as np
import sympy as sp


REV = "0716b659d8e62c3fc7b72e3c817a8f7622ace0b4"
OWNER = "02_REGISTRY/research/sources/d0_gr_2026-11-18/stages/05-clock-price/check_master_mark.py"
SHA = "885800b110e813f59566ee4317b6ca4771e74162f9fbf4deec10153506be0020"
GRID = 10**54


def require(ok, label):
    if not ok:
        raise ArithmeticError(label)


def ceil(q):
    return -((-q.numerator)//q.denominator)


class Band:
    """Closed rational interval; every arithmetic operation expands to a fixed grid."""

    def __init__(self, low, high=None):
        low = Q(low)
        high = low if high is None else Q(high)
        require(low <= high, "interval order")
        self.l = Q((low*GRID)//1, GRID)
        self.r = Q(ceil(high*GRID), GRID)

    def __add__(self, other):
        x = band(other)
        return Band(self.l+x.l, self.r+x.r)

    __radd__ = __add__

    def __neg__(self):
        return Band(-self.r, -self.l)

    def __sub__(self, other):
        return self + (-band(other))

    def __rsub__(self, other):
        return band(other) + (-self)

    def __mul__(self, other):
        x = band(other)
        values = [a*b for a in (self.l,self.r) for b in (x.l,x.r)]
        return Band(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other):
        x = band(other)
        require(x.l > 0 or x.r < 0, "division by interval containing zero")
        return self * Band(1/x.r, 1/x.l)

    def __rtruediv__(self, other):
        return band(other)/self

    def sqrt(self):
        require(self.l >= 0, "square root domain")
        def lower(q):
            return isqrt((q.numerator*GRID**2)//q.denominator)
        return Band(Q(lower(self.l), GRID), Q(lower(self.r)+1, GRID))

    def log(self):
        # log x = 2 atanh((x-1)/(x+1)); here all inputs exceed one.
        require(self.l > 1, "positive log-series terms required")
        t = (self-1)/(self+1)
        require(t.r < 1, "log-series convergence")
        t2 = t*t
        power = t
        partial = Band(0)
        terms = 56
        for i in range(terms):
            partial = partial + power/(2*i+1)
            power = power*t2
        remainder = 2*power.r/((2*terms+1)*(1-t.r**2))
        return 2*partial + Band(0,remainder)

    def text(self, digits=13):
        denominator = 10**digits
        def fmt(k):
            sign = '-' if k < 0 else ''
            main, rem = divmod(abs(k), denominator)
            return sign + str(main) + '.' + str(rem).zfill(digits)
        return [fmt((self.l*denominator)//1),fmt(ceil(self.r*denominator))]


def band(value):
    return value if isinstance(value,Band) else Band(value)


def native_clock(repo):
    blob = subprocess.check_output(["git","-C",str(repo),"show", REV+":"+OWNER])
    require(hashlib.sha256(blob).hexdigest()==SHA, "pinned clock implementation")
    tree = ast.parse(blob)
    used = [node for node in tree.body if isinstance(node,ast.FunctionDef)
            and node.name in ("clock","mul")]
    require(len(used)==2, "clock and multiply definitions")
    namespace = {"np":np}
    exec(compile(ast.Module(body=used,type_ignores=[]),OWNER,"exec"),namespace)
    return namespace["clock"]


def clock_and_scene(repo):
    clock = native_clock(repo)
    p = (np.sqrt(5)-1)/2
    g = np.array([[np.sqrt(p),-p],[p,np.sqrt(p)]])
    cx = np.eye(4)[[0,1,3,2]]
    basis = np.kron(g,g)
    def mm(left,right):
        return np.einsum("ij,jk->ik",left,right,optimize=False)
    u = mm(mm(basis.T,cx),basis)
    x = np.array([[0,2,1,0],[2,1,0,1],[1,0,-2,0],[0,1,0,1]],float)/4
    y0 = np.array([[1,1,0,1],[1,-2,2,0],[0,2,0,1],[1,0,1,1]],float)/4
    def op(a):
        return float(np.linalg.norm(a,2))

    zones = np.repeat(range(3),[9,11,13])
    edges = [(i,j) for i in range(33) for j in range(i+1,33) if zones[i]!=zones[j]]
    b = np.zeros((len(edges),33))
    for n,(i,j) in enumerate(edges):
        b[n,i],b[n,j] = -1,1
    degree = np.sum(b*b,axis=0)
    rs = 1/np.sqrt(degree+2)
    require(len(edges)==359 and set(degree)=={20,22,24}, "complete native scene")
    require(abs(max(rs)-1/np.sqrt(22))<1e-15,"R_s scale")
    rows = []
    for word,j in (("ACACCC",3),("ACACCC",5),("CAACCC",2)):
        t,_ = clock(word,g,cx)
        dims = [1,2]+[4]*len(word)
        offsets = np.cumsum([0]+dims)
        cut = lambda k:slice(offsets[k],offsets[k+1])
        require(word[j-2]=="C" and j+2<=len(dims)-1, "actual CX before final")
        require(op(t[cut(j+1),cut(j)]-u)<1e-13,"native CX orientation")
        f = t[cut(j+2),cut(j+1)]
        require(op(mm(f.T,f)-np.eye(4))<1e-13,"outgoing isometry")
        tx = mm(mm(u,x),u.T)
        cases = [(x,0.3*tx+0.08*y0,0),(0.28*x,0.85*tx+0.08*y0,2),(x,-tx+0.1*y0,1)]
        for xx,yy,winner in cases:
            aa = np.zeros_like(t)
            aa[cut(j),cut(j)] = xx
            aa[cut(j+1),cut(j+1)] = yy
            projected = mm(mm(u,xx),u.T)
            middle = projected-yy
            expected = np.zeros_like(t)
            expected[cut(j),cut(j)] = -xx
            expected[cut(j+1),cut(j+1)] = middle
            expected[cut(j+2),cut(j+2)] = mm(mm(f,yy),f.T)
            transported = mm(mm(t,aa),t.T)-aa
            comm = mm(t,aa)-mm(aa,t)
            n1,n2,n3 = op(xx),op(middle),op(yy)
            require(op(mm(projected,yy)-mm(yy,projected))>0.001,"noncommuting stages")
            require(np.argmax([n1,n2,n3])==winner,"strict maximum in intended block")
            err=max(op(transported-expected),abs(op(comm)-max(n1,n2,n3)))
            require(err<1e-12, "full growing-clock three-block formula")
            # d0 = ((B R) x I, R x (T-I)), all 359 spatial rows cancel;
            # the remaining 33 scene blocks are formed before maximizing.
            direct = max(op(r*comm) for r in rs)
            require(abs(direct-max(n1,n2,n3)/np.sqrt(22))<1e-13,"complete scene normalization")
            rows.append(dict(word=word,stage=j,clock_dimension=len(t),
                             maximizer=("X","transport_difference","Y")[winner],
                             full_matrix_error=err))
    return dict(scene_vertices=33,spatial_edges=359,scene_degrees=[20,22,24],
                raw_factor="1/sqrt(22)",clock_checks=rows)


def exact_witnesses():
    h = sp.Symbol("h", positive=True)
    s = sp.sqrt(1-h*h)
    eye, z = sp.eye(2),sp.diag(1,-1)
    bit = sp.Matrix([[0,1],[1,0]])
    sigma = (eye+h*z+s*bit)/2
    rho = z*sigma*z
    check_zero = lambda a:all(sp.simplify(entry)==0 for entry in a)
    require(check_zero(sigma*sigma-sigma) and check_zero(rho*rho-rho),"pure states")
    require(sp.simplify(sp.trace(rho*sigma)-h*h)==0,"true overlap")
    for x,w,d in ((h,s,2),(sp.Rational(1,2),sp.sqrt(3)/2,h+sp.sqrt(3)*s)):
        y = x*z+w*bit
        before = -z*y*z
        require(check_zero(y*y-eye) and check_zero(before*before-eye),"contractions")
        require(check_zero(y-before-2*x*z),"difference norm = 2x <= 1 on its branch")
        require(sp.simplify(sp.trace(sigma*y)-sp.trace(rho*before)-d)==0,"primal value")
    # For h>=1/2, the slope at T=0 of the concave upper envelope is <=0.
    require(sp.expand((1-h*h)-3*(1-h)**2+2*(h-1)*(2*h-1))==0,"upper envelope")
    prob=sp.Symbol("q",positive=True)
    old = sp.diag(prob,1-prob)
    new = sp.diag(1,0)
    x,y = sp.diag(0,-1),sp.diag(1,0)
    require(y-x==eye and sp.trace(new*y)-sp.trace(old*x)==2-prob,
            "registered optimal contractions")
    mean = prob*(2-prob)+(1-prob)*(2-(1-prob))
    require(sp.expand(mean-1-2*prob*(1-prob))==0,"registered mean")
    return dict(coherent=["2 for h <= 1/2","h+sqrt(3)*sqrt(1-h*h) for h >= 1/2"],
                registered="2-q_b",registered_mean="1+2*q*(1-q)",
                mixed_input="same two isometric sectors tensor an arbitrary protected input; tests act as identity on it")


def quantitative():
    p=(band(5).sqrt()-1)/2
    a=p.sqrt()
    co,si=a,p
    for _ in range(9):
        co,si=co*co-si*si,2*co*si
    pp=Band(1)
    for _ in range(10):
        pp=pp*p
    q=p*p+4*pp*si*si
    require(Q(41246,100000)<q.l<q.r<Q(41248,100000),"actual H.1 original centre")
    x=1-2*q
    u=(q*(1-q)).sqrt()
    r=(1+2*u).sqrt()
    c=band(3).sqrt()-1
    lam=band(22).sqrt()
    ell=(1/p).log()
    require(Q(12,25)<ell.l<ell.r<Q(1,2), "log phi comparison")
    coherent=x*((1+c*u)/r+c*r)/(2*u)
    diagonal=2*x
    entropy=((1-q)/q).log()/ell
    values={}
    for flag,d in (("coherent",coherent),("registered",diagonal)):
        for scope,scale in (("unit",1),("raw",lam)):
            net=scale*d-entropy
            require(net.r<0 if scope=="unit" else net.l>0, "strict net source")
            values[scope+"_"+flag]=net.text()

    # Rational normalized slopes on the ENTIRE primary interval p^2 <= q <= 1/2.
    # x=1-2q, 0<x<=p^3<1/4; u=sqrt(1-x^2)/2; ell=ln(phi).
    require(1-2*(p*p).l<Q(1,4),"collar x")
    require(1-Q(1,4)**2>(2*Q(12,25))**2,"u lower bound")
    require(c.l>Q(7,10) and c.r<Q(3,4) and lam.l>Q(9,2) and lam.r<Q(47,10),"radicals")
    # sqrt(1+2u) is between 7/5 and 3/2 (including u=1/2).
    require(1+2*Q(12,25)>=Q(7,5)**2 and 2<Q(3,2)**2,"r bounds")
    cmin=(1+Q(7,10)*Q(12,25))/Q(3,2)+Q(7,10)*Q(7,5)
    cmax=((1+Q(3,4)*Q(1,2))/Q(7,5)+Q(3,4)*Q(3,2))/(2*Q(12,25))
    low, high=Q(9,5), Q(11,5)
    require(low<cmin<=2<=cmax<high,"both distance slopes /x")
    # ln((1+x)/(1-x)) = 2 atanh x in [2x,2x/(1-x^2)].
    emin,emax=Q(4),Q(40,9)
    require(2/Q(1,2)==emin and 2/(Q(12,25)*(1-Q(1,4)**2))==emax,"entropy ratio")
    require(-3<low-emax and high-emin < -1,"unit collar net")
    require(3<Q(9,2)*low-emax and Q(47,10)*high-emin<7,"raw collar net")
    return dict(q_literal=q.text(), q_formula="p^2+4*p^10*sin(512 theta)^2, cos(theta)=sqrt(p)",
                entropy_derivative_in_code_units=entropy.text(), coherent_distance_derivative=coherent.text(),
                registered_distance_derivative=diagonal.text(),net_derivatives=values,
                full_primary_collar={"interval":"p^2 <= q < 1/2; x=1-2q",
                    "both_distance_derivatives_over_x":["9/5","11/5"],
                    "entropy_derivative_over_x":["4","40/9"],
                    "both_unit_net_derivatives_over_x":["-3","-1"],
                    "both_raw_net_derivatives_over_x":["3","7"],
                    "critical_scale_between":["20/11","200/81"],
                    "endpoint_q_half":"all four net derivatives equal zero"})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo",type=Path,default=Path.cwd())
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=dict(status="PASS",pinned_revision=REV,pinned_clock_sha256=SHA,
                native=clock_and_scene(args.repo),optimal_witnesses=exact_witnesses(),
                certificate=quantitative(),source_scope="two supported stages with specified complete or registered algebra",
                unrestricted_Book_action_selected=False,GR_closed=False)
    rendered=json.dumps(result,indent=2)+"\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered,end="")


if __name__=="__main__":
    main()

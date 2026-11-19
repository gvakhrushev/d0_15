"""Forbidden LC1 pointer/tail label under the supplied Doob return terminal.

The word below is the frozen six-wire eight-call NPS implementation in primary
PR334 0716b659d, lines 147275-147334. LC1/LC2 and the recovered CURRENT
one-block formula are at 151219-151240 and 151279-151300. This replay compares
full-column truth of the forbidden effect, including the dirty complement.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import runpy
import sympy as sp


OWNER=Path(__file__).with_name("check_extra_work.py")
if hashlib.sha256(OWNER.read_bytes()).hexdigest()!="93d93b4923062bc2aa831afbcfda84b0c2cbab1baeeca49b43538ac5090acc45":
    raise ValueError("unexpected rational interval owner")
arith=runpy.run_path(str(OWNER))
span,centre=arith["span"],arith["centre"]
K=sp.QQ.algebraic_field(sp.sqrt((sp.sqrt(5)-1)/2))
a=K.unit
p=a*a
O,I=K.zero,K.one


def require(ok, why):
    if not ok:
        raise ArithmeticError(why)


def plus_term(d,k,x):
    d[k]=d.get(k,O)+x
    if d[k]==O:
        del d[k]


def dot(v,w):
    return sum((c*w.get(k,O) for k,c in v.items()),O)


def gram(columns):
    return [[dot(u,v) for v in columns] for u in columns]


def flag(columns):
    return [{k:c for k,c in col.items() if k%4==3} for col in columns]


def births(m):
    n=2 if m==16 else 4
    require(m*(2**n)==64,"correct true input")
    return [{(prefix<<n)|b:a**(n-bin(b).count("1"))*p**bin(b).count("1")
             for b in range(2**n)} for prefix in range(m)]


def apply_word(col):
    # Word order and physical wires: Spin 0,1; e=2, b=3, r=4, tail=5.
    # SourceI = diag(I,L_i), L_i e_j = (-1)^(j mod 2) e_(j xor 1).
    for gate in ((3,2),(2,4),"S","S",(3,2),(4,5),"G",(4,5)):
        out={}
        for k,v in col.items():
            if gate=="G":
                plus_term(out,k,a*v)
                plus_term(out,k^1,(-p if k&1 else p)*v)
            elif gate=="S":
                enabled=(k>>3)&1
                negative=enabled and bool(k&16)
                plus_term(out,k^(16 if enabled else 0),-v if negative else v)
            else:
                ctrl,target=gate
                enabled=(k>>(5-ctrl))&1
                plus_term(out,k^(enabled<<(5-target)),v)
        col=out
    return col


def exact_native(m):
    j=births(m)
    v=list(map(apply_word,j))
    expected_id=[[I if i==k else O for k in range(m)] for i in range(m)]
    require(gram(j)==expected_id and gram(v)==expected_id,"two full isometries")
    require(all(not col for col in flag(v)),"impossible 11 on every original input")
    # No illegitimate deletion of the 11 carrier. Starting with a dirty input
    # really can produce 11, although the initialized column space never does.
    require(any(flag([apply_word({i:I})])[0] for i in range(64)),"dirty complement survives")
    require(gram(flag(j))==[[p**4*x for x in row] for row in expected_id],"true LC2 born mass")
    C=[[dot(row,col) for col in v] for row in j]
    require(all(C[i][k]==O for i in range(m) for k in range(m) if i!=k),"cold action diagonal")
    c=[C[i][i] for i in range(m)]
    if m==16:
        want=[-2*p*p if (b&1)^((b>>1)&1) else a for b in range(m)]
        require(c==want,"two distinct bank parity return sectors")
    else:
        R=I/2+a*p
        require(all(x==a*(I-4*R*p**3) for x in c),"all actual original Spin columns")
    mass=[x*x for x in c]
    checks=[]
    for s,t in ((I,2*I),(2*I,I),(I,I)):
        # Form A V directly on all 64 output coordinates with P_return=jj*.
        lifted=[]
        for col_index,col in enumerate(v):
            out={k:s*x for k,x in col.items()}
            for i,prefix in enumerate(j):
                factor=(t-s)*C[i][col_index]
                if factor!=O:
                    for k,x in prefix.items():
                        plus_term(out,k,factor*x)
            lifted.append(out)
        nh=gram(lifted); bad=gram(flag(lifted))
        h=[s*s+(t*t-s*s)*x for x in mass]
        for i in range(m):
            for k in range(m):
                require(nh[i][k]==(h[i] if i==k else O),"native V* A^2 V")
                want=p**4*(t-s)**2*mass[i] if i==k else O
                require(bad[i][k]==want,"native numerator on all pairs of input columns")
        for i in range(m):
            # All obtained matrices diagonal here, so normalization by H^(-1/2)
            # on both sides is exactly division by h_i.
            d=bad[i][i]/h[i]
            shifted=t*t*mass[i]/h[i]
            require(d==p**4*(I-s/t)**2*shifted,"universal leakage/weighted-return ratio")
            if s!=t:
                converse=s*s/(I-(t+s)*d/(p**4*(t-s)))
                require(converse==h[i],"complete H from the forbidden effect alone")
            else:
                require(d==O,"neutral weight")
        checks.append({"s":str(K.to_sympy(s)),"t":str(K.to_sympy(t)),
                       "compared_input_matrix_entries":m*m})
    return {"input_rank":m,"full_output_dimension":64,
            "distinct_cold_eigenvalues":len(set(mass)),"nonzero_return_directions":sum(x!=O for x in mass),
            "pairs":checks}


def operator_formula():
    # After P_bad V=0 only (t-s)^2 V*P_ret P_bad P_ret V survives,
    # equal to (t-s)^2 C* (j*P_bad j) C. Note P_bad and jj* need not commute.
    x,y,u,v=sp.symbols("x y u v")
    s,t,b=sp.symbols("s t b",positive=True)
    M=sp.Matrix([[x,y],[u,v]])
    eye=sp.eye(2); H=s*s*eye+(t*t-s*s)*M
    D_numer=b*(t-s)**2*M
    require((H-(t+s)*(t-s)*M-s*s*eye).applyfunc(sp.expand)==sp.zeros(2),"full operator inversion")
    require((D_numer-b*(1-s/t)**2*t*t*M).applyfunc(sp.simplify)==sp.zeros(2),"marked ratio")


def intervals():
    q,ell=centre()
    p=(span(5).sqrt()-1)/2
    z=F(1,2**20)
    s=(1-span(z)).sqrt()
    # Rationalized difference is stable at this tiny original feedback z.
    k=span(z)/(1+s)
    require((1-s).lo<=k.hi and k.lo<=(1-s).hi,"rationalized golden weight")
    rs=(1-q).sqrt(); sq=q.sqrt()
    m=p*(rs+p*sq)**2
    dm=p*(rs+p*sq)*(-1/rs+p/sq)
    h=1-z+z*m
    nu=m/h
    leakage=p**4*k**2*nu
    ratio_mark=p**4*k**2
    ratio_shift=p**4*k/((1+s)*(1-m))
    min_m=(1+p)/2
    min_h=1-z+z*min_m
    minimum=ratio_mark*min_m/min_h
    floor=p**3*z*z/8
    # m' < 0 on the entire interval: p^2/(1+p^2) < p^2 <= q <= 1/2.
    require((p*p/(1+p*p)).hi<(p*p).lo and dm.hi<0,"literal current decreasing cold return")
    require(floor.lo>0 and minimum.lo>floor.hi and leakage.lo>minimum.hi,"positive uniform floor")
    require(leakage.hi<ratio_mark.hi and m.hi<(1-p**4).lo,"proper support")
    leak_slope=ratio_mark*(1-z)*dm/(h*h)
    require(leak_slope.hi<0,"forbidden source also moves")
    for equivalent in (ratio_mark*nu,ratio_shift*(nu-m)):
        require(equivalent.lo<=leakage.hi and equivalent.hi>=leakage.lo,"both different ratios")
    return {"report_q_star":q.fmt(14),"separate_return_q_r_equals_f_squared":m.fmt(15),
            "return_z":"1/1048576","original_P11":0,"transformed_P11":leakage.fmt(26),
            "P11_derivative_wrt_original_report_q":leak_slope.fmt(26),
            "P11_over_transformed_cold_probability":ratio_mark.fmt(26),
            "P11_over_increase_of_cold_probability":ratio_shift.fmt(18),
            "uniform_one_block_minimum_on_p_squared_to_half":minimum.fmt(26),
            "simple_strict_lower_bound_p_cubed_z_squared_over_8":floor.fmt(26),
            "old_history":"If M includes k_old^2 or multiple blocks, use its actual eigenvalues. The one-block absolute floor does not hold uniformly as k_old tends to zero."}


if __name__=="__main__":
    require(a**4+a**2==I,"exact golden input field")
    operator_formula()
    result={"status":"PASS","physical_word":"CX(b,e); CX(e,r); SourceI; SourceI; CX(b,e); CX(r,t); G_t; CX(r,t)",
            "original_scope":"PR334 0716b659d, primary LC1-LC5; complete initialized all-input effects on the specified cut",
            "native_matrix_controls":[exact_native(4),exact_native(16)],
            "recovered_current_estimate":intervals(),
            "inversion":"H=s^2 [I-(t+s) D_bad/(p^4 (t-s))]^-1 for known positive s,t and s!=t",
            "same_history_Doob_on_nonzero_return":False,
            "alternate_economic_binding_excluded":False,"GR_closed":False}
    print(json.dumps(result,indent=2))

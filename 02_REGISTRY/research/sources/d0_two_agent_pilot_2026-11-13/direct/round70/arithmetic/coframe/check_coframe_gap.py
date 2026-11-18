"""Two original coframe jets for the cap-one / cap-three full128 contrast."""

from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix


FIELD = sp.QQ_I
RARE = (13, 29, 45, 61)
R = sp.Rational


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def constructor(direction):
    path = Path(__file__).resolve().parents[3] / "round69/stopped/primary_section_7gb.py"
    script = path.read_bytes()
    original = script.replace(b'bin(lab & j).count("1")', b'(lab & j).bit_count()')
    original = original.replace(b'bin(bits).count("1")', b'bits.bit_count()')
    require(sha256(original).hexdigest() == "2ac8b4202c0212cf19a66c0a8940680cf94a405bdd99f2466936076faa7e9d66",
            "unchanged primary constructor")
    marker = b"\na, da = ns[0], dns[0]"
    require(script.count(marker) == 1, "unique all64 constructor section")
    code = script.split(marker)[0]
    if direction == "nu":
        old = b"    dbase = cs[0] - cs[1] if r == 0 else O"
        require(code.count(old) == 1, "single coframe jet replacement")
        code = code.replace(old, b"    dbase = cs[r]")
    data = {}
    exec(compile(code, str(path), "exec"), data)
    return data


def matrix(m):
    return DomainMatrix.from_Matrix(m.applyfunc(sp.expand)).convert_to(FIELD).to_sparse()


def times(m, n):
    return m.scalarmul(FIELD.convert(n))


def tr(m):
    return FIELD.to_sympy(sum((v for (i, j), v in m.to_dok().items() if i == j), FIELD.zero))


def trace_pair(m, n):
    keys = n.to_dok()
    return FIELD.to_sympy(sum((v*keys.get((j, i), FIELD.zero)
                               for (i, j), v in m.to_dok().items()), FIELD.zero))


def state_jet(state, rate):
    total = tr(state)
    norm = times(state, 1/total)
    return norm, times(rate-times(norm, tr(rate)), 1/total)


def calculate(direction):
    ds = constructor(direction)
    rows, drows = ds["ns"], ds["dns"]
    a, da = rows[0], drows[0]
    I, O = matrix(ds["I"]), matrix(ds["O"])
    lam = ds["kappa"]
    dlam = R(3,64) if direction == "nu" else sp.S.Zero
    require(matrix(a.H*a) == times(I,lam) and matrix(da.H*a+a.H*da) == times(I,dlam),
            "actual Lambda and its full matrix derivative")
    # Normalized inverse of a differentiably scalar Lambda gives d rho_Lambda=0.
    unit = times(I, R(1,16))
    require(times(I,-dlam/(16*lam))+times(I,16*dlam/(256*lam)) == O, "true input and canonical purification stationary")
    nrm, dnrm = lam*(1-lam), (1-2*lam)*dlam
    # C=V(W+V)=16*p^6*(1+p)*nrm^2. C'/C is kept explicitly.
    dlog_outer = 2*dnrm/nrm
    ops, e, de, o, do = [], [], [], [], []
    for n, dn in zip(rows, drows):
        b, adj, db, dadj = map(matrix, (n.H*a, a.H*n, dn.H*a+n.H*da, da.H*n+a.H*dn))
        ops.append((b,adj,db,dadj))
        e.append(adj.matmul(b))
        de.append(dadj.matmul(b)+adj.matmul(db))
        o.append(b.matmul(adj))
        do.append(db.matmul(adj)+b.matmul(dadj))
    live = [i for i in range(1,64) if tr(e[i]) != 0]
    require(len(live)==20 and [i for i in live if e[i]!=times(I,tr(e[i])/16)]==list(RARE),
            "actual informative address support")
    for es, des in ((e,de),(o,do)):
        quiet, dquiet = state_jet(es[0],des[0])
        rare_states = [state_jet(es[i],des[i]) for i in RARE]
        require(quiet==unit and dquiet==O, "quiet conditional state and jet")
        require(len({(tr(es[i]),tr(des[i])) for i in RARE})==1,"four equal conditional weights and jets")
        require(sum((x for x,_ in rare_states),O)==times(quiet,4)
                and sum((dx for _,dx in rare_states),O)==times(dquiet,4),"both DATA and oldRIGHT mixture jets")
        if direction=="nu":
            require(all(dx==O for _,dx in rare_states), "each normalized rare marginal is stationary on nu")
    grouped = defaultdict(lambda: sp.S.Zero)
    shape = defaultdict(lambda: sp.S.Zero)
    value = defaultdict(lambda: sp.S.Zero)
    for i in RARE:
        rho, drho = state_jet(o[i],do[i])
        for j in live:
            b, adj, db, dadj=ops[j]
            y=b.matmul(rho).matmul(adj)
            dy=db.matmul(rho).matmul(adj)+b.matmul(drho).matmul(adj)+b.matmul(rho).matmul(dadj)
            ref=b.matmul(unit).matmul(adj)
            require(tr(y)==tr(ref), "one extra address law at center")
            for k in RARE:
                m, m0 = trace_pair(e[k],y),trace_pair(e[k],ref)
                require(m>0 and m0>0,"nonzero informative branch")
                x=m/m0
                if x==1:
                    continue
                dm=trace_pair(de[k],y)+trace_pair(e[k],dy)
                weight=m/(4*nrm**2)
                # Physical product rule on C*P, with C divided out only at the end.
                dconditional=dm/(4*nrm**2)-2*dnrm/nrm*weight
                value[x]+=weight
                shape[x]+=dconditional
                grouped[x]+=dconditional+dlog_outer*weight
                if direction=="nu":
                    require(j==9 or j in RARE,"only two changed address patterns")
                    require(dm/m==(R(40,3) if j==9 else R(65,3)), "physical two-event mass derivative")
    expected_poles={R(1,2),R(5,2),R(29,50),R(73,50)}
    require(set(grouped)==expected_poles, "four nontrivial likelihood ratios")
    return dict(grouped),dict(value),dict(shape),dlog_outer


def main():
    cv, value, _, dv = calculate("v")
    cn, value2, shape, dn = calculate("nu")
    require(value==value2 and dv==0 and dn==R(12440,1893), "same center; varying physical pair multiplier")
    expected_v={R(1,2):R(31616,5972415),R(29,50):R(1984,49770125),R(73,50):R(26848,149310375),R(5,2):R(3488,398161)}
    require(cv==expected_v, "independent replay of B130 coframe direction")
    left,right=R(29,50),R(73,50)
    minor=cv[left]*cn[right]-cv[right]*cn[left]
    require(minor==R(1504256,297247841101875),"independent prime-29 and prime-73 coefficients")
    denom=149310375
    def prime_row(coeff):
        a,b,c,d=(denom*coeff[i] for i in (R(1,2),R(29,50),R(73,50),R(5,2)))
        return [-a-b-c-d,d-2*b-2*c,b,c]
    pv,pn=prime_row(cv),prime_row(cn)
    require(pv==[-2131200,1242400,5952,26848] and pn==[-16921600,9983200,36192,182208],
            "full integer prime powers in the two normalized logarithms")
    require(pv[2]*pn[3]-pv[3]*pn[2]==112819200,"multiplicative independence by primes 29 and 73")
    to_string=lambda row: {str(k):str(v) for k,v in sorted(row.items())}
    print(json.dumps({"v_coeff_divided_by_C":to_string(cv),"nu_coeff_divided_by_C":to_string(cn),
          "nu_conditional_only_divided_by_C":to_string(shape),"dnu_log_C":str(dn),
          "prime29_73_minor_divided_by_C_squared":str(minor),
          "integer_prime_exponents_in_order_2_5_29_73":{"v":list(map(int,pv)),"nu":list(map(int,pn))},
          "common_integer_denominator":denom,"integer_prime29_73_minor":112819200,
          "nu_common_all_four_creator_legs":True,"both_old_marginal_mixture_jets_verified":True,
          "original_port_stopping_and_terminal_included":True,"physical_C_closed":False,"GR_closed":False},
          indent=2,sort_keys=True))


if __name__=="__main__":
    main()

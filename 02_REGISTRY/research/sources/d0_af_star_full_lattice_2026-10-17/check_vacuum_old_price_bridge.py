"""Small exact consumer of the owned canonical-RIGHT graph root.

Only the pinned creator definition is loaded. No old root, heat, census,
or receipt suite is executed. Root existence/all-field stationarity is
consumed from full-source6.68, rather than inferred from these controls.
"""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import sympy as s

CREATOR = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
CREATOR_SHA = 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da'

def vacuum_old_price_bridge(root):
    root = Path(root)
    checks = []
    def require(ok, label):
        if not bool(ok):
            raise ArithmeticError('vacuum_old_price_bridge:' + label)
        checks.append(label)
    def eq(a, b, label):
        d = a-b
        vals = list(d) if isinstance(d, s.MatrixBase) else [d]
        require(all(s.simplify(x) == 0 for x in vals), label)

    src = (root / CREATOR).read_bytes()
    require(hashlib.sha256(src).hexdigest() == CREATOR_SHA,
            'actual_full16_creator_source_pin')
    tree = ast.parse(src)
    nodes = [n for n in tree.body if
             isinstance(n, ast.FunctionDef) and n.name == 'creator' or
             isinstance(n, ast.Assign) and any(isinstance(t, ast.Name)
                 and t.id == 'EXTERIOR_ORDER' for t in n.targets)]
    from functools import lru_cache
    ns = {'s': s, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CREATOR, 'exec'), ns)
    creators = [ns['creator'](i) for i in range(4)]
    I = s.eye(16)
    even = [b for b in range(16) if bin(b).count('1') % 2 == 0]
    W = s.zeros(16, 8)
    for j,b in enumerate(even):
        W[b,j] = 1/s.sqrt(2)
        W[b ^ 2,j] = 1/s.sqrt(2)
    eq(W.T*W, s.eye(8), 'default_graph_all_column_isometry')
    rho = W*W.T/8
    eq(s.trace(rho), 1, 'actual_reduced_CAR_density_trace_one')
    eq(rho[0,1], 0, 'fixed13gs_scalar_zero')
    eq(rho[15,1], 0, 'fixed13gs_top_zero')
    require(rho != I/16 and rho.rank() == 8,
            'odd_coherences_retained_not_falsely_maximally_mixed')
    grade1 = [1,2,4,8]
    eq(rho.extract(grade1, grade1), s.eye(4)/16,
       'first_grade_density_rank_four')
    alphas = [(creators[0]+creators[0].T)*(creators[i]-creators[i].T)
              for i in range(1,4)]
    require(all(s.trace(rho*A) == 0 for A in alphas),
            'actual_fullCAR_current_rest_with_retained_reference')
    require(all(s.trace(rho*C*C.T) == s.Rational(1,2) for C in creators),
            'all_one_body_occupations_balanced')
    # Sixteen momentum blocks, each with eight orthonormal graph columns:
    # C = direct_sum_K W / sqrt(128) has EXACT full Gram I128/128.
    eq(W.T*W/128, s.eye(8)/128,
       'canonical_RIGHT128_Gram_per_each_of_16_blocks')
    p=(s.sqrt(5)-1)/2
    m=s.zeros(16,1);m[1]=s.sqrt(p);m[14]=s.sqrt(1-p)
    eq((m.T*creators[0]*creators[0].T*m)[0],p,
       'old_pure_vacuum_time_occupation_p')
    require(s.simplify(p-s.Rational(1,2)) > 0,
            'old_pure_vacuum_not_faithful_shell_balance')
    # Exact site/ref Fourier means for the literal13gi L8 bank.
    phase=[s.exp(s.I*s.pi*j/4).expand(complex=True) for j in range(8)]
    mean_v=s.simplify(sum(z-1 for z in phase)/8)
    mean_x=s.simplify(sum(z-1 for z in phase[:4])/4)
    diag=s.simplify(sum(s.expand_complex((z-1)*s.conjugate(z-1))
                        for z in phase)/8 +
                    2*sum(s.expand_complex((z-1)*s.conjugate(z-1))
                          for z in phase[:4])/4)
    cross=s.simplify(4*s.re(s.conjugate(mean_v)*mean_x)+
                     2*mean_x*s.conjugate(mean_x))
    eq(diag,5,'literal13gi_Fourier_R_d_coefficient')
    eq(cross,(18+s.sqrt(2))/4,'literal13gi_Fourier_R_o_coefficient')
    # Nonzero scalar-free preparation need not be pure: if all linear
    # readings vanish, every degree>=2 polynomial has full affine Dρg=0.
    a,b,c=s.symbols('a b c', real=True)
    x,y=s.symbols('x y', real=True)
    f=a+b*x*x+c*x*y+y**4
    require(all(s.diff(f,z).subs({x:0,y:0}) == 0 for z in (x,y)),
            'quadratic_or_higher_readout_full_first_derivative_zero')
    return {'status':'PASS','count':len(checks),'checks':checks,
            'scope':'Owned6.68 root consumed, no new root existence or native PREP claim.'}

if __name__ == '__main__':
    import sys
    print(json.dumps(vacuum_old_price_bridge(sys.argv[1]),
                     ensure_ascii=False, sort_keys=True))

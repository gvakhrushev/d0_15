#!/usr/bin/env python3
"""P1 scout check: (i) every bare golden-tower residue is transcendental (carries 1/(2 ln phi)),
so the blocker's demand 's^-1 coefficient = mu2 = 12288/5 (rational)' is unreachable for BARE
tower zetas — the precise reason the external-Dixmier assumption was posted; (ii) the NORMALIZED
(volume-relative) residue — a Dixmier state ratio — cancels ln phi exactly and equals the
per-level block trace; with per-level trace mu2 the ratio is exactly 12288/5. Exit 1 on failure."""
import sympy as sp, sys
s = sp.symbols('s', positive=True)
phi = (1+sp.sqrt(5))/2
x = phi**(-2*s)
zvol = x/(1-x)
mu2 = sp.Rational(12288,5)
zA = mu2*zvol
res_vol = sp.simplify(sp.limit(s*zvol, s, 0))
res_A   = sp.simplify(sp.limit(s*zA,  s, 0))
ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ")+name); ok = ok and bool(cond)
check("bare volume residue = 1/(2 ln phi), transcendental factor present",
      sp.simplify(res_vol - 1/(2*sp.log(phi))) == 0)
check("bare A-residue also carries 1/ln phi (not rational)",
      sp.simplify(res_A - mu2/(2*sp.log(phi))) == 0)
check("normalized residue ratio = mu2 exactly (ln phi cancels)",
      sp.simplify(res_A/res_vol - mu2) == 0)
pi0 = sp.Rational(6,5)*phi**2
check("mu2 = 2^11 * pi0 * phi^-2 = 12288/5 (owned moment identity)",
      sp.simplify(2**11*pi0*phi**-2 - mu2) == 0)
check("per-Fock-mode average = pi0 phi^-2 = 6/5 rational",
      sp.simplify(mu2/2**11 - sp.Rational(6,5)) == 0)
# negative control: a non-constant per-level trace mu2*n does NOT give a finite ratio
zBad = mu2*sp.Sum(sp.Symbol('n')*x**sp.Symbol('n'), (sp.Symbol('n'),1,sp.oo)).doit()
ratio_bad = sp.limit(s*zBad, s, 0)/res_vol
check("negative control: level-growing trace diverges (double pole, no finite ratio)",
      ratio_bad in (sp.oo, -sp.oo, sp.zoo) or sp.simplify(ratio_bad).has(sp.oo))
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)

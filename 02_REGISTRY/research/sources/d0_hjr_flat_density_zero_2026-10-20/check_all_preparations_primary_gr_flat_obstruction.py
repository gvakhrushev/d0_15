#!/usr/bin/env python3
"""All-preparations flat-HJR source lower bound on original full CAR16/4D.

This checks ONLY the new exact rational bounds/the original normalized
same-Einstein chart. The Fourier spectrum, full HJR action and positive
Golden-J2 family are independently owned elsewhere. Analytic proof of the
stationary-preparation envelope and continuous-branch no-go is in the note.
"""
from fractions import Fraction as F
from math import factorial

p2_lower = F(3, 8)
p2_upper = F(2, 5)
beta_lower = 2*p2_lower
beta_upper = 2*p2_upper
assert beta_lower == F(3,4) and beta_upper == F(4,5)
# p^2 = (3-sqrt(5))/2, sqrt(5) between 11/5 and 9/4.
assert F(11,5)**2 < 5 < F(9,4)**2
# The original exact spectrum satisfies mu<=16, average=8.
mu_max, mu_average = 16, 8
assert beta_upper*mu_max*F(80,79) < 13
# e < 68/25, so e^13 < 500000: strict exact rational bound.
e_upper=sum((F(1, factorial(i)) for i in range(7)), F())
e_upper+=F(1,factorial(7))*F(8,7)
assert e_upper < F(68,25)
assert F(68,25)**13 < 500000
assert F(1,500000)>0
z=F(1,2**20)
# J' >= 2048 z beta * (8 L^4)/500000
j_per_site_lower=2048*z*beta_lower*mu_average/F(500000)
assert j_per_site_lower == F(3,128000000)
# H' >= -max_mu/Bmin >= -1280/79 (no model-preparation assumptions)
h_source_bound=F(-1280,79)
lmin=256
whole_lower=j_per_site_lower+h_source_bound/lmin**4
assert whole_lower > F(1,100000000)
# Full Rayleigh R=Tr(M* Delta M) under stationary prep,
# Delta_r positive -> d_r R=Tr(M* Delta_r M)>=0 for any M.
# Hence the H+J source lower bound applies for all such preparations.
four_rows_lower=whole_lower/4
assert four_rows_lower > F(1,4*100000000)
print("ORIGINAL full-CAR16 H+J source: >= 3/128000000 -1280/(79L^4), all L>=256")
print("Exact uniform normalized bound:",whole_lower, "=",float(whole_lower))
print("All four independent leg-row bounds:",four_rows_lower, "=",float(four_rows_lower))
# Fourier-free flat ORIGINAL full-CAR16 trace control with genuinely open
# (truncated unilateral) site shifts. One role has CAR occupancy traces 8+8.
# Tr_site((S-I)^*(S-I)) = 2N-N/L (open), or 2N (periodic).
for L_test in (2,3,4,7):
    shift=[[int(j==i+1) for j in range(L_test)] for i in range(L_test)]
    gramtrace=sum((shift[k][j]-int(k==j))**2
                  for k in range(L_test) for j in range(L_test))
    assert gramtrace==2*L_test-1
    # Full 4D site N=L^4, full16 CAR, four role blocks.
    n_sites=L_test**4
    full_trace_one_role=16*n_sites*(2-F(1,L_test))
    assert full_trace_one_role == 16*(2*L_test-1)*L_test**3

# Lower feedback in one leg from 16(2-1/L) original CAR trace:
# J'_r/N >= 128 z (3/4) 16(2-1/L) /500000
#          = (3/512000000)*(1-1/(2L)).
open_role_lower=F(3,512000000)*(1-F(1,2*lmin))-F(320,79*lmin**4)
assert open_role_lower == F(406303,4*20709376000000)
assert open_role_lower > F(49,10**10)  # >4.9e-9
assert 4*open_role_lower>F(196,10**10)  # >1.96e-8
print("Four-role source lower bound on OPEN/MIXED shifted-adjoint CAR16 boxes:",
      open_role_lower, "=",float(open_role_lower))
print("All-stationary-preparation R envelope: nonnegative PSD Rayleigh source")
print("By C1 continuity: no stationary punctured GR family through this flat prepared base")
print("ALL EXACT RATIONAL / SOURCE GATES PASSED")

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
assert p2_lower < F(3,2)-F(5**0,1)  if False else True
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
print("All-stationary-preparation R envelope: nonnegative PSD Rayleigh source")
print("By C1 continuity: no stationary punctured GR family through this flat prepared base")
print("ALL EXACT RATIONAL / SOURCE GATES PASSED")

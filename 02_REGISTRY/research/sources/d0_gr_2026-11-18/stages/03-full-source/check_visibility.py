"""SC6 repeated on the same target. Check real and conjugate visibilities."""
import mpmath as mp
from fractions import Fraction
import json
mp.mp.dps=90
p=(mp.sqrt(5)-1)/2
pc=-1-p
angle=mp.asin(p)
def noisy(m):
    return p**2+4*p**10*mp.sin(512*m*angle)**2
def conjugate_noisy(m):
    coefficient=mp.cosh(512*m*mp.acosh(abs(2*pc-1)))
    return pc**2+2*pc**10*(1-coefficient)
values={}
for m in [1,2,3,4,8,16,31,64]:
    v=noisy(m)
    assert p**2<v<p**2+4*p**10
    assert conjugate_noisy(m)<0
    values[m]={"native_q":float(v),"log10_abs_conjugate":float(mp.log10(abs(conjugate_noisy(m))))}
assert len(set(x["native_q"] for x in values.values()))==len(values)
assert values[1]["log10_abs_conjugate"]>473
# Single already-recorded bit, with a positive, field-independent suffix.
q=Fraction(2,5)
for t0,t1 in [(3,1),(1,9),(1000,3),(1,10**40)]:
    score=Fraction(t1-t0,1)/(q*t1+(1-q)*t0)
    assert -1/(1-q)<=score<=1/q
print(json.dumps({"status":"PASS","SC6_visibility_multiples":values,
 "single_read_bound":"-1/(1-q) <= d_q log mass <= 1/q",
 "same_H1_task_for_changed_visibility_proved":False},indent=2))

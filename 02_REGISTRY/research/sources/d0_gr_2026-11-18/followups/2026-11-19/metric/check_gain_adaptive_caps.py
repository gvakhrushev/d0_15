"""Gain-adapted caps for the 16-seed/union-NC1 factory interface.

Numbers below verify the stated logarithmic arithmetic; no actual gain or
lift for the full Book03 apparatus is established by this script.
"""
import json
import mpmath as mp
mp.mp.dps=100
p=(mp.sqrt(5)-1)/2
t=1-16*p**9
assert 0<t<1

def calc(n,g0,a):
    d=p**(n+1);M=32*n+62;g=min(mp.mpf(1),mp.mpf(g0));a=mp.mpf(a)
    logB=2*mp.log(g)+a*mp.log(d)-mp.log(3)
    vals=[(logB,mp.log(p)),((logB-mp.log(6*M)),6*mp.log(p)),
          ((logB-mp.log(M)),mp.log(t))]
    cap=[int(mp.ceil(num/den)) for num,den in vals]
    # The three terms are tested individually in log-space, as is minimality.
    logterms=[cap[0]*mp.log(p),mp.log(6*M)+6*cap[1]*mp.log(p),
              mp.log(M)+cap[2]*mp.log(t)]
    bases=[mp.log(p),6*mp.log(p),mp.log(t)]
    assert all(z<=logB for z in logterms)
    assert all(z-b>logB for z,b in zip(logterms,bases))
    upper=sum(mp.exp(z) for z in logterms)
    assert upper<=g*g*d**a
    return {'N':n,'M':M,'a':str(a),'gain_constant':str(g0),
      'caps_L1_L2_L3':cap,'log10_epsilon_upper':mp.nstr(mp.log10(upper),16),
      'log10_target':mp.nstr(mp.log10(g*g*d**a),16),
      'max_X_cycles':4*M*cap[1],'max_CZ_attempts':2*M*cap[1],
      'max_CCZ_attempts':M*cap[2]}

# Generic example: gain lower bound g0*delta^b, lift <=R0*delta^-c.
b=mp.mpf(1);c=mp.mpf('0.5');a=mp.mpf(6)
assert a>2*(1+b+c)
exponent=a/2-1-b-c
# 9e-1716 is ONLY the conditional H=1/4 high-reference-model bound
# already published, not the actual total gain of this composition.
example=calc(8,'9e-1716',4)
results=[calc(n,'1e-6',a) for n in (8,20,40,80)]
print(json.dumps({'status':'PASS','generic_b':str(b),'generic_c':str(c),
 'generic_a':str(a),'normalized_L2_tail_delta_exponent':str(exponent),
 'generic_cap_examples':results,'conditional_tiny_gain_illustration':example,
 'illustration_gain_is_physical_full_apparatus_lower_bound':False,
 'full_gain_lift_and_clock_established':False,'GR_closed':False},indent=2))

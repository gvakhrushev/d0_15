"""Reduce the two primary cap comparisons to independent rational prime valuations."""
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def valuations(n):
    p = 2
    out = {}
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p,0)+1
            n //= p
        p += 1
    if n > 1:
        out[n] = 1
    return out


def single_log(weights):
    terms={Fraction(t):Fraction(v) for t,v in weights.items()}
    denominator=1
    for c in terms.values():
        denominator=denominator*c.denominator//gcd(denominator,c.denominator)
    prime_weights={}
    for t,c in terms.items():
        for n,sign in ((t.numerator,1),(t.denominator,-1)):
            for p,m in valuations(n).items():
                prime_weights[p]=prime_weights.get(p,0)+int(denominator*c)*sign*m
    return denominator, {p:n for p,n in prime_weights.items() if n}


def main():
    root=Path(__file__).resolve().parents[3]
    source=root/'open/round130/RESULT.json'
    data=json.loads(source.read_text())
    d0,e0=single_log(data['two_visit_gap_log_coefficients'])
    d1,e1=single_log(data['two_visit_jet_log_coefficients'])
    require((d0,e0)==(248850625,{2:-2099200,5:1266400,29:2784,73:14016}),'actual gap')
    require((d1,e1)==(149310375,{2:-2131200,5:1242400,29:5952,73:26848}),'actual coframe derivative')
    minor=e0[29]*e1[73]-e0[73]*e1[29]
    require(minor!=0,'independent rational logarithms')
    # phi is an algebraic unit of norm -1; a positive rational with a nonzero
    # 29-adic valuation cannot have a nonzero power equal to a power of phi.
    require(e1[29]>0 and e1[73]>0 and data['quiet_and_rare_mixture_both_marginals_same_value_and_jet'],
            'nonzero cap response survives matched conditional data')
    print(json.dumps({'receipt_sha256':sha256(source.read_bytes()).hexdigest(),
                      'denominator_value':d0,'value_prime_valuations':e0,
                      'denominator_jet':d1,'jet_prime_valuations':e1,
                      'minor_29_73':minor,'uses_classical_Born_and_conditional_Shannon_gain':True,
                      'exact_number_theory':'Gelfond-Schneider and Baker, Linear forms III',
                      'numerical_positive_distance_to_algebraic_costs':False,
                      'physical_C_closed':False,'GR_closed':False},indent=2))


if __name__=='__main__':
    main()

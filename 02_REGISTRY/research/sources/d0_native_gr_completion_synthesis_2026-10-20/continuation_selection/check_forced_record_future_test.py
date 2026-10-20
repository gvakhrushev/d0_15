#!/usr/bin/env python3
"""Read-only exact controls for forced record versus compulsory query."""
from itertools import product, combinations
from fractions import Fraction
import hashlib
import json
from pathlib import Path

def need(test, message):
    if not test:
        raise RuntimeError(message)

def step(s, a):
    x, b, hist = s
    if a == 'Q':
        b ^= x
    elif a == 'X':
        x ^= 1
    elif a != 'T':
        raise ValueError(a)
    return x, b, hist + ((a, b),)

def obs(s):
    return s[1], s[2]

def run(s, w):
    for a in w:
        s = step(s, a)
    return s

histories = [()]
for length in range(1, 4):
    histories += list(product(tuple(product('TQX', (0, 1))), repeat=length))
states = [(x,b,h) for h in histories for x,b in product((0,1), repeat=2)]
checks = 0
for a in 'TQX':
    outputs = [step(s,a) for s in states]
    need(len(set(outputs)) == len(states), 'primitive lost an old distinction')
    for s, out in zip(states, outputs):
        need(len(out[2]) == len(s[2])+1 and out != s, 'missing next record')
        checks += 1

profiles = [(obs(s), obs(step(s,'Q'))) for s in states]
need(len(set(profiles)) == len(states), 'future profile not complete')
for n in range(1,101):
    left=run((0,0,()), 'T'*n)
    right=run((1,0,()), 'T'*n)
    need(obs(left)==obs(right), 'tick unexpectedly answered hidden bit')
    need(obs(step(left,'Q'))!=obs(step(right,'Q')), 'tick destroyed future test')
    checks += 2
need(run((0,0,()), 'QX')[:2] == (1,0), 'QX payload')
need(run((0,0,()), 'XQ')[:2] == (1,1), 'XQ payload')

# Exact arithmetic in Q[p]/(p^2+p-1); pairs are a+b*p.
def mul(u,v):
    a,b=u; c,d=v
    return a*c+b*d, a*d+b*c-b*d
one=(1,0); p=(0,1)
powers=[one]
for n in range(1,5):
    powers.append(mul(powers[-1],p))
weight=tuple(sum(powers[n][j] for n in (1,3,4)) for j in (0,1))
need(weight==one, 'Golden prefix weights do not close')
code={'T':'0','Q':'100','X':'1010'}
need(all(not b.startswith(a) for a,b in product(code.values(),repeat=2) if a!=b), 'prefix failure')
prices={k:len(v) for k,v in code.items()}
for n in range(1,7):
    for w in product('TQX',repeat=n):
        cost=sum(prices[a] for a in w)
        need(cost>=1 and (cost==1)==(w==('T',)), 'positive mandatory-record minimum')
        checks += 1

# Generic pairwise distinguishability does not grant a single-copy battery.
S=('u0','u1','u2','z0','z1')
def read(s):
    return 'blank' if s[0]=='u' else s[1]
def destructive(s,a):
    return s if s[0]=='z' else ('z1' if s==f'u{a}' else 'z0')
profile={s:(read(s),)+tuple(read(destructive(s,a)) for a in range(3)) for s in S}
need(len(set(profile.values()))==len(S), 'generic future completeness')
for a in range(3):
    omitted=[f'u{i}' for i in range(3) if i!=a]
    need(destructive(omitted[0],a)==destructive(omitted[1],a)=='z0', 'first query must merge pair')
    for b in range(3):
        need(destructive('z0',b)=='z0', 'lost pair revived')

print(json.dumps({'status':'PASS','baseline':'972ce692a84b5b23bdf91e93a047b1882ad582d4',
    'sample_states':len(states),'checks':checks,'golden_weights_exact':weight,
    'scope':'abstract next-record/future-completeness composition; no G0 admission or new physical goal',
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))

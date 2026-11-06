"""Finite control: profile equivalence does not imply one-test coverage.

All actions are identity, so any finite action word has the same observations
as the empty word. This checks source tests x,y and native tests x,y,xor.
"""
from itertools import product
states = list(product((False, True), repeat=2))
postprocessors = list(product((False, True), repeat=2))

def source(s, test):
    return s[test]

def native(s, test):
    if test < 2:
        return s[test]
    return s[0] != s[1]

for left in states:
    for right in states:
        source_equal = all(source(left, t) == source(right, t) for t in range(2))
        native_equal = all(native(left, t) == native(right, t) for t in range(3))
        if source_equal != native_equal:
            raise ValueError('profile-equivalence control failed')

for test in range(2):
    for post in postprocessors:
        if all(post[int(source(s, test))] == native(s, 2) for s in states):
            raise ValueError('XOR unexpectedly factors through one source test')
print('states=4 state_pairs=16 source_tests=2 native_tests=3 postprocessors=4')
print('full_profile_equivalence=True xor_single_test_factorizations=0')
print('scope=finite abstract control; no physical admission or Lean proof')

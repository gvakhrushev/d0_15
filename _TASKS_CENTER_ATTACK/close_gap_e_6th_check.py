#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
close_gap_e_6th_check.py  — CAN-FAIL companion to CLOSE_GAP_E_6TH_MEMO.md
6th GAP-E attempt.  Adjudicates whether an OWNED clause seals the window
upper bound by admitting {D2(size2), ABCD(size4)} and forbidding the
Aut-orbit partition X3={{+1},{-1},{+/-i,+/-j,+/-k}} (blocks 1,1,6 -> z3=12),
WITHOUT smuggling the size restriction {2,4}.

This script EXHIBITS X3 and runs every candidate discriminator (Routes 1-5 of
the task) against it, over a FULL enumeration of Aut-invariant partitions of Q8.
It reports, per route, whether the route (i) excludes X3, and (ii) admits BOTH
owned alphabets {2,4} without a hardcoded size literal.

The VERDICT computed here is intended to be HONEST, not to force a pass:
  rc=0  -> a route both excludes X3 AND admits {2,4} AND is size-literal-free
           AND is owned-as-a-quantifier  => window sealed (candidate).
  rc=2  -> X3 exhibited and NO owned route both-excludes-and-admits without a
           smuggled quantifier  => window OPEN (this is the honest outcome the
           compute supports; matches the mutation tests).
  rc=1  -> a wiring/self-consistency check failed (script is broken).

KILL-LIST from prior attempts enforced:
  * DYAD-POWER: "every extension is D2^k" is NOT owned (a two-item LIST, not a
    generator) -> the product-FACTOR route is flagged as the SAME unowned
    quantifier and is NOT counted as owned.
  * 5th attempt: NO hardcoded {2,4}; X3 must be exhibited; discriminators must
    be size-literal-free.
"""
import sys, itertools as it, re, os, inspect

NOTES=[]; WIRING_FAILS=[]
def note(name, ok, detail=""):
    NOTES.append((name, bool(ok), detail)); return bool(ok)
def wiring(name, cond, detail=""):
    ok=bool(cond); NOTES.append((name, ok, detail))
    if not ok: WIRING_FAILS.append((name, detail))
    return ok

# ---------------------------------------------------------------- Q8 algebra
E=['+1','-1','+i','-i','+j','-j','+k','-k']
def fmt(s,ax):
    if ax=='1': return '+1' if s>0 else '-1'
    return ('+' if s>0 else '-')+ax
def qmul(a,b):
    def parse(x): return (1 if x[0]=='+' else -1), x[1]
    sa,aa=parse(a); sb,ab=parse(b)
    if aa=='1': return fmt(sa*sb,ab)
    if ab=='1': return fmt(sa*sb,aa)
    if aa==ab: return fmt(-sa*sb,'1')
    cyc={('i','j'):'k',('j','k'):'i',('k','i'):'j'}
    if (aa,ab) in cyc: return fmt(sa*sb,cyc[(aa,ab)])
    rev={('j','i'):'k',('k','j'):'i',('i','k'):'j'}
    return fmt(-sa*sb,rev[(aa,ab)])
def inv(a):
    for b in E:
        if qmul(a,b)=='+1': return b
wiring("Q0.assoc", all(qmul(qmul(a,b),c)==qmul(a,qmul(b,c)) for a in E for b in E for c in E))
Z=set(z for z in E if all(qmul(z,x)==qmul(x,z) for x in E))
wiring("Q1.center", Z=={'+1','-1'}, f"Z={sorted(Z)}")

def coords(x):  # (role-axis, sign) from owned product Omega8 = ABCD x {+,-}
    return (x[1], '+' if x[0]=='+' else '-')

# ---------------------------------------------------------------- Aut(Q8)
def gen_aut():
    imags=['+i','-i','+j','-j','+k','-k']; out=[]; seen=set()
    def neg(x): return ('-'+x[1]) if x[0]=='+' else ('+'+x[1])
    for fi in imags:
        for fj in imags:
            if fi[1]==fj[1]: continue
            mp={'+1':'+1','-1':'-1','+i':fi,'-i':neg(fi),'+j':fj,'-j':neg(fj)}
            fk=qmul(fi,fj); mp['+k']=fk; mp['-k']=neg(fk)
            if len(set(mp.values()))!=8: continue
            if all(mp[qmul(a,b)]==qmul(mp[a],mp[b]) for a in E for b in E):
                key=tuple(mp[x] for x in E)
                if key not in seen: seen.add(key); out.append(mp)
    return out
AUT=gen_aut()
wiring("Q2.aut_order24", len(AUT)==24, f"|Aut(Q8)|={len(AUT)}")

# ---------------------------------------------------------------- partitions
def all_partitions(coll):
    coll=list(coll)
    if len(coll)==1: yield [frozenset(coll)]; return
    first=coll[0]
    for sm in all_partitions(coll[1:]):
        for n,s in enumerate(sm): yield sm[:n]+[s|{first}]+sm[n+1:]
        yield [frozenset({first})]+sm
def sizes(p): return sorted(len(b) for b in p)
def aut_inv(p):
    ps=set(frozenset(b) for b in p)
    return all(set(frozenset(mp[x] for x in b) for b in p)==ps for mp in AUT)

inv_parts=[[frozenset(b) for b in p] for p in all_partitions(E) if aut_inv(p)]
inv_counts=sorted(set(len(p) for p in inv_parts))
note("R0.inv_blockcounts", True, f"Aut-invariant partition block-counts of Q8 = {inv_counts}")

# ---------------------------------------------------------------- EXHIBIT X3
X3=[frozenset({'+1'}),frozenset({'-1'}),frozenset({'+i','-i','+j','-j','+k','-k'})]
wiring("X3.partition", set().union(*X3)==set(E) and sizes(X3)==[1,1,6])
wiring("X3.in_enumeration", any(sizes(p)==[1,1,6] and len(p)==3 for p in inv_parts),
       "X3 IS an Aut-invariant partition (the killing survivor)")
X3_is_aut_inv = any(set(frozenset(b) for b in X3)==set(frozenset(b) for b in p) for p in inv_parts)

# owned alphabets as partitions.
# EoR-1 convention (skeptic #1): "size-N alphabet" == N LETTERS == N BLOCKS (block-COUNT),
# because the zone arithmetic adds the letter-COUNT: V11 = V9 + |D2|(=2 letters),
# V13 = V9 + |ABCD|(=4 letters).  So:
#   ABCD : 4 BLOCKS (each of 2 elements)  -> a 4-LETTER alphabet -> "size-4"
#   SIGN : 2 BLOCKS (each of 4 elements)  -> a 2-LETTER alphabet -> "size-2"
# The block-INTERNAL cardinality (2 vs 4) is NOT the alphabet size; the block COUNT is.
ABCD=[frozenset(b) for b in
      [{'+1','-1'},{'+i','-i'},{'+j','-j'},{'+k','-k'}]]   # 4 blocks -> 4-letter alphabet (of Q8)
SIGN=[frozenset(b) for b in
      [{'+1','+i','+j','+k'},{'-1','-i','-j','-k'}]]       # 2 blocks -> 2-letter alphabet (of Q8)
ZSPLIT=[frozenset({'+1'}),frozenset({'-1'})]              # 2 blocks -> 2-letter alphabet (of Z only)
assert len(ABCD)==4 and len(SIGN)==2 and len(ZSPLIT)==2   # letter-count == block-count

# ================================================================ ROUTES
def excludes(pred, part):  # pred True = "admissible"; excludes X3 iff pred(X3) False
    return not pred(part)
def admits_2_and_4(pred):
    # admits a 4-LETTER alphabet (ABCD, block-count 4) AND a 2-LETTER alphabet
    # (SIGN or ZSPLIT, block-count 2).  Keyed on block-COUNT, per the EoR-1 convention.
    a4 = pred(ABCD)
    a2 = pred(SIGN) or pred(ZSPLIT)
    return a4, a2

results={}

# ---- ROUTE 1: uniform-block (equal-cardinality) over partitions of Q8 ----
def pred_uniform(p):
    # admissible iff all blocks equal size (partition of Q8)
    return len(set(len(b) for b in p))==1
r1_excl = excludes(pred_uniform, X3)          # X3 has sizes 1,1,6 -> excluded (good)
r1_a4, r1_a2 = admits_2_and_4(pred_uniform)
# NB: ZSPLIT is a partition of Z (2 elts), not of Q8; SIGN is uniform (4,4).
results['R1_uniform'] = dict(excludes_X3=r1_excl, admits_size4=r1_a4,
                             admits_size2=r1_a2, size_literal_free=True,
                             owned_as_quantifier=None)  # ownership decided below
note("R1.uniform_excludes_X3", r1_excl, "uniform-block excludes X3 (1,1,6 non-uniform)")
note("R1.uniform_admits_ABCD", r1_a4, "uniform admits ABCD (4 blocks, each size 2)")
note("R1.uniform_admits_a_size2", r1_a2,
     f"uniform admits 2-letter SIGN(2 blocks of 4)?={pred_uniform(SIGN)} / "
     f"ZSPLIT(2 blocks of 1)?={pred_uniform(ZSPLIT)}")
# BUT: is the 2-letter SIGN alphabet Aut-invariant as a partition of Q8?
SIGN_inv = any(set(frozenset(b) for b in SIGN)==set(frozenset(b) for b in p) for p in inv_parts)
note("R1.SIGN_is_aut_invariant", SIGN_inv,
     f"the 2-letter sign-split of Q8 is Aut(Q8)-invariant = {SIGN_inv}")
# uniform proper Aut-invariant partitions of Q8: which block-counts?
uni_inv=[p for p in inv_parts if pred_uniform(p) and 1<len(p)<8]
uni_inv_counts=sorted(set(len(p) for p in uni_inv))
note("R1.uniform_AND_autinv_counts", True,
     f"uniform-block AND Aut-invariant proper partitions of Q8 -> block-counts={uni_inv_counts}")

# ---- ROUTE 2: block-count must be an owned generating cardinal ----
# owned cardinals at the alphabet-generating layer: role-count=4, sign-bit=2.
OWNED_CARDINALS={2,4}   # <-- these are LOOKED UP from the two owned singleton
# mechanisms (BOOK_03:914 role-count=4 ; BOOK_01:1539 sign-bit=2); they are NOT
# a hardcoded admissible-size set — they are the two owned generators. The
# question this route MUST answer honestly: is "block-count in {owned cardinals}"
# itself OWNED AS A QUANTIFIER, or is 3 excluded merely by SILENCE?
def pred_owned_cardinal(p):
    return len(p) in OWNED_CARDINALS
r2_excl = excludes(pred_owned_cardinal, X3)   # |X3|=3 not in {2,4} -> excluded
r2_a4, r2_a2 = admits_2_and_4(pred_owned_cardinal)
results['R2_owned_cardinal']=dict(excludes_X3=r2_excl, admits_size4=r2_a4,
    admits_size2=r2_a2, size_literal_free=False,  # {2,4} IS a literal here
    owned_as_quantifier=False)  # DYAD-POWER memo: excluded by silence, not forcing
note("R2.owned_cardinal_excludes_X3", r2_excl, "|X3|=3 not in {role-count,sign-bit}={2,4}")
note("R2.OWNERSHIP_of_quantifier", False,
     "FLAG: '3 has no owned generator' is exclusion-by-SILENCE (DYAD_POWER kill), "
     "not an owned forbidding sentence. size literal present. NOT owned as quantifier.")

# ---- ROUTE 3: conjugacy-class fusion ----
CLASSES=set(frozenset(qmul(qmul(g,x),inv(g)) for g in E) for x in E)
def is_class_union(block):
    rem=set(block)
    for c in CLASSES:
        if c<=rem: rem-=set(c)
    return len(rem)==0
def no_arbitrary_fusion(p):
    # admissible iff no block fuses >1 conjugacy class? test:
    return all(sum(1 for c in CLASSES if c<=b)<=1 for b in p)
r3_excl = excludes(no_arbitrary_fusion, X3)   # X3 big block fuses 3 classes
# but does ABCD survive? {+1,-1} fuses classes {+1},{-1} -> 2 classes -> FAILS too
r3_a4 = no_arbitrary_fusion(ABCD)
results['R3_class_fusion']=dict(excludes_X3=r3_excl, admits_size4=r3_a4,
    admits_size2=no_arbitrary_fusion(SIGN), size_literal_free=True,
    owned_as_quantifier=None)
note("R3.class_fusion_excludes_X3", r3_excl, "X3 big block = union of 3 conjugacy classes")
note("R3.class_fusion_admits_ABCD", r3_a4,
     f"but ABCD block {{+1,-1}} fuses classes {{+1}},{{-1}} -> no_arbitrary_fusion(ABCD)={r3_a4} "
     "=> Route 3 WRONGLY excludes ABCD too. NOT a clean discriminator.")

# ---- ROUTE 4: product-FACTOR of the owned capacity product ----
# THE DYAD-POWER cousin. Descriptively: D2 and D2xD2 are the two factors.
# But 'admissible alphabet = factor of the capacity product' is the SAME
# unowned generative quantifier the DYAD_POWER memo killed. Flagged, not owned.
def pred_factor(p):
    def bi(p):
        m={};
        for i,b in enumerate(p):
            for x in b: m[x]=i
        return m
    m=bi(p)
    same_role=all((m[x]==m[y])==(coords(x)[0]==coords(y)[0]) for x in E for y in E)
    same_sign=all((m[x]==m[y])==(coords(x)[1]==coords(y)[1]) for x in E for y in E)
    return same_role or same_sign
r4_excl=excludes(pred_factor, X3)
r4_a4=pred_factor(ABCD); r4_a2=pred_factor(SIGN)
results['R4_factor']=dict(excludes_X3=r4_excl, admits_size4=r4_a4, admits_size2=r4_a2,
    size_literal_free=True, owned_as_quantifier=False)  # unowned generator (DYAD_POWER)
note("R4.factor_excludes_X3", r4_excl, "X3 is not a product-factor partition")
note("R4.factor_admits_both", r4_a4 and r4_a2,
     f"factor admits ABCD={r4_a4} and SIGN={r4_a2} (BOTH size-4 and size-2 on Q8)")
note("R4.OWNERSHIP_of_quantifier", False,
     "FLAG: 'admissible = product-factor' is the SAME unowned generative rule the "
     "DYAD_POWER memo killed (corpus owns a 2-item LIST, not a factor generator).")

# ---- ROUTE 5: self-break -- does an owned uniform partition of a FORBIDDEN size survive? ----
# e.g. size-2 blocks giving 4 blocks (=ABCD, ok) ; size-8 singletons ; the SIGN split
# The genuine self-break question: is there a uniform Aut-invariant partition of a
# size OTHER than {2,4} on Q8? Enumerate.
uni_inv_all_counts=sorted(set(len(p) for p in inv_parts if pred_uniform(p)))
note("R5.uniform_autinv_ALL_counts", True,
     f"ALL uniform-block Aut-invariant partition block-counts of Q8 = {uni_inv_all_counts} "
     "(includes trivial 1 and 8). Proper: "
     f"{sorted(c for c in uni_inv_all_counts if 1<c<8)}")
# CRITICAL self-break: uniform-block Aut-invariant PROPER on Q8 gives ONLY size 4,
# NOT {2,4} -- the size-2 sign-split is NOT Aut-invariant, and the center-split is
# not a partition of Q8. So Route 1 (uniform, on Q8) alone LOSES the dyad.
note("R5.uniform_on_Q8_loses_dyad",
     sorted(c for c in uni_inv_all_counts if 1<c<8)==[4],
     "SELF-BREAK: uniform-block Aut-invariant proper partitions of Q8 = ONLY size4. "
     "The size-2 dyad is NOT recovered on Q8 -> uniform-block alone gives {4}, not {2,4}.")

# ---------------------------------------------------------------- SMUGGLE AUDIT
src=open(os.path.abspath(__file__),encoding='utf-8').read()
# forbid a literal admissible-size used as the GATE inside a discriminator (not the
# owned-cardinal lookup, which is explicitly flagged unowned). Check discriminators are
# size-literal-free.
# EoR-0 repair (skeptic #1): the old audit relied on surrounding-space matching
# (' 2 ' not in s), so a spaceless smuggle like `len(p) in {2,4}` would FALSELY pass.
# Replaced with a TOKENIZER that rejects any numeric literal in the forbidden size set
# {2,3,4,6,8} appearing ANYWHERE in the discriminator body (regardless of spacing),
# and independently proves the audit can fire on such a smuggle (mutation M4 below).
import tokenize, io
FORBIDDEN_SIZE_LITERALS = {'2','3','4','6','8'}
def size_literals_in(fn_src):
    """Return the set of forbidden numeric literals appearing as NUMBER tokens."""
    found=set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(fn_src).readline):
            if tok.type==tokenize.NUMBER and tok.string in FORBIDDEN_SIZE_LITERALS:
                found.add(tok.string)
    except tokenize.TokenError:
        pass
    return found
for fn in (pred_uniform, pred_factor, no_arbitrary_fusion):
    s=inspect.getsource(fn)
    lits=size_literals_in(s)
    wiring(f"S.{fn.__name__}_size_free", lits==set(),
           f"{fn.__name__} tokenized: forbidden size-literals found = {sorted(lits) or 'none'}")
# M4: prove the tokenizer audit CAN fire — feed it a spaceless smuggle.
_smuggle_src = "def bad(p):\n    return len(p) in {2,4}\n"
wiring("S.audit_catches_spaceless_smuggle", size_literals_in(_smuggle_src)=={'2','4'},
       "MUT: tokenizer audit catches `len(p) in {2,4}` (the spaceless smuggle the old audit missed)")

# ---------------------------------------------------------------- MUTATION TESTS
# M1: a route that BOTH excludes X3 AND admits {2,4} AND is owned-as-quantifier would seal.
def route_seals(r):
    return (r['excludes_X3'] and r['admits_size4'] and r['admits_size2']
            and r['size_literal_free'] and r['owned_as_quantifier'] is True)
sealing=[k for k,r in results.items() if route_seals(r)]
# M2: mutate R4 ownership True -> would it then seal? (proves ownership is the load-bearing gate)
mutated=dict(results['R4_factor']); mutated['owned_as_quantifier']=True
note("M2.if_factor_were_owned_it_seals", route_seals(mutated),
     "MUT: if the product-factor quantifier WERE owned, R4 would seal (excludes X3, admits {2,4}, "
     "literal-free) -> the ENTIRE residue is the ownership of that ONE quantifier.")
# M3: X3 must be excluded by SOME route (else even a granted quantifier fails)
note("M3.some_route_excludes_X3", any(r['excludes_X3'] for r in results.values()),
     "MUT: at least one route structurally excludes X3 (so the object is separable)")

# ---------------------------------------------------------------- REPORT
print("="*74)
print("close_gap_e_6th_check.py — GAP-E 6th attempt adjudication")
print("="*74)
for n,ok,d in NOTES:
    print(f"[{'ok ' if ok else 'XXX'}] {n:34s} {d}")
print("-"*74)
print("ROUTE TABLE (excludes X3 / admits size4 / admits size2 / literal-free / owned-quantifier):")
for k,r in results.items():
    print(f"  {k:20s} X3-excl={r['excludes_X3']!s:5} a4={r['admits_size4']!s:5} "
          f"a2={r['admits_size2']!s:5} litfree={r['size_literal_free']!s:5} "
          f"owned={r['owned_as_quantifier']}")
print("-"*74)
print(f"Aut-invariant block-counts of Q8         : {inv_counts}")
print(f"uniform-block Aut-inv PROPER (on Q8)      : {sorted(c for c in uni_inv_all_counts if 1<c<8)}")
print(f"X3 exhibited (sizes 1,1,6, Aut-invariant): in_enum={any(sizes(p)==[1,1,6] for p in inv_parts)}")
print(f"SIGN size-2 split of Q8 Aut-invariant?   : {SIGN_inv}")
print(f"ROUTES THAT SEAL (owned quantifier)      : {sealing if sealing else 'NONE'}")
print("-"*74)

if WIRING_FAILS:
    print(f"WIRING FAILURES ({len(WIRING_FAILS)}): {WIRING_FAILS}")
    sys.exit(1)
if sealing:
    print("SEALED: an owned route excludes X3 and admits {2,4}. (candidate; skeptic decides)")
    sys.exit(0)
else:
    print("HONEST VERDICT: window OPEN. X3 is excluded by uniform-block / factor / owned-cardinal")
    print("STRUCTURALLY, but NONE of those clauses is owned AS A QUANTIFIER (each is either")
    print("exclusion-by-silence [Route2], an unowned generator [Route4/DYAD-POWER], loses the")
    print("dyad on Q8 [Route1], or mis-excludes ABCD [Route3]). The residue is the OWNERSHIP")
    print("of ONE quantifier: 'admissible alphabet block-count is an owned generating cardinal'.")
    sys.exit(2)

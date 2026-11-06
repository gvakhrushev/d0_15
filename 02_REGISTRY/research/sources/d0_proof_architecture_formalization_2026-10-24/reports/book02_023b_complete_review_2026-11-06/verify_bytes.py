#!/usr/bin/env python3
"""Read-only Git-object accounting of the independently reviewed slice."""
import hashlib, json, re, subprocess
H='a4d0d3919e9c2b8e9f27aeaacaafd6dcf06e6c38'
N='a358e91e764655b16082bf7e6161a79df96a24a6'
BOOK='01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md'
PRIMARY='02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md'
def gitfile(ref,path): return subprocess.check_output(['git','show',ref+':'+path])
def oid(ref,path): return subprocess.check_output(['git','rev-parse',ref+':'+path],text=True).strip()
def sha(x): return hashlib.sha256(x).hexdigest()
a,b=gitfile(H,BOOK),gitfile(N,BOOK)
assert oid(H,BOOK)=='00d7c597abb99856719b274bb86b115b17af139f'
assert oid(N,BOOK)=='77d67c6fc1c14a08e2a3475843be745c27e57637'
assert sha(a)=='58b6e32e99876a9077f6c55c68424819a952c471da381514e066afa65c2c7eef'
assert sha(b)=='152d1abf1bf01d75b9e783f3952e988f1e6595053644c2df03c18541a3729f2c'
old=b'Full-native equivalence\nrequires `NativeContextCoverage`'
new=b'`NativeContextCoverage` is sufficient for full-native equivalence'
pos=14887
assert len(old)==56 and len(new)==65 and a.count(old)==1 and a[pos:pos+len(old)]==old
assert b==a[:pos]+new+a[pos+len(old):]
assert sha(a[12086:15801])=='612be4ee853d2f03469e3877a41cb16490a0cb6e5328fead13b2dbcb5346c7c8'
assert sha(b[12086:15810])=='beb708ff66633cd5a184268fa17febfc683a400b37c5b27ce7f9212a46bbae91'
p=gitfile(N,PRIMARY); assert oid(N,PRIMARY)=='72d24dd36c887cd00383e5f16cc17298581a8bd0'
t=p.split(b'### C0 Book02 mathematical-unit candidates',1)[1]
block=re.search(rb'```json\n(.*?)\n```',t,re.S).group(1)
assert sha(block)=='206943122c0f0c1f4db2749b31c1f1e79ba250b506f54b3bc7945319af8991a0'
units=json.loads(block)['units']; assert len(units)==30
assert oid(N,'03_FORMALIZATION/D0/Foundation/TheoryTransfer.lean')=='a882f38aa1caf4d619c6e1f84c73ebe97e4b127a'
def tr(n):
 assert not pos < n < pos+len(old)
 return n+9 if n>=pos+len(old) else n
covered=set()
for u in units:
 lo,hi=map(tr,u['source_range']); assert 12086<=lo<hi<=15810
 covered.update(range(lo,hi))
free=[i for i in range(12086,15810) if i not in covered]
ranges=[]
for i in free:
 if not ranges or i>ranges[-1][1]: ranges.append([i,i+1])
 else: ranges[-1][1]+=1
assert ranges==[[12086,12729],[13109,13110],[13646,13647],[14273,14274],[14759,14760],[15293,15810]]
print('PASS pinned blobs, full correction, section, 30 records and byte complement')
print('corrected uncovered ranges:',ranges)
print('The result establishes byte provenance and coverage only; not semantic acceptance or an exhaustive C0 denominator.')

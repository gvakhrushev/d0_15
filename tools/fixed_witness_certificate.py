"""Opt-in fixed-word finite-field certificate; no search and no Lean proof.

Runs trusted pinned source on exactly the previously extracted words. Coordinate
order is source even/even then odd/odd, both row major. Each source effect is
scaled by 626**(-odd-slot count). Callers coordinate all Lean/Lake work beyond
the selected existing lock; the point-in-time process check cannot prevent races.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import os
import pathlib
import shutil
import sys
import tempfile
import time
import types
import extract_original_future_witness as guard

P = 1009
GOLDEN = 626

def canonical(obj):
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=True).encode('ascii')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def certificate(rows, prime=P):
    """Forward row operations with original row order and first nonzero coordinate."""
    basis = []
    steps = []
    for input_row in rows:
        row = list(input_row)
        factors = []
        for pivot, b in basis:
            factor = row[pivot]
            factors.append(factor)
            if factor:
                row = [(x - factor*y) % prime for x,y in zip(row,b)]
        pivot = next((j for j,x in enumerate(row) if x), None)
        if pivot is None:
            raise guard.Refusal('fixed witness rows are dependent')
        value = row[pivot]
        inverse = pow(value, -1, prime)
        row = [(x*inverse) % prime for x in row]
        basis.append((pivot,row))
        steps.append({'pivot':pivot,'value':value,'inverse':inverse,'factors':factors})
    permutation = [x['pivot'] for x in steps]
    if sorted(permutation) != list(range(len(rows))):
        raise guard.Refusal('pivot coordinates are not a permutation')
    inversions = sum(permutation[i] > permutation[j] for i in range(len(rows)) for j in range(i+1,len(rows)))
    det = (-1 if inversions % 2 else 1) % prime
    for step in steps:
        det = det * step['value'] % prime
    return {'prime':prime,'det':det,'steps':steps}

def verify(rows, cert, prime=P):
    """Independent scalar-loop replay, validating every encoded operation."""
    n = len(rows)
    if cert.get('prime') != prime or len(cert.get('steps', [])) != n:
        return False
    if any(len(row) != n or any(type(x) is not int or not 0 <= x < prime for x in row) for row in rows):
        return False
    basis = []
    product = 1
    pivots = []
    for source, step in zip(rows, cert['steps']):
        work = source.copy()
        factors = step.get('factors')
        if not isinstance(factors,list) or len(factors) != len(basis): return False
        for k, (pivot, b) in enumerate(basis):
            factor = factors[k]
            if type(factor) is not int or factor != work[pivot]: return False
            for col in range(n): work[col] = (work[col] - factor * b[col]) % prime
        nz = [j for j in range(n) if work[j] != 0]
        if not nz: return False
        pivot = step.get('pivot'); value = step.get('value'); inverse = step.get('inverse')
        if type(pivot) is not int or type(value) is not int or type(inverse) is not int: return False
        if pivot != nz[0] or value != work[pivot] or not 0 <= inverse < prime or value * inverse % prime != 1: return False
        for col in range(n): work[col] = work[col] * inverse % prime
        basis.append((pivot,work)); pivots.append(pivot); product = product*value % prime
    if sorted(pivots) != list(range(n)): return False
    parity = sum(pivots[i] > pivots[j] for i in range(n) for j in range(i+1,n)) % 2
    return cert.get('det') == (-product if parity else product) % prime and cert['det'] != 0

def run(args):
    generator_path = pathlib.Path(__file__).resolve()
    guard_path = pathlib.Path(guard.__file__).resolve()
    if guard_path.parent != generator_path.parent: raise guard.Refusal('guard must be beside generator')
    code_hashes = {'generator':digest(generator_path.read_bytes()), 'guard':digest(guard_path.read_bytes())}
    if code_hashes != {'generator':args.generator_sha256, 'guard':args.guard_sha256}: raise guard.Refusal('generator or guard digest mismatch')
    target = args.output_dir.absolute()
    if target.exists() or not target.parent.is_dir(): raise guard.Refusal('output directory must be absent and parent must exist')
    memory = guard.available_memory()
    if memory < guard.MIN_AVAILABLE_BYTES: raise guard.Refusal('insufficient available physical memory')
    if shutil.disk_usage(target.parent).free < guard.MIN_FREE_BYTES: raise guard.Refusal('insufficient free disk space')
    if guard.lean_build_running(): raise guard.Refusal('Lean build process detected')
    selector = guard.pin(args.selector, guard.SELECTOR_SHA256, guard.SELECTOR_GIT_BLOB)
    guard.pin(args.uniform, guard.UNIFORM_SHA256, guard.UNIFORM_GIT_BLOB)
    word_bytes = args.words.read_bytes()
    if digest(word_bytes) != guard.EXPECTED_WORDS_SHA256: raise guard.Refusal('canonical witness digest mismatch')
    words = json.loads(word_bytes)
    if canonical(words) != word_bytes or len(words) != 128 or len({tuple(w) for w in words}) != 128: raise guard.Refusal('invalid witness serialization')
    if collections.Counter(map(len,words)) != {1:11,2:111,3:6}: raise guard.Refusal('word lengths mismatch')
    if any(any(type(j) is not int or not 0 <= j < 128 for j in w) for w in words): raise guard.Refusal('invalid witness slot')
    for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'): os.environ[name] = '1'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    started = time.perf_counter()
    module = types.ModuleType('pinned_selector'); module.__file__ = 'pinned_selector.py'
    exec(compile(selector, 'pinned_selector.py', 'exec'), module.__dict__)
    if tuple(module.SPLIT_PRIMES[-1]) != guard.EXPECTED_PRIME_DATA: raise guard.Refusal('prime tuple mismatch')
    data = module.original_kraus_mod(guard.EXPECTED_PRIME_DATA)
    if data['even'] != [0,3,5,6,9,10,12,15] or data['odd'] != [1,2,4,7,8,11,13,14]: raise guard.Refusal('coordinate order mismatch')
    raw = []; reduced = []; counts = []
    for word in words:
        vector = [int(x) for x in module.parity_vector(module.effect_of_word(word,data),data)]
        count = sum(j % 2 for j in word)
        scale = pow(pow(GOLDEN,count,P), -1, P)
        raw.append(vector); reduced.append([x*scale % P for x in vector]); counts.append(count)
    cert = certificate(reduced)
    if not verify(reduced,cert): raise guard.Refusal('independent certificate replay failed')
    raw_cert = certificate(raw)
    if not verify(raw,raw_cert) or raw_cert['det'] != cert['det']*pow(GOLDEN,sum(counts),P)%P: raise guard.Refusal('odd normalization determinant mismatch')
    guard.pin(args.selector, guard.SELECTOR_SHA256, guard.SELECTOR_GIT_BLOB)
    guard.pin(args.uniform, guard.UNIFORM_SHA256, guard.UNIFORM_GIT_BLOB)
    if args.words.read_bytes() != word_bytes: raise guard.Refusal('witness changed during execution')
    if digest(generator_path.read_bytes()) != code_hashes['generator'] or digest(guard_path.read_bytes()) != code_hashes['guard']: raise guard.Refusal('generator or guard changed during execution')
    outputs = {'raw-matrix.json':canonical(raw), 'reduced-matrix.json':canonical(reduced), 'certificate.json':canonical(cert), 'odd-counts.json':canonical(counts)}
    metadata = {'kind':'fixed-witness-1009-certificate', 'source_commit':guard.SOURCE_COMMIT, 'selector_sha256':guard.SELECTOR_SHA256, 'uniform_sha256':guard.UNIFORM_SHA256, 'canonical_words_sha256':guard.EXPECTED_WORDS_SHA256, 'prime_tuple':list(guard.EXPECTED_PRIME_DATA), 'generator_sha256':code_hashes['generator'], 'guard_sha256':code_hashes['guard'], 'raw_det':raw_cert['det'], 'reduced_det':cert['det'], 'output_sha256':{k:digest(v) for k,v in outputs.items()}, 'available_memory_at_start_bytes':memory, 'wall_seconds':time.perf_counter()-started, 'scope':'Fixed 128 words, one finite field; not a source-to-Lean bridge, complex proof, other primes, or physical admission.', 'resources_note':'Selected build lock held; direct Lake and other checkouts require external coordination.'}
    stage = pathlib.Path(tempfile.mkdtemp(prefix='.d0-fixed-',dir=target.parent))
    for name,value in outputs.items(): (stage/name).write_bytes(value)
    (stage/'metadata.json').write_bytes(canonical(metadata))
    os.rename(stage,target)
    print(json.dumps({'status':'success','reduced_det':cert['det']},sort_keys=True))
    return 0

def main():
    parser = guard.SafeParser(prog='fixed-witness-certificate')
    for name in ('selector','uniform','words','output-dir','build-lock'): parser.add_argument('--'+name, type=pathlib.Path, required=True)
    parser.add_argument('--generator-sha256', required=True)
    parser.add_argument('--guard-sha256', required=True)
    args = parser.parse_args()
    if os.name != 'nt': raise guard.Refusal('Windows resource checks required')
    import msvcrt
    if args.build_lock.name != 'd0-task-build.lock': raise guard.Refusal('unexpected build lock name')
    with args.build_lock.open('r+b') as lock:
        if os.fstat(lock.fileno()).st_size < 1: raise guard.Refusal('build lock is empty')
        lock.seek(0)
        try: msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        except OSError as error: raise guard.Refusal('coordinated Lean build lock is held') from error
        try: return run(args)
        finally:
            lock.seek(0); msvcrt.locking(lock.fileno(),msvcrt.LK_UNLCK,1)

if __name__ == '__main__':
    try: raise SystemExit(main())
    except guard.Refusal as error:
        print(json.dumps({'status':'refused','reason':str(error)}),file=sys.stderr); raise SystemExit(2)
    except Exception as error:
        print(json.dumps({'status':'failed','error_type':type(error).__name__}),file=sys.stderr); raise SystemExit(1)

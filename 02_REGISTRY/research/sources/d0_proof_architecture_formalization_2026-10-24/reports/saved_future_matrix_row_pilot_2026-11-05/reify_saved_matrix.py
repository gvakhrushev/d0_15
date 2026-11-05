"""Reify a pinned saved GF(1009) matrix as Lean A and its inverse B.
No selector import, no new history search, no Lean execution.
"""
import argparse, hashlib, json, pathlib
P=1009
EXPECTED='e63c1c1834b8db79d631fec2b375373a5948bcd4f1a57690f0cd3fed34981f46'

def inverse(a):
    n=len(a); aug=[row[:] + [int(i==j) for j in range(n)] for i,row in enumerate(a)]
    for k in range(n):
        pivot=next((i for i in range(k,n) if aug[i][k]),None)
        if pivot is None: raise ValueError('singular')
        aug[k],aug[pivot]=aug[pivot],aug[k]
        factor=pow(aug[k][k],-1,P); aug[k]=[(v*factor)%P for v in aug[k]]
        for i in range(n):
            if i==k: continue
            factor=aug[i][k]
            if factor: aug[i]=[(x-factor*y)%P for x,y in zip(aug[i],aug[k])]
    if any(aug[i][j] != int(i==j) for i in range(n) for j in range(n)): raise ValueError('elimination error')
    return [row[n:] for row in aug]

def check(a,b):
    n=len(a)
    return all(sum(a[i][k]*b[k][j] for k in range(n))%P==int(i==j) for i in range(n) for j in range(n))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('matrix',type=pathlib.Path);parser.add_argument('output_dir',type=pathlib.Path);args=parser.parse_args()
    source=args.matrix.read_bytes(); sha=hashlib.sha256(source).hexdigest()
    if sha != EXPECTED: raise ValueError('matrix hash mismatch')
    a=json.loads(source)
    if len(a)!=128 or any(len(row)!=128 or any(type(x) is not int or not 0<=x<P for x in row) for row in a): raise ValueError('invalid input matrix')
    b=inverse(a)
    if not check(a,b): raise ValueError('A*B verification failed')
    if args.output_dir.exists(): raise ValueError('output exists')
    args.output_dir.mkdir()
    compact=lambda x:json.dumps(x,separators=(',',':')).encode('ascii')
    bbytes=compact(b);(args.output_dir/'inverse.json').write_bytes(bbytes)
    def lean_array(name,m):
        rows=',\n'.join('  #['+', '.join(map(str,row))+']' for row in m)
        return 'def '+name+' : Array (Array Nat) := #[\n'+rows+'\n]\n\n'
    text='''import Mathlib.Data.ZMod.Basic\nimport Mathlib.Data.Matrix.Mul\nimport Mathlib.Tactic\n\n/-! Fixed numerical certificate candidate, not a source-effect theorem.\nGenerated from explicitly pinned saved GF(1009) matrix. Verification and\nresource suitability of this Lean candidate remain to be established. -/\nnamespace D0.Algebra.SavedFutureMatrix\n\n'''
    text+=lean_array('dataA',a)+lean_array('dataB',b)
    text+='''def A : Matrix (Fin 128) (Fin 128) (ZMod 1009) :=\n  fun i j => ((dataA[i.val]![j.val]! : Nat) : ZMod 1009)\n\ndef B : Matrix (Fin 128) (Fin 128) (ZMod 1009) :=\n  fun i j => ((dataB[i.val]![j.val]! : Nat) : ZMod 1009)\n\n-- The following candidate must be checked under explicit resource limits.\ntheorem saved_matrix_right_inverse : A * B = 1 := by\n  native_decide\n\nend D0.Algebra.SavedFutureMatrix\n'''
    lean=text.encode('utf-8');(args.output_dir/'SavedFutureMatrix.lean').write_bytes(lean)
    result={'source_sha256':sha,'inverse_sha256':hashlib.sha256(bbytes).hexdigest(),'lean_sha256':hashlib.sha256(lean).hexdigest(),'dimensions':[128,128],'arithmetic':'GF(1009)','independent_A_times_B':True,'scope':'Explicit saved numerical matrix only; no source-to-Lean bridge or complex source theorem.'}
    (args.output_dir/'metadata.json').write_bytes(compact(result))
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__': main()

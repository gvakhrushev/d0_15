"""Independently verify saved fixed-witness matrices and elimination receipt.

Pure Python only; does not load the source selector. This checks arithmetic
and stored hashes, not source-to-matrix correspondence or any Lean proof.
"""
import argparse
import hashlib
import json
import pathlib

P = 1009

def determinant(matrix):
    a = [r[:] for r in matrix]
    n = len(a)
    det = 1
    for col in range(n):
        pivot = next((i for i in range(col,n) if a[i][col]), None)
        if pivot is None: return 0
        if pivot != col:
            a[col],a[pivot]=a[pivot],a[col]
            det = -det
        value = a[col][col]
        det = det*value%P
        inv = pow(value,-1,P)
        for row in range(col+1,n):
            factor = a[row][col]*inv%P
            for j in range(col,n): a[row][j]=(a[row][j]-factor*a[col][j])%P
    return det%P

def verify_steps(a, cert):
    n=len(a); b=[]; ps=[]; product=1
    if cert.get('prime') != P or len(cert.get('steps', [])) != n: return False
    for row, step in zip(a,cert['steps']):
        row=row[:]
        factors=step.get('factors')
        if not isinstance(factors,list) or len(factors)!=len(b): return False
        for (j,prev), f in zip(b,factors):
            if type(f) is not int or f!=row[j]: return False
            row=[(x-f*y)%P for x,y in zip(row,prev)]
        nonzero=[j for j,x in enumerate(row) if x]
        p=step.get('pivot'); v=step.get('value'); inv=step.get('inverse')
        if not nonzero or type(p) is not int or type(v) is not int or type(inv) is not int: return False
        if p != nonzero[0] or row[p] != v or not 0 <= inv < P or v*inv%P != 1: return False
        b.append((p,[(x*inv)%P for x in row]));ps.append(p);product=product*v%P
    if sorted(ps)!=list(range(n)): return False
    sign=(-1)**sum(ps[i]>ps[j] for i in range(n) for j in range(i+1,n))
    return cert.get('det')==product*sign%P

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('directory',type=pathlib.Path); args=parser.parse_args()
    d=args.directory
    metadata=json.loads((d/'metadata.json').read_bytes())
    names=('raw-matrix.json','reduced-matrix.json','certificate.json','odd-counts.json')
    blobs={n:(d/n).read_bytes() for n in names}
    if any(hashlib.sha256(blobs[n]).hexdigest()!=metadata['output_sha256'][n] for n in names): raise ValueError('output hash mismatch')
    raw,reduced,cert,counts=(json.loads(blobs[n]) for n in names)
    if len(raw)!=128 or len(reduced)!=128 or len(counts)!=128: raise ValueError('dimensions')
    for matrix in (raw,reduced):
        if any(len(r)!=128 or any(type(x) is not int or not 0<=x<P for x in r) for r in matrix): raise ValueError('matrix shape or value')
    if any(type(k) is not int or not 0<=k<=3 for k in counts): raise ValueError('odd count')
    for a,b,k in zip(raw,reduced,counts):
        if any(x != y*pow(626,k,P)%P for x,y in zip(a,b)): raise ValueError('normalization')
    rd=determinant(reduced); rawd=determinant(raw)
    if rd==0 or rd!=metadata['reduced_det'] or rawd!=metadata['raw_det'] or rawd!=rd*pow(626,sum(counts),P)%P: raise ValueError('determinant')
    if not verify_steps(reduced,cert) or cert['det']!=rd: raise ValueError('elimination certificate')
    print(json.dumps({'status':'success','reduced_det':rd},sort_keys=True))

if __name__ == '__main__': main()

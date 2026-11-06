"""Pack the pinned saved matrix and its verified inverse into Lean strings.
This is source generation only; it does not run Lean or the source selector.
"""
import hashlib,json,pathlib,argparse
parser=argparse.ArgumentParser();parser.add_argument('matrix',type=pathlib.Path);parser.add_argument('inverse',type=pathlib.Path);parser.add_argument('output',type=pathlib.Path);args=parser.parse_args()
a_bytes=args.matrix.read_bytes();b_bytes=args.inverse.read_bytes()
if hashlib.sha256(a_bytes).hexdigest()!='e63c1c1834b8db79d631fec2b375373a5948bcd4f1a57690f0cd3fed34981f46':raise ValueError('matrix mismatch')
if hashlib.sha256(b_bytes).hexdigest()!='ccb3155efc38c91eb206b75e07699628414cac0e97e41f4865a6a95c1d6c2588':raise ValueError('inverse mismatch')
a=json.loads(a_bytes);b=json.loads(b_bytes)
def pack(m):
 if len(m)!=128 or any(len(r)!=128 or any(type(x) is not int or not 0<=x<1009 for x in r) for r in m):raise ValueError('invalid matrix')
 return ''.join(f'{x:04d}' for row in m for x in row)
pa,pb=pack(a),pack(b)
if args.output.exists(): raise ValueError('output exists')
lean='''import Mathlib.Data.ZMod.Basic\nimport Mathlib.Data.Matrix.Mul\nimport Mathlib.Tactic\n\n/-! One-row candidate on packed saved numerical data. No source bridge. -/\nnamespace D0.Algebra.SavedFutureMatrixPacked\n\n'''
lean+='def dataA : ByteArray := ("'+pa+'" : String).toUTF8\n\n'
lean+='def dataB : ByteArray := ("'+pb+'" : String).toUTF8\n\n'
lean+='''def digit (xs : ByteArray) (k : Nat) : Nat := (xs.get! k).toNat - 48\n\ndef entry (xs : ByteArray) (i j : Fin 128) : ZMod 1009 :=\n  let k := 4 * (128 * i.val + j.val)\n  (1000 * digit xs k + 100 * digit xs (k + 1) +\n    10 * digit xs (k + 2) + digit xs (k + 3) : Nat)\n\ndef A : Matrix (Fin 128) (Fin 128) (ZMod 1009) := entry dataA\ndef B : Matrix (Fin 128) (Fin 128) (ZMod 1009) := entry dataB\n\n-- Resource-bounded candidate; no theorem until the pilot succeeds.\ntheorem first_row_right_inverse : ∀ j : Fin 128,\n    (A * B) 0 j = (1 : Matrix (Fin 128) (Fin 128) (ZMod 1009)) 0 j := by\n  native_decide\n\nend D0.Algebra.SavedFutureMatrixPacked\n\n#print axioms D0.Algebra.SavedFutureMatrixPacked.first_row_right_inverse\n'''
args.output.write_text(lean,encoding='utf-8',newline='')
print(json.dumps({'matrix_sha256':hashlib.sha256(a_bytes).hexdigest(),'inverse_sha256':hashlib.sha256(b_bytes).hexdigest(),'pilot_sha256':hashlib.sha256(lean.encode()).hexdigest(),'packed_bytes_each':len(pa),'scope':'candidate only, no Lean execution'}))

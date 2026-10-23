"""Local connector transport: the collar and unpadded centre are hash pinned.
Original CQ only uses the collar; the original padded centre is not used.
"""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).parent
def get_inputs():
 b=(ROOT/'rational_collar.json').read_bytes()
 if hashlib.sha256(b).hexdigest()!='b86d94a59f5b0ecfec55af3a6c0db80eec257d41b09f3a03c59e367f56093fa1':raise RuntimeError('collar mismatch')
 b2=(ROOT/'center_new.json').read_bytes()
 if hashlib.sha1(b'blob '+str(len(b2)).encode()+b'\0'+b2).hexdigest()!='6b520fbd6218444601d90d7e30b738f8c828bd22':raise RuntimeError('centre mismatch')
 return json.loads(b),json.loads(b2)

#!/usr/bin/env python3
"""Read-only local evidence verification, no expensive historic repository suite."""
import hashlib,json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
v=json.loads((P/'VALIDATION.json').read_text())
for fn,sha in v['sha256'].items():
    data=(P/fn).read_bytes()
    if hashlib.sha256(data).hexdigest()!=sha:raise ValueError('SHA '+fn)
outs=[]
for opt in (False,True):
    args=[sys.executable]+(['-O'] if opt else [])+[str(P/'check_moving_cut_book.py')]
    r=subprocess.run(args,check=True,capture_output=True)
    if r.stderr:raise ValueError('stderr in '+str(args))
    outs.append(r.stdout)
if outs[0]!=outs[1]:raise ValueError('optimized output differs')
if outs[0]!=(P/'RESULT.json').read_bytes():raise ValueError('saved result differs')
if outs[1]!=(P/'RESULT_OPTIMIZED.json').read_bytes():raise ValueError('optimized saved result differs')
parsed=json.loads(outs[0])
if parsed['check_count']!=v['normal']['check_count'] or parsed['status']!='PASS':
    raise ValueError('check counts')
print(json.dumps({'status':'PASS','normal_and_optimized_identical':True,'checks':parsed['check_count'],'GR_closed':False},sort_keys=True))

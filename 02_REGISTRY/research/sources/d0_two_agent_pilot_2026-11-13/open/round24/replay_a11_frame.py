#!/usr/bin/env python3
"""Replay A11 current-frame check without writing to the A11 directory."""
from pathlib import Path
import shutil,tempfile,subprocess,hashlib,json,os
p=Path(__file__).resolve().parent
a=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round11')
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory(dir=p,prefix='frame_review_') as d:
 d=Path(d);shutil.copy2(a/'check_current_frame.py',d/'check_current_frame.py')
 env=dict(os.environ,OPENBLAS_NUM_THREADS='1')
 res=subprocess.run(['python3','-B','-W','error',str(d/'check_current_frame.py'),str(p.parent/'round21')],capture_output=True,text=True,check=True,env=env)
 assert sha(d/'CURRENT_FRAME_CHECK.json')==sha(a/'CURRENT_FRAME_CHECK.json')
 out={'status':'ISOLATED_A11_FRAME_REPLAY_PASSED','source_sha256':sha(a/'check_current_frame.py'),'output_sha256':sha(d/'CURRENT_FRAME_CHECK.json'),'output':json.loads(res.stdout),'GR_closed':False}
(p/'A11_FRAME_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

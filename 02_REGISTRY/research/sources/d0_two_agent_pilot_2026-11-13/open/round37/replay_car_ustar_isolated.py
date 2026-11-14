#!/usr/bin/env python3
"""Rebuild the emitted Ustar in an isolated temporary working directory."""
from pathlib import Path
from hashlib import sha256
import shutil,tempfile,subprocess,json
P=Path(__file__).resolve().parent;source=P/'build_car_ustar.py';artifact=P/'CAR_USTAR_NATIVE.json';sha=lambda p:sha256(p.read_bytes()).hexdigest();before=sha(artifact);code=sha(source)
with tempfile.TemporaryDirectory(prefix='ustar-replay-',dir=P) as td:
 t=Path(td);shutil.copyfile(source,t/source.name)
 r=subprocess.run(['python3','-B','-W','error',source.name],cwd=t,text=True,capture_output=True,check=True)
 new=sha(t/artifact.name);assert new==before and sha(artifact)==before and sha(source)==code
out={'status':'PASS_ISOLATED_USTAR_REBUILD','builder_sha256':code,'CAR_USTAR_NATIVE_sha256':before,'rebuilt_artifact_byte_identical':True,'owner_libraries_read_only':True,'stdout':r.stdout.strip(),'huge_native_word_executed':False,'GR_closed':False}
(P/'CAR_USTAR_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

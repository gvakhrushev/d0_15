#!/usr/bin/env python3
"""Execute changes in the actual algebra, not mutations of expected receipts."""
from pathlib import Path
import tempfile,subprocess,sys,json
P=Path(__file__).resolve().parent
M=[
('lose_golden_weight','signal=2*p**3*(1+q)','signal=2*p**4*(1+q)','golden_effect','both_interference_outcomes'),
('drop_Lorentz_pairing','acc+=pairing(M,L*ETA)-pairing(M,L.inv()*ETA)',
 'acc+=pairing(M,L)-pairing(M,L.inv())','geometry','whole_signed_star_equals_overlap_accumulator'),
('price_before_aggregation','A=F(Qaction)','A=F(x*x)+F(2*y*y)+F(x*y)','response','full_source_x'),
('freeze_one_central_sector','tau*u+(1-tau)*v,v+tau*(u-v)','tau*u,v+tau*(u-v)',
 'response','block_weight_convex_coefficient'),
('make_terminal_flag_local','k=unit(t);jx=unit(x);jy=unit(y)','k=unit(x);jx=unit(x);jy=unit(y)',
 'preserved_geometry','retained_geometry_metric')]
def run():
    text=(P/'check_central_record.py').read_text();out=[]
    with tempfile.TemporaryDirectory(prefix='d0-central-mutants-') as d:
        root=Path(d);(root/'interval_sign.py').write_bytes((P/'interval_sign.py').read_bytes())
        for name,old,new,func,failed in M:
            if text.count(old)!=1:raise RuntimeError('Nonunique mutation '+name)
            f=root/(name+'.py');f.write_text(text.replace(old,new))
            script='import runpy; m=runpy.run_path('+repr(str(f))+');m['+repr(func)+']()'
            proc=subprocess.run([sys.executable,'-c',script],cwd=root,capture_output=True,text=True,timeout=20)
            if proc.returncode==0 or 'ArithmeticError: '+failed not in proc.stderr:
                raise RuntimeError('Unexpected mutation outcome '+name+'\n'+proc.stderr)
            out.append({'mutation':name,'failed_at':failed,'status':'REJECTED_BY_MATHEMATICS'})
    return {'mutations':out,'expected_files_changed':False}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))

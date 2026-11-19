#!/usr/bin/env python3
"""Executed mathematical mutations, without weakening immutable-parent pins."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
CHANGES=[
 ('lost_RR_history','words=[(x,y) for x in letters for y in letters]',
  'words=[(x,y) for x in letters for y in letters if x or y]','all_four_word_mass'),
 ('amplitude_as_probability','success=amplitudes[0]**2',
  'success=amplitudes[0]','success_is_determinant'),
 ('false_unitary_sign','U=C.row_join(-K).col_join(K.row_join(C))',
  'U=C.row_join(K).col_join(K.row_join(C))','full_eight_mode_unitarity'),
 ('frozen_raw_blank','blank=p4*raw','blank=p4*b0','complete_calibrated_source_value'),
 ('frozen_event_calibration','recovered=2*s0*contrast/(p4*ar*scale**2)',
  'recovered=2*s0*contrast/(p4*a0*scale**2)','complete_calibrated_source_value'),
 ('frozen_probe_scale','recovered=2*s0*contrast/(p4*ar*scale**2)',
  'recovered=2*s0*contrast/(p4*ar*x0**2)','complete_calibrated_source_value')
]


def run():
    original=(HERE/'check_golden_determinant.py').read_text()
    verdicts=[]
    with tempfile.TemporaryDirectory(prefix='d0-determinant-mutants-') as directory:
        for label,old,new,expected in CHANGES:
            if original.count(old)!=1:
                raise ValueError('mutation target not unique: '+label)
            path=Path(directory)/(label+'.py')
            path.write_text(original.replace(old,new))
            result=subprocess.run([sys.executable,str(path)],capture_output=True,
                                  text=True,timeout=90)
            if result.returncode==0 or ('ArithmeticError: '+expected) not in result.stderr:
                raise ArithmeticError('mutation not rejected mathematically: '+label+'\n'+result.stderr)
            verdicts.append({'mutation':label,'verdict':'REJECTED','failed_check':expected})
    return {'scope':'six actually changed programs; no scientific status promotion','mutations':verdicts}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))

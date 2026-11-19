#!/usr/bin/env python3
"""Execute actual changed mathematics; keep all committed expected data fixed."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
MUTATIONS=[
    ('wrong_signed_momentum_projector',
     '(F(sign,4),(v,))','(F(-sign,4),(v,))',
     'span_checks','central_projector_'),
    ('omit_odd_word_return',
     'tuple(j+1 for j in indices)+((0,) if len(indices)%2 else ())',
     'tuple(j+1 for j in indices)',
     'span_checks','full_shell_word_reconstruction_'),
    ('drop_Fock_dimension_from_CP_weight',
     "eq('normalized_conditional_depolarizing_weight',F(16,128),F(1,8))",
     "eq('normalized_conditional_depolarizing_weight',F(1,128),F(1,8))",
     'channel_checks','normalized_conditional_depolarizing_weight'),
    ('freeze_actual_preparation_response',
     'opt=-b*theta/c','opt=S.Integer(0)',
     'convex_checks','exact_preparation_response'),
]

def main():
    source=(HERE/'check_preparation_descent.py').read_text()
    outputs=[]
    with tempfile.TemporaryDirectory(prefix='d0-complete-preparation-mutants-') as temp:
        for name,old,new,function,expected in MUTATIONS:
            if source.count(old)!=1:
                raise ValueError('Nonunique mutation target: '+name)
            file=Path(temp)/(name+'.py')
            file.write_text(source.replace(old,new))
            driver='import runpy; m=runpy.run_path('+repr(str(file))+'); m['+repr(function)+']()'
            proc=subprocess.run([sys.executable,'-c',driver],text=True,capture_output=True,timeout=30)
            if proc.returncode==0 or ('ArithmeticError: '+expected) not in proc.stderr:
                raise ArithmeticError('Unexpected mutation result: '+name+'\n'+proc.stderr)
            label=proc.stderr.rsplit('ArithmeticError: ',1)[1].strip().splitlines()[0]
            outputs.append({'mutation':name,'failed_check':label,'status':'REJECTED_MATHEMATICALLY'})
    return {'schema':'d0-complete-preparation-descent-mutations/1','mutations':outputs,
            'expected_results_modified':False}

if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))

#!/usr/bin/env python3
"""Execute formula mutations; no fixture or expected-result tampering."""
from pathlib import Path
import json, subprocess, sys, tempfile
HERE=Path(__file__).resolve().parent
M=[
 ('freeze_embedding','X = S.Matrix([y[0]-t*(y[1]**2+y[1]*y[2]), y[1], y[2], y[3]])','X = y','pullback','opposite_embedding_restores_every_point'),
 ('omit_connection_oneform_jacobian','Op=[sum((substitute(Om[a],x,f)*Jf[a,r] for a in range(4)),S.zeros(4)) for r in range(4)]','Op=[substitute(Om[r],x,f) for r in range(4)]','pullback','ordered_path_generator_1'),
 ('freeze_retained_response','reduced=Hgg-Hgz*Hzz.inv()*Hgz.T','reduced=Hgg','ward_and_schur','same_action_reduced_Hessian'),
 ('omit_offshell_acceleration','(vel.T*hess*vel)[0]+(grad.T*acc)[0],0','(vel.T*hess*vel)[0],0','ward_and_schur','off_shell_second_Ward_includes_acceleration'),
 ('wrong_metric_relative_sign','normalized=E.subs({a:1,b:-1,c:1,d:1,e:-1})','normalized=E.subs({a:1,b:1,c:1,d:1,e:-1})','metric_selector','selected_operator_annihilates_all_coordinate_velocities'),
 ('omit_true_clock_Euler','-2*div+clock_source*grad,S.zeros(4,1)','-2*div,S.zeros(4,1)','clock_ward','full_clock_metric_Noether_identity')]
def run():
    text=(HERE/'check_relational_ward.py').read_text();out=[]
    with tempfile.TemporaryDirectory(prefix='d0-relational-mutants-') as directory:
        for name,old,new,function,expected in M:
            if text.count(old)!=1:raise ValueError('Nonunique target '+name)
            p=Path(directory)/(name+'.py');p.write_text(text.replace(old,new))
            code='import runpy; ns=runpy.run_path('+repr(str(p))+'); ns['+repr(function)+']()'
            proc=subprocess.run([sys.executable,'-c',code],capture_output=True,text=True,timeout=35)
            if proc.returncode==0 or ('ArithmeticError: '+expected) not in proc.stderr:
                raise ArithmeticError('Wrong mutation outcome '+name+'\n'+proc.stderr)
            out.append({'mutation':name,'failed_check':expected,'status':'REJECTED_BY_MATHEMATICS'})
    return {'mutations':out,'expected_output_modified':False}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))

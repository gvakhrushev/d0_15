#!/usr/bin/env python3
"""Actual four-valued coframe/CAR target sectors on the original chart."""
from pathlib import Path
from itertools import product
from collections import Counter
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P.parent;M=2688;STRIDE_BITS=80
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
cf=load('a48_old_cf_targets',D/'round20/coframe_targets.py')
mat=cf.old;loc=cf.loc;Dyadic=mat.Dyadic


def code_indices(coordinates):return [q for j in coordinates for q in (j,M+j)]
def code_pattern(digits):return [q for j in digits for q in (j&1,j>>1)]


def field_increment(iv,c,digit):
    assert type(digit) is int and 0<=digit<4
    return iv.mul(iv.rational(1,1<<STRIDE_BITS),iv.sub(iv.rational(digit),iv.mul(iv.rational(3),iv.pow(c['p'],2))))


def coframe_templates():
    out={}
    for bank,rows in loc.catalogue().items():
        out[bank]=[{'bank':bank,'address':r['a'],'site':r['site'],'direction':r['direction'],
          'coordinates':r['SAM_indices']} for r in rows if r['kind']=='inverse_coframe_column']
    return out


def coframe_spec(row,digits):
    assert len(digits)==len(row['coordinates'])
    if row['bank'] in ('f','q'):
        role=row['direction'];x=row['site'];digits=None if not row['coordinates'] else list(digits)
        spec={'family':'current','role':role,'x2':x[2] if role==1 else 0,'x3':x[3] if role==1 else 0,'digits':digits}
        name='c_'+str(role)+'_'+str(spec['x2'])+str(spec['x3'])+'_'+('fixed' if digits is None else ''.join(map(str,digits)))
    else:
        spec={'family':'reference','role':row['direction'],'PF_count':cf.PF_BY_SITE[tuple(row['site'])]['N']}
        name='r_'+str(spec['role'])+'_'+str(spec['PF_count'])
    return name,spec


def coframe_sectors(templates,bank):
    for row in templates[bank]:
        for digits in product(range(4),repeat=len(row['coordinates'])):
            name,_=coframe_spec(row,digits)
            yield {'address':row['address'],'SAM_indices':code_indices(row['coordinates']),
              'SAM_pattern':code_pattern(digits),'family_id':name}


def coframe_catalogue():
    templates=coframe_templates();specs={};multiplicity={}
    for bank,rows in templates.items():
        hist=Counter()
        for row in rows:
            for digits in product(range(4),repeat=len(row['coordinates'])):
                name,spec=coframe_spec(row,digits)
                assert name not in specs or specs[name]==spec
                specs[name]=spec;hist[name]+=1
        multiplicity[bank]=hist
    return specs,templates,multiplicity


def coframe_vector(iv,c,spec):
    original=dict(spec)
    if original['family']=='current':
        original.pop('digits');original['bits']=None
    vector=cf.vector(iv,c,original)
    if spec['family']=='current' and spec['digits'] is not None:
        assert len(spec['digits'])==4
        vector=[iv.add(v,field_increment(iv,c,d)) for v,d in zip(vector,spec['digits'])]
    return vector


def material_specs():
    specs=[]
    for x0 in range(4):
        specs.append({'id':f'q{x0}_fixed','kind':'q','x0':x0,'digits':None})
        for digits in product(range(4),repeat=2):
            specs.append({'id':f'q{x0}_{digits[0]}{digits[1]}','kind':'q','x0':x0,'digits':list(digits)})
    specs.extend([{'id':'y_positive','kind':'y','sign':1},{'id':'y_negative','kind':'y','sign':-1}])
    assert len(specs)==70
    return specs


def material_half_vector(iv,c,spec):
    original=dict(spec)
    if original['kind']=='q':original.pop('digits');original['bits']=None
    _,psi=mat.half_vector(iv,c,original)
    if spec['kind']=='q' and spec['digits'] is not None:
        psi=[iv.add(v,field_increment(iv,c,d)) for v,d in zip(psi,spec['digits'])]
    R=iv.rational;one=R(1);a=c['sqrtp']
    slack=iv.sub(iv.sub(one,c['p']),iv.add(iv.pow(psi[0],2),iv.pow(psi[1],2)))
    assert slack[0]>iv.scale//3
    den=iv.sqrt(iv.mul(R(2),iv.add(one,a)))
    v={1:iv.div(iv.add(one,a),den),14:iv.div(iv.sqrt(slack),den),0:iv.div(psi[0],den),15:iv.div(psi[1],den)}
    return v,psi


def material_catalogue():
    original=mat.catalogue();out={'q':[],'y+':original['y+'],'y-':original['y-']};seen=set()
    for row in original['q']:
        if not row['SAM_indices']:out['q'].append(row);continue
        if row['site'] in seen:continue
        seen.add(row['site']);x0=row['site_coordinates'][0]
        for digits in product(range(4),repeat=2):
            out['q'].append({'site':row['site'],'site_coordinates':row['site_coordinates'],
              'SAM_indices':code_indices(row['SAM_indices']),'SAM_pattern':code_pattern(digits),
              'vector_id':f'q{x0}_{digits[0]}{digits[1]}'})
    assert len(out['q'])==1216 and len(seen)==64
    return out

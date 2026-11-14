#!/usr/bin/env python3
"""Outward exact names of the original B25 coframe Julia planar factors."""
from pathlib import Path
from itertools import product
import importlib.util,json,sys
P=Path(__file__).resolve().parent;D=P.parent
def load(name,path):
    sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m
old=load('a20_dyadic',D/'round18/material_targets.py');Dyadic=old.Dyadic
loc=load('a20_locality',D/'round19/julia_locality.py')
fact=load('a20_factors',D/'round19/coframe_factorization.py')
PF_PATH=loc.B/'round21/ORIGINAL_PF_N20_L4.jsonl'
PF=[json.loads(x) for x in PF_PATH.read_text().splitlines()];PF_BY_SITE={tuple(r['site']):r for r in PF}
def specification(bank,row):
    assert row['kind']=='inverse_coframe_column'
    if bank in ('f','q'):
        role=row['direction'];x=row['site'];bits=row['SAM_pattern'] if row['SAM_indices'] else None
        spec={'family':'current','role':role,'x2':x[2] if role==1 else 0,'x3':x[3] if role==1 else 0,'bits':bits}
        name='c_'+str(role)+'_'+str(spec['x2'])+str(spec['x3'])+'_'+('fixed' if bits is None else ''.join(str(b) for b in bits))
    else:
        spec={'family':'reference','role':row['direction'],'PF_count':PF_BY_SITE[tuple(row['site'])]['N']}
        name='r_'+str(spec['role'])+'_'+str(spec['PF_count'])
    return name,spec
def catalogue():
    specs={};banks={}
    for bank,rows in loc.catalogue().items():
        out=[]
        for row in loc.sectors(rows):
            if row['kind']!='inverse_coframe_column':continue
            name,spec=specification(bank,row)
            assert name not in specs or specs[name]==spec
            specs[name]=spec
            out.append({'address':row['a'],'SAM_indices':row['SAM_indices'],'SAM_pattern':row['SAM_pattern'],'family_id':name})
        banks[bank]=out
    assert len(specs)==247 and sum(map(len,banks.values()))==14848
    return specs,banks
def square(iv,v):
    a,b=v;low=0 if a<=0<=b else min(a*a,b*b);high=max(a*a,b*b)
    return low//iv.scale,-((-high)//iv.scale)
def add_all(iv,terms):
    out=(0,0)
    for x in terms:out=iv.add(out,x)
    return out
def constants(iv):
    c=old.constants(iv);c['pi']=iv.pi();return c
def vector(iv,c,spec):
    R=iv.rational;role=spec['role'];v=[R(0) for _ in range(4)]
    if spec['family']=='current':
        nu=R(3,5)
        if role==1:
            xx,yy=spec['x2'],spec['x3']
            H=iv.add(iv.mul(iv.mul(c['k0'],square(iv,c['pi'])),R(xx*xx+yy*yy,40000)),R(3*(xx*xx-yy*yy),1600))
            v[0]=nu;v[1]=iv.neg(iv.div(iv.mul(nu,H),R(2)))
        else:v[{0:1,2:2,3:3}[role]]=nu
        if spec['bits'] is not None:
            for j,b in enumerate(spec['bits']):v[j]=iv.add(v[j],iv.mul(R(1,2**30),iv.sub(R(b),square(iv,c['p']))))
    else:
        norm=iv.div(iv.sqrt(R(256*spec['PF_count'],10946)),R(10))
        if role in (0,1):
            a=iv.div(norm,iv.sqrt(R(2)));v[0]=a if role==0 else iv.neg(a);v[1]=a
        else:v[role]=iv.neg(norm) if role==2 else norm
    return v
def factors(iv,v,spec):
    S=iv.scale;R=iv.rational;n2=add_all(iv,(square(iv,x) for x in v));n=iv.sqrt(n2)
    assert n[0]>0 and n[1]<S
    role=spec['role'];dominant=({0:1,1:0,2:2,3:3}[role] if spec['family']=='current' else {0:0,1:0,2:2,3:3}[role])
    first=dominant if dominant else 1;order=[first]+[j for j in (1,2,3) if j!=first]
    cur=list(v);eliminate=[]
    for j in order:
        radius=iv.sqrt(iv.add(square(iv,cur[0]),square(iv,cur[j])))
        # Strict interval check, no floating dominant selection or threshold.
        assert 2*radius[0]>=n[1],(spec,j,'unproved denominator bound')
        cc=iv.div(cur[0],radius);ss=iv.div(cur[j],radius)
        identity=cur[j]==(0,0) and cur[0][0]>0
        if identity:assert cc[0]<=S<=cc[1]
        eliminate.append({'mode':j,'cos':cc,'sin':ss,'exact_identity':identity,'radius':radius})
        cur[0]=radius;cur[j]=R(0)
    d=iv.sqrt(iv.sub(R(1),n2))
    return {'norm':n,'norm_squared':n2,'mode_rotations':list(reversed(eliminate)),
            'base_native_cos':d,'base_native_sin':n,'chosen_elimination_order':order}
def clip_unit(iv,value):
    out=max(-iv.scale,value[0]),min(iv.scale,value[1]);assert out[0]<=out[1];return out
def native_angle_targets(iv,factors):
    # Every occupation pair has source pivot bit1, so negate its desired sine.
    for index,rotation in enumerate(factors['mode_rotations']):
        if rotation['exact_identity']:continue
        signs=sorted({sign for _,_,sign in fact.fock_pairs(rotation['mode'])})
        for sign in signs:
            si=rotation['sin'] if sign==-1 else iv.neg(rotation['sin'])
            yield ('mode',index,sign),clip_unit(iv,rotation['cos']),clip_unit(iv,si)
    yield ('base',0,0),clip_unit(iv,factors['base_native_cos']),clip_unit(iv,factors['base_native_sin'])

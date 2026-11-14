#!/usr/bin/env python3
"""Emit concrete fixed phases and symbolic paid-recursion DAG for adapter."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
import json
import adapter_native as a
P=Path(__file__).resolve().parent;cert=json.loads((P/'ADAPTER_PHASE_CERTIFICATE.json').read_text());ph=int(cert['phase_k']);cor=int(cert['correction_l']);hk=int(json.loads((a.D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())['k'])
lay=a.layout(w=0,external_count=2703);SAM=lay['external'][:2688];site=lay['external'][2688:2696];right=lay['external'][2696:2703];assert len(SAM)==2688 and len(site)==8 and len(right)==7
fixed=a.fixed(lay,ph,cor,hk);N=len(lay['start_controls']);L=len(fixed['Flogical']);F=a.nb.seq(*fixed['start'][:L]);flagphase=fixed['start'][L];Fi=a.nb.seq(*fixed['start'][L+1:]);assert Fi==a.nb.inverse_literal(F,lay['port'],tuple(lay['spin']))
parts={'H':fixed['H'],'good_branch0_phase':fixed['good'][0],'start_compute_F':F,'start_flag1_phase':flagphase,'start_compute_literal_inverse':Fi,'final_rebit_correction':fixed['correction']}
for name,tree in parts.items():
 a.nb.validate_schema(tree,lay['qubits'],lay['port'],tuple(lay['spin']),(lay['oldRIGHT_witness'],))
 for leaf in a.nb.leaves(tree):assert not set(leaf['wires']).intersection(site+right+SAM)
counts={name:a.native_counts(tree,lay['port']) for name,tree in parts.items()}
assert counts['good_branch0_phase']=={'G_other':2*ph,'CX':2}
assert counts['start_flag1_phase']=={'G_port':ph,'G_other':ph,'CX':8,'SourceI':4}
assert counts['final_rebit_correction']=={'G_other':cor}
assert counts['start_compute_literal_inverse']==a.raw_inverse_counts(counts['start_compute_F'])
assert len(fixed['Flogical'])==90 and N==23
# Deliberately distinct fresh RAW v -> zero for branch, rebit and F flag/work.
zero_wires=[lay['branch'],lay['rebit'],lay['predicate_flag']]+lay['predicate_work'];assert len(zero_wires)==N+1==24
zeros=[a.nb.rotation_power(q,-1,lay['port'],tuple(lay['spin'])) for q in zero_wires]
zc=sum((a.native_counts(z,lay['port']) for z in zeros),a.Counter());assert zc=={'G_port':24,'CX':144,'SourceI':96}
# Actual raw-inverse accounting is linear in the unknown native controlled V.
axes=('G_port','G_other','CX','SourceI');base,inv=a.native_budget(0,ph,cor,hk);coeff={}
for axis in axes:
 c,_=a.native_budget(0,ph,cor,hk,{axis:1});coeff[axis]={k:str(c[k]-base[k]) for k in axes}
assert all(int(v)>=0 for column in coeff.values() for v in column.values())
# Conditional mathematical error for w<=32768, δV<=2^-3250.
Nmax=23+32768;delta=Fraction(1,2**4096);dv=Fraction(1,2**3250)
err=Fraction(1,2**3280)+6561*dv+(13122+13120*Nmax+1)*delta
assert err<Fraction(1,2**3230)
out={'status':'CONCRETE_NATIVE_PHASES_AND_CONDITIONAL_ADAPTER_GRAMMAR','layout':lay,'SAM_wires':SAM,'internal_SITE_spectators':site,'RIGHT_spectators':right,'phase_certificate_sha256':sha256((P/'ADAPTER_PHASE_CERTIFICATE.json').read_bytes()).hexdigest(),'source_sha256':sha256((P/'adapter_native.py').read_bytes()).hexdigest(),
 'fixed_native_DAGs':parts,'fixed_forward_inventories':{name:{axis:str(c[axis]) for axis in axes} for name,c in counts.items()},'RAW_v_to_zero_grammar':zeros,'new_RAW_v_wires':zero_wires,'RAW_v_zero_inventory':{axis:str(zc[axis]) for axis in axes},
 'recursion':{'A0':['H','CONTROLLED_OMEGA_LOADER','H'],'A_next_chronology':['A_prev','good_branch0_phase','literal_raw_inverse(A_prev)','start_compute_F;start_flag1_phase;start_compute_literal_inverse','A_prev'],'levels':8,'after_A8':'final_rebit_correction','literal_inverse_rule':'reverse complete actual sequence and inverse every G/CX/SourceI leaf; inverse-of-inverse is NOT syntactically cancelled'},
 'unknown_loader_resource_axes':list(axes),'forward_inventory_constant_when_CV_cost_zero':{k:str(base[k]) for k in axes},'literal_inverse_inventory_constant_when_CV_cost_zero':{k:str(inv[k]) for k in axes},'controlled_loader_forward_inventory_coefficients':coeff,
 'missing_operator':'actual branch-controlled SAM-controlled Omega loader, exactly idle on branch0, clean V-private anchor, phase rebit and comparator untouched, uniform anchor-isometry error <=2^-3250, with literal primitive inverse',
 'isometry_error_lt':'2^-3230 if 0<=private_w<=32768 and missing contract holds','ideal_failure_lt':'2^-6561','no_failure_discarded':True,'full_native_program_not_bound_or_executed':True,'physical_C_closed':False,'GR_closed':False}
(P/'ADAPTER_NATIVE_GRAMMAR.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
print(json.dumps({'status':out['status'],'predicate_controls':N,'predicate_gates':L,'new_RAW_v_zero_wires':len(zero_wires),'levels':8,'isometry_error_lt':out['isometry_error_lt'],'requires_controlled_loader':True}))

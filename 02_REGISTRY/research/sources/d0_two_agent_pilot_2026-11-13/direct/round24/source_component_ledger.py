#!/usr/bin/env python3
"""Known prepared-source components; deliberately not a full H.1 receipt."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib,importlib.util,json,sys
import full_car_source as car
P=Path(__file__).resolve().parent;D=P.parent
sys.path.insert(0,str(D/'round22'))
import full_choi_bank as choi
B=car.v.B
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m);return m
site=load('a24_site',B/'round45/site_native.py')
def upper_power(e):
    assert e>0
    n=e.denominator.bit_length()-e.numerator.bit_length()
    while e>=Fraction(1,2**n):n-=1
    while e<Fraction(1,2**(n+1)):n+=1
    return n
def encoded(e):return {'numerator_hex':hex(e.numerator),'denominator_hex':hex(e.denominator),'strict_upper_bound':'2^-'+str(upper_power(e))}
def main():
    axes=('G_port','G_other','CX','SourceI');banks=('y+','y-','f','0','x+','x-','q');native=Counter();ch=Counter();ca=Counter()
    for bank in banks:
        ch.update({q:180*v for q,v in choi.inventory(bank)['RAW_prepared_forward'].items()})
        ca.update({q:16*v for q,v in car.inventory(bank)['source_forward'].items()})
    native.update(ch);native.update(ca)
    site_counts=site.inventory(site.library());site_error=18*Fraction(1,2**3264)
    choi_error=1260*choi.errors()[2];car_error=sum((16*car.error_bound(bank) for bank in banks),Fraction())
    report=json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text());report_error=int(report['seven_report_all_known_approximate_macros'])*Fraction(1,2**4096)
    assert report['prepared_Choi_copies']==180 and report['prepared_CAR_copies_with_RIGHT']==16
    known=choi_error+car_error+report_error
    fresh={'Choi_DATA':1260*22,'Choi_private':1260*24,'CAR_source':112*19,'CAR_predicate':112*3}
    assert sum(fresh.values())==60424
    h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    pins=[Path(__file__),D/'round22/FULL_CHOI_BANK_PLAN.json',P/'FULL_CAR_SOURCE_PLAN.json',D/'round17/GLOBAL_REPORT_COMPILATION.json',B/'round45/SITE_NATIVE_PLAN.json']
    out={'status':'EXACT_KNOWN_SOURCE_COMPONENT_LEDGER_NOT_COMPLETE_H1','source_sha256':{str(p):h(p) for p in pins},
         'declared_preparation_occurrences':{'Choi_per_bank':180,'CAR_per_bank':16,'banks':list(banks)},
         'native_source_forward_totals':{name:{q:str(v[q]) for q in axes} for name,v in [('Choi1260',ch),('CAR112',ca),('all_sources',native)]},
         'literal_reverse_of_all_source_preparations':{q:str(v) for q,v in car.v.inverse_price(native).items()},
         'source_RAW_births_only':fresh,'source_RAW_births_sum':sum(fresh.values()),
         'separate_shared_SITE_RAW_inputs':8,'separate_report_processor_RAW_for_seven':7*report['fresh_RAW_v_births_for_processor_and_fair'],
         'SITE_native_prepare':{q:str(site_counts['SITE_forward'][q]) for q in axes},'SITE_native_literal_unprepare':{q:str(site_counts['SITE_literal_inverse'][q]) for q in axes},
         'exact_error_components':{'Choi1260':encoded(choi_error),'CAR112':encoded(car_error),'one_SITE_occurrence':encoded(site_error),'A17_seven_reports_known_only':encoded(report_error)},
         'conditional_known_sum_with_one_SITE_occurrence':encoded(known+site_error),
         'conditional_known_sum_with_two_SITE_occurrences':encoded(known+2*site_error),
         'SITE_occurrences_in_complete_forward_A_not_assumed':True,
         'not_a_bound_for_complete_eta_A':True,'not_a_total_birth_or_clock_count':True,
         'requirements':['One admitted same-fibre schedule with exactly these source occurrences','All other forward/internal inverse/comparator/marks/reader/transport occurrences explicitly included','Canonical product RAW source births conditional on shared SAM and one SITE','Actual protected-factor scalar T6 or an independently applicable theorem','Original marked vacuum extension and full Book03/source binding'],
         'alpha_target_ge_half_proved':False,'physical_C_closed':False,'GR_closed':False}
    (P/'SOURCE_COMPONENT_LEDGER.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'source_RAW_inputs':sum(fresh.values()),'conditional_known_sum_with_two_SITE':out['conditional_known_sum_with_two_SITE_occurrences']['strict_upper_bound']}))
if __name__=='__main__':main()

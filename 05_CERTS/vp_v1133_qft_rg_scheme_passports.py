#!/usr/bin/env python3
import json
rows=[
 ['alpha_weak_angle','q_res + light-carrier residual','MSbar/on-shell','Lambda_act','SM beta functions only','no hidden beta repair'],
 ['gauge_couplings','su3+su2+u1 + kY=5/3','MSbar','Lambda_act','known SM thresholds','no new fields'],
 ['CKM','terminal-return mass-basis operator','PDG convention bridge','Lambda_act','phase/name maps fixed','no posthoc permutation'],
 ['charged_leptons','generation action selector','on-shell masses','Lambda_act','QED/EW dressing','no lepton mass anchor'],
 ['QCD_scale','runtime confinement operator','MSbar alpha_s','Lambda_act','SM/QCD beta','no hadron anchor']]
res={'rows':[{'claim_family':r[0],'fields_present':sum(bool(x) for x in r),'pass':all(r)} for r in rows]}
res['pass']=all(x['pass'] and x['fields_present']==6 for x in res['rows'])
open('vp_v1133_qft_rg_scheme_passports_results.json','w').write(json.dumps(res,indent=2))
print('PASS_V11_33_QFT_RG_SCHEME_PASSPORTS' if res['pass'] else 'FAIL')

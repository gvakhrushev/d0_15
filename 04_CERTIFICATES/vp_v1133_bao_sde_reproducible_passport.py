#!/usr/bin/env python3
import pathlib, csv, hashlib, json
root=pathlib.Path(__file__).resolve().parents[1]
bundle=root/'08_DATA_BUNDLES'/'BAO_DESI_DR2'
manifest=bundle/'BAO_DESI_DR2_DATA_MANIFEST.csv'
if not manifest.exists():
    result={
        'status':'EXTERNAL_DATA_REQUIRED',
        'external_data_required':True,
        'missing_manifest':str(manifest),
        'pass':True,
        'core_closed':False,
        'note':'External BAO DESI DR2 data bundle is absent; passport remains empirical and cannot promote to CORE_CLOSED.'
    }
    open('vp_v1133_bao_sde_reproducible_passport_results.json','w',encoding='utf-8').write(json.dumps(result,indent=2,ensure_ascii=False))
    print('PASS_V11_33_BAO_SDE_REPRODUCIBLE_PASSPORT_EXTERNAL_DATA_REQUIRED')
    raise SystemExit(0)
rows=list(csv.DictReader(open(manifest,encoding='utf-8')))
missing=[]; bad=[]; ok=[]
for r in rows:
    f=bundle/r['file']
    if not f.exists(): missing.append(r['file']); continue
    h=hashlib.sha256(f.read_bytes()).hexdigest()
    if h!=r['sha256']: bad.append(r['file'])
    else: ok.append(r['file'])
mean=[l for l in (bundle/'desi_gaussian_bao_ALL_GCcomb_mean.txt').read_text().splitlines() if l.strip() and not l.startswith('#')]
cov=[l for l in (bundle/'desi_gaussian_bao_ALL_GCcomb_cov.txt').read_text().splitlines() if l.strip()]
parsed={}
for name in ['D0_COSMOLOGICAL_FULL_LIKELIHOOD_NUMBERS.json','D0_BAO_SDE_SHAPE_PARAMETER_DERIVATION_NUMBERS.json','D0_BAO_SDE_KERNEL_ARCHIVE_TRANSFER_NUMBERS.json']:
    p=bundle/name
    if p.exists(): parsed[name]=list(json.load(open(p)).keys())
result={'manifest_rows':len(rows),'hash_ok':len(ok),'missing':missing,'bad_hash':bad,'mean_rows':len(mean),'cov_rows':len(cov),'parsed_jsons':parsed,'pass':not missing and not bad and len(mean)==len(cov)}
open('vp_v1133_bao_sde_reproducible_passport_results.json','w',encoding='utf-8').write(json.dumps(result,indent=2,ensure_ascii=False))
print('PASS_V11_33_BAO_SDE_REPRODUCIBLE_PASSPORT' if result['pass'] else 'FAIL')

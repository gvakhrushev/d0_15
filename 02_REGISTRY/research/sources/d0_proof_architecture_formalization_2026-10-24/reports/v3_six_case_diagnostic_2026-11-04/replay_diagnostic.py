import hashlib,json,pathlib,sys,time,subprocess
root=pathlib.Path.cwd();sys.path.insert(0,str(root))
from tools import proof_architecture as p, proof_architecture_cold_start as c, proof_architecture_cold_start_v3 as v
old=json.loads(pathlib.Path('/tmp/d0_pr402_cold_start_2026-11-04_2bc79af4a_summary.json').read_text())
index={'labelled-native-raising-inverse':[0], 'finite-hermitian-adjoint-twisted-car-application':[2,3,6,10], 'native-stationary-recording-seed-whole-word-source':[1], 'archive-preserving-binary-seed-full-query-source':[2], 'canonical-af-native16-retained-report-fibre':[1], 'pr334-native-af-paid-futures-and-full-price-separation':[4,5]}
fixtures={x['id']:x for x in c.CASES}; previous={x['id']:x for x in old['cases']};jobs=[(cid,i,fixtures[cid]['queries'][i]) for cid,indices in index.items() for i in indices]
start=time.monotonic();output=pathlib.Path('/tmp/d0_v3_six_case_bracketed.json');progress=pathlib.Path('/tmp/d0_v3_six_case_bracketed_provisional.json')
if output.exists():raise RuntimeError('output already exists')
before=p.load_dataset(root)
if before['worktree_dirty'] or before['snapshot_commit']!='3b8cb99fd5f004a83d4def1e1d439fe77d0193c7':raise RuntimeError('not the requested clean head')
corpus_before=v.corpus_snapshot(root);allowed=set(v.corpus_paths(root)); print('before',json.dumps(corpus_before),flush=True)
hits_by_query=p.full_text_search_many(root,[q for _,_,q in jobs],v.RANK_SIZE,ranked_pages=v.RANK_PAGES); print('search_sec',round(time.monotonic()-start,2),flush=True)
if len(hits_by_query)!=len(jobs):raise RuntimeError('incomplete query results')
results=[]
for completed,((cid,i,q),hits) in enumerate(zip(jobs,hits_by_query),1):
 qstart=time.monotonic();pages=v.source_pages(root,q,hits); result={'query':q,'ranked_pages':v._ranked_pages(hits),'source_pages':pages};combined=v.verified_query(root,q,result,allowed)
 targets=[r for r in previous[cid]['required_sources'].values() if not r['found'] and (not r['scoped_queries'] or any(x['query_index']==i for x in r['scoped_queries']))]
 for item in targets:
  req={'path':item['path'],'commit':item['expected_commit'],'blob':item['expected_blob']};status=c._required_source_status([(q,combined)],req)
  row={'case':cid,'original_query_index':i,'source':item['path'],'previous_status':item['status'],'matching_returned_evidence':status['found'],'status':'evidence_verified_discovery_unattested' if status['found'] else status['status'],'candidate_stage':status['candidate_stage'],'candidate_rank':status['candidate_rank'],'candidate_locator_source':status['candidate_locator_source'],'candidate_page_number':status['candidate_page_number'],'evidence_lines':status['evidence_lines'][:2], 'expected_commit':req['commit'],'expected_blob':req['blob']}
  results.append(row);print(json.dumps({k:row[k] for k in ['case','original_query_index','source','matching_returned_evidence','status','candidate_stage','candidate_rank','candidate_page_number']},ensure_ascii=False),flush=True)
 progress.write_text(json.dumps({'snapshot_validation':'PENDING_DO_NOT_USE','query_count_completed':completed,'results':results},ensure_ascii=False,indent=2)+'\n')
 print('done_query',cid,i,'ranked',len(hits),'pages',len(pages),'sec',round(time.monotonic()-qstart,2),flush=True)
after=p.load_dataset(root); corpus_after=v.corpus_snapshot(root)
for key in ('snapshot_commit','worktree_dirty','source_digests'):
 if before[key]!=after[key]:raise RuntimeError('checkout changed during diagnostic: '+key)
if corpus_before!=corpus_after:raise RuntimeError('corpus changed during diagnostic')
data={'snapshot_commit':before['snapshot_commit'],'worktree_dirty':before['worktree_dirty'],'authority_source_digests':before['source_digests'],'corpus_snapshot_before':corpus_before,'corpus_snapshot_after':corpus_after,'snapshot_validation':'consistent_at_two_points','discovery_validation':'unattested','scope':'10 selected queries for prior six failed cases; only previously missing sources are checked','query_count':len(jobs),'seconds':round(time.monotonic()-start,2),'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'results':results}
with output.open('x',encoding='utf-8') as stream:json.dump(data,stream,ensure_ascii=False,indent=2);stream.write('\n')
print('complete',len(results),'sec',data['seconds'],flush=True)

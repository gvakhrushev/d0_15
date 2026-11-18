#!/usr/bin/env python3
"""Separate ideal REPORT1, native error, and global READY semantics."""
from pathlib import Path
from itertools import product
import json
import check_native_ready_exact as exact
a=exact.a
# post_label=0, post_READY=1, report=2, native port=3/spin=4,5/aux=6
p={'native_port':3,'native_spin':[4,5],'native_aux_arbitrary':6}
word=[]
for logical in [('CX',1,2),('CCX',1,0,2)]:
 tree=a.lower_gate(p,1,logical)
 for gate in a.s.nb.expand(tree,20000):word.append((gate['op'],*gate['wires']))
# Ideal XOR report update, including arbitrary old report target.
for label,ready,old in product((0,1),repeat=3):
 x=label|(ready<<1)|(old<<2);y=a.s.logic.apply_word([('CX',1,2),('CCX',1,0,2)],x)
 assert y==x^((ready*(1-label))<<2)
# Even when global all_READY (separate wire) is zero, ideal REPORT1 can be 1.
assert a.s.logic.apply_word([('CX',1,2),('CCX',1,0,2)],2)==6
# With post_READY=0, both native primitive blocks are exactly inactive for
# arbitrary label/port/Spin/aux. Report target starts 0.
for label,ext in product((0,1),range(16)):
 initial=label|(ext<<3);assert exact.run(word,initial)=={initial:exact.one}
# At k=1, true-ready label1 should yield report0 ideally, but the approximate
# CCX implementation leaves a nonzero report1 component. This is not a
# counterexample to the certified huge-k error bound; it clarifies exact scope.
failed=exact.run(word,3);wrong={x:c for x,c in failed.items() if (x>>2)&1 and c!=exact.zero};assert wrong
out={'status':'PASS_REPORT_EXTRACTION_IDEAL_VS_NATIVE_BOUNDARY','ideal_report_is_post_READY_and_not_label':True,'ideal_REPORT1_does_not_imply_global_all_READY':True,'acceptance_must_jointly_require_global_all_READY':True,'native_post_READY_zero_exactly_inactive_columns':32,'native_k1_ready1_label1_has_nonzero_wrong_report_component':True,'scope':'k1 exact diagnostic, not actual huge-k norm estimate; actual imperfection belongs to A14 all-column error budget','GR_closed':False}
Path(__file__).with_name('REPORT_EXTRACTION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

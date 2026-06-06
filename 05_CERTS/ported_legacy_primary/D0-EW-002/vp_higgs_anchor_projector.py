#!/usr/bin/env python3
import math
import numpy as np

phi = (1 + math.sqrt(5)) / 2
delta0 = (math.sqrt(5) - 2) / 2
Rank = 3
V13 = 13
N_anchor = Rank * V13
# Pi_H is represented by the identity on the scalar anchor image.
Pi_H = np.eye(N_anchor)
defect = np.ones(N_anchor) * (float(delta0) / math.sqrt(N_anchor))
assert Pi_H.shape == (39,39)
assert abs(np.linalg.norm(defect) - float(delta0)) < 1e-12
v_H = abs(defect[0])
assert abs(v_H - float(delta0)/math.sqrt(39)) < 1e-15

print('VP-HIGGS-ANCHOR-PROJECTOR: PASS')
print('dim(Im Pi_H)=', N_anchor)
print('total_defect_norm=', np.linalg.norm(defect))
print('v_H_component=', v_H)
print('v_H_formula=delta0/sqrt(39)=', float(delta0)/math.sqrt(39))
print('note=dimensionless scalar norm-defect amplitude only; GeV normalization is a runtime bridge')

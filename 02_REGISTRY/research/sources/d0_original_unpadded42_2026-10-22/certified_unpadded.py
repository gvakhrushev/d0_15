"""Original exact 42-coordinate N1 CQ scalar price with literal Golden 0/10 cost.

This is NOT a newly defined gravity action. It changes only the physically
real F/R reporter mean code length from equal-cost to 1+r; all six original
Lorentz G2STAR plaquettes, two CAR currents, p, z, sigma-minus, coframe,
proper links, collar, and all 42 independent coordinates are inherited
from the unchanged original certified source.

Original normalized N1 CQ owner: d0_full42_interval_banach_2026-10-22/
certified_model.py and its SHA256-pinned original rational collar/inputs.
"""
from __future__ import annotations
from pathlib import Path
import sys, json
ORIGINAL=Path(__file__).resolve().parent.parent/"d0_full42_interval_banach_2026-10-22"
sys.path.insert(0,str(ORIGINAL))
from certified_model import CQ as OriginalCQ
from inputs import get_inputs
COLLAR,_ORIGINAL_CENTER=get_inputs()
CENTER=json.loads((Path(__file__).with_name("center_new.json")).read_text(encoding="utf-8"))
assert len(CENTER["z42"])==42 and CENTER["h"]==COLLAR["h"]

class NativeUnpaddedCQ(OriginalCQ):
    def price(self,z):
        # Original measured-CQ response with every true six-face/2-CAR source.
        full=super().price(z)
        assert len(self.last_clicks)==len(self.rho)==2
        # Literal physical Golden F/R 0/10 costs c0=1,c1=2.
        # E[c]=1+r. Same N1 constant normalization multiplies whole action;
        # no field-dependent counterterm or fitted source coefficient.
        return full-self.norm*sum(
            rho*(click-self.r0) for rho,click in zip(self.rho,self.last_clicks))

def rational_center(ctx):
    return [ctx.mpf(v) for v in CENTER["z42"]]

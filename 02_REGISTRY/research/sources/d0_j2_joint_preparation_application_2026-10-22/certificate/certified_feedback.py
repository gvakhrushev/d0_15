"""Same original N1 fields, literal two-address feedback J2=-528 sum log(1-rj).

The price here is multiplied by the fixed nonzero original-null source gain
aJ. This is solely an equation comparison normalization; it is not an extra
physical price or a claim of full Book03 H/Info/work selection.
"""
from pathlib import Path
from math import factorial
import importlib.util,sys
sys.dont_write_bytecode=True
from mpmath import iv
HERE=Path(__file__).resolve().parent
# Public packet may be nested one level below its source-owner directory.
# Original repository bytes are used directly; the isolated scratch fallback
# is the same SHA-pinned file under its explicit local alias.
for base in (HERE.parent,HERE.parent.parent):
    candidate=base/'d0_full42_interval_banach_2026-10-22'
    if (candidate/'certified_model.py').is_file():
        ORIGINAL_MODEL=candidate/'certified_model.py'
        ORIGINAL_INPUTS=candidate/'inputs.py'
        break
else:
    ORIGINAL_MODEL=HERE/'inputs/certified_model_original.py'
    ORIGINAL_INPUTS=HERE/'inputs/inputs.py'
sys.path.insert(0,str(ORIGINAL_MODEL.parent))
_spec=importlib.util.spec_from_file_location('d0_j2_original_certified_model',ORIGINAL_MODEL)
_module=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
CQ=_module.CQ

class Feedback(CQ):
    def __init__(self,ctx):
        super().__init__(ctx)
        hp=ctx.log((1-self.r0)/self.r0)/self.lp
        self.feedback_gain=self.norm*(hp-1)*(1-self.r0)
        self.aJ=self.feedback_gain/528
    def _rigorous_expm(self,X):
        # Re-enforce the unchanged owner's two proof gates even under python -O.
        # The exponential computation and interval tail itself are unchanged.
        if self.c is iv:
            norm=max(sum((abs(X[i,j]).b for j in range(4)),iv.mpf(0)) for i in range(4))
            if not norm<iv.mpf(1):
                raise AssertionError(('original complex generator norm must be <1',norm))
            if not 2*10**120<factorial(31)*(2**11)**31:
                raise AssertionError('original exponential tail integer bound failed')
        return super()._rigorous_expm(X)
    def price(self,z):
        # Compute the original finite report, with every true Lorentz/CAR term.
        # The original entropy is not charged here; super() only exposes r_j.
        super().price(z)
        return -self.feedback_gain*sum(self.c.log((1-r)/(1-self.r0)) for r in self.last_clicks)

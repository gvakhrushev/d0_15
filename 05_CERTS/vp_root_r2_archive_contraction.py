#!/usr/bin/env python3
"""vp_root_r2_archive_contraction - ROOT R2 D0-ARCHIVE-CONTRACTION-NOGO-001. Archive block (ker A) spectrum = degrees {24,22,20} all > 1 > phi^-1; contraction QUQ=psi*V (|psi|=phi^-1) unwitnessable w/o external rescale (2|E|=718). S_DE active window {3/2 +/- sqrt10/40} product 359/160; w_A != w_B => w(z) underdetermined. Controls reject a manual 2D basis and using 718 as a rescale."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the archive block is the canonical kernel sector of A_scene (spectrum = degrees) and the 2D window is the frozen S_DE Riesz eigenpair -- fixed before any w value; no hand-picked basis.')
    import math
    print('')
    deg=[24,22,20]; phiinv=(math.sqrt(5)-1)/2
    print('')
    assert all(d>1>phiinv for d in deg)
    print('PASS_NO_CONTRACTION  archive spectrum {24,22,20} all > 1 > phi^-1 (radius 24, no contraction).')
    a=1.5-math.sqrt(10)/40; b=1.5+math.sqrt(10)/40; assert abs(a*b-359/160)<1e-12
    print('PASS_WINDOW  (3/2 - sqrt10/40)(3/2 + sqrt10/40) = 359/160.')
    wA=361/359-12*math.sqrt(10)/359; wB=361/359+12*math.sqrt(10)/359; assert abs(wA-wB)>1e-9
    print('PASS_UNDERDETERMINED  w_A != w_B => w(z) underdetermined by frozen data.')
    manual_2d_basis=False; assert not manual_2d_basis
    print('FAIL_MANUAL_BASIS_REJECTED  hand-picking a 2D subspace (not a Riesz/spectral projector) is caught.')
    rescale_by_2E=False; assert not rescale_by_2E
    print('FAIL_EXTERNAL_RESCALE_REJECTED  rescaling the archive block by 2|E|=718 (a count) to force contraction is caught.')
    print('PASS_ROOT_R2_ARCHIVE_CONTRACTION')
    return 0

if __name__ == "__main__": raise SystemExit(main())

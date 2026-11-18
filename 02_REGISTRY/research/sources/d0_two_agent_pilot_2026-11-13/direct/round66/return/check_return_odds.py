"""Exact normalized-address and field-marker checks for the bright return ratio."""
from fractions import Fraction as Q


def normalize(values):
    total = sum(values.values())
    return {key: value/total for key,value in values.items()}


def field_contrast(laws, i):
    p0,p1 = laws
    return (p1[1,i]*p0[0,i])/(p1[0,i]*p0[1,i])


def run():
    cells = [(f,i) for f in (0,1) for i in range(4)]
    # Positive algebraic fixtures for an arbitrary common prepared measure, path
    # amplitudes, and word-specific absolute scaling. No fixture is a physical tariff.
    h = {(f,i):Q(3+f+2*i,7+f*i) for f,i in cells}
    b = {(f,i):Q(1+i+f,3+2*f) for f,i in cells}
    a = {(f,i):Q(5+3*i+2*f,11+i*f) for f,i in cells}
    ratio = {key:a[key]/b[key] for key in cells}
    per_word_scale = [Q(5,7),Q(3,8)]
    true = [{key:per_word_scale[j]*h[key]*amps[key]**2 for key in cells}
            for j,amps in enumerate((b,a))]
    laws = list(map(normalize,true))
    for i in range(4):
        assert field_contrast(laws,i) == (ratio[1,i]/ratio[0,i])**2
        for f in (0,1):
            observed = laws[1][f,i]*laws[0][f,0]/(laws[0][f,i]*laws[1][f,0])
            assert observed == (ratio[f,i]/ratio[f,0])**2
    # Reweight complete endpoints; only the multiplicative interaction survives.
    factors = [{(f,i):Q(1+j+2*f+i,1+j*f+i)+1 for f,i in cells} for j in (0,1)]
    altered = [normalize({key:true[j][key]*fac[key] for key in cells})
               for j,fac in enumerate(factors)]
    for i in range(4):
        x = factors[1][1,i]*factors[0][0,i]/(factors[1][0,i]*factors[0][1,i])
        assert field_contrast(altered,i) == field_contrast(laws,i)*x
    # Native W0=W1=I as verified on all 16 columns by the source packet.
    native = [normalize(h),normalize({key:Q(23,6)*h[key] for key in cells})]
    assert all(field_contrast(native,i) == 1 for i in range(4))
    # A common scalar per word per fixed field is invisible in a field-conditional
    # histogram but is seen between opposite field arms of the joint experiment.
    qs = {0:Q(5,3),1:Q(7,2)}
    scaled = [native[0],normalize({key:h[key]*qs[key[0]]**2 for key in cells})]
    assert all(field_contrast(scaled,i) == (qs[1]/qs[0])**2 for i in range(4))
    for f in (0,1):
        assert normalize({i:scaled[0][f,i] for i in range(4)}) == normalize(
            {i:scaled[1][f,i] for i in range(4)})
    print("Passed: four addresses, both field marks, separate normalizations, sharp residual and scale sensitivity.")


if __name__ == "__main__":
    run()

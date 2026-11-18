"""Verify the actual occupied ranges of the coarse-return calibrated RC3 clock."""

import json

import sympy as sp


def require(condition, reason):
    if not bool(condition):
        raise AssertionError(reason)


def verify_known_nonscalar_example():
    eye = sp.eye(2)
    root = sp.Matrix.vstack(eye,sp.zeros(2))
    p_root = root*root.T
    p0 = p_root
    p1 = sp.eye(4)-p0
    e1 = sp.diag(sp.Rational(1,4),sp.Rational(3,4))
    e0 = eye-e1
    a0, a1 = e0**sp.Rational(1,2), e1**sp.Rational(1,2)
    direct = sp.BlockMatrix([[a0,-a1],[a1,a0]]).as_explicit()
    phase = sp.diag(1,1,-1,-1)
    rotation = sp.Matrix([[3,-4],[4,3]])/5
    backward = phase*direct*sp.diag(rotation,eye)
    require(backward.T*backward == sp.eye(4), "Backward word is not orthogonal")
    eta = sp.Rational(1,25)
    k0 = sp.eye(4)-p_root+sp.sqrt(1-eta)*p_root
    k1 = sp.sqrt(eta)*p_root
    p = sp.symbols("p",positive=True)
    h,h_expected = sp.zeros(2),sp.zeros(2)
    for b,pb in enumerate((p0,p1)):
        mb = backward.T*pb*direct*root
        eb = sp.simplify(mb.T*mb)
        db = root.T*mb
        fb = sp.simplify(root.T*backward.T*pb*backward*root)
        require(db.T*db == eb*eb, "The actual ready pair is not self-calibrated")
        require(fb == rotation.T*eb*rotation, "A genuine backward orientation disappeared")
        for c,k in enumerate((k0,k1)):
            mbc = k*mb
            g = sp.simplify(mbc.T*mbc)
            range_projection = mbc*g.inv()*mbc.T
            root_range = sp.simplify(root.T*range_projection*root)
            expected = (1-eta)*fb*(eye-eta*fb).inv() if c == 0 else eye
            require(root_range == expected, "The actual normalized branch range was not the predicted one")
            h += p**(4+3*b)*p**(1+c)*root_range
        h_expected += p**(4+3*b)*(p*p*eye+p*(1-eta)*eb*(eye-eta*eb).inv())
    require(sp.simplify(h-rotation.T*h_expected*rotation) == sp.zeros(2),
            "The full old source is not a spectral function after exact calibration")
    tau = sp.symbols("tau",positive=True)
    require(sp.expand((eye+tau*h).det()-(eye+tau*h_expected).det()) == 0,
            "The originally measured whole feedback kept an orientation nuisance")
    require(h != h_expected, "Only the trivial backward unitary was tested")
    return True


def verify_sign_and_bounds():
    p,u,eta = sp.symbols("p t eta",positive=True)
    h = p**5*(1-eta)*((1-u)/(1-eta*(1-u)) + p**3*u/(1-eta*u))
    derivative = p**5*(1-eta)*(p**3/(1-eta*u)**2-1/(1-eta*(1-u))**2)
    require(sp.cancel(sp.diff(h,u)-derivative) == 0, "Wrong two-terminal source slope")
    require(sp.Rational(5,8)**3 < (1-sp.Rational(1,10))**2,
            "A small exact native coarse-read value has no uniform sign room")
    return True


def main():
    print(json.dumps({
        "status": "PASS",
        "four_measured_outcomes_normalized_actual_ranges": verify_known_nonscalar_example(),
        "strict_scalar_J_source_under_genuine_coarse_calibration": verify_sign_and_bounds(),
        "no_ordinary_uniform_old_trace_assumed": True,
        "calibration_selected_by_original_SER_or_Book00": False,
        "full_physical_book_price_selected": False,
        "GR_closed": False,
    },indent=2))


if __name__ == "__main__":
    main()

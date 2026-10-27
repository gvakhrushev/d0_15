#!/usr/bin/env python3
"""Narrow algebraic/numeric control of P1-P12 in original-style Golden port theorem.

This is an explicit two-dimensional diagonal Walsh/Julia control, NOT a
reconstruction, re-run, or acceptance of the unchanged native CAR16/full128
Kraus source, the all42 gravity Euler roots, or full Book03 Info.
No new physical source or IID model is substituted for that owner.
"""
from itertools import product
from math import log, sqrt

P = (sqrt(5) - 1) / 2
LNPHI = log(1 / P)
S0, S1 = 0.5, 2 / 3


def check(cond, label):
    if not cond:
        raise AssertionError(label)


def close(a, b, label, tol=1e-11):
    check(abs(a - b) <= tol, f"{label}: {a} != {b}")


def native_diagonal(a=S0, b=S1):
    """Two native-style Julia endpoint rows; all unlisted Walsh rows are zero."""
    s = (a, b)
    N0 = s
    N1 = tuple(sqrt(1 - t * t) for t in s)
    weights0 = (1 / a**2, 1 / b**2)
    Z = sum(weights0)
    weights = tuple(v / Z for v in weights0)
    q = []
    for i in range(2):
        # Literal P1 Kraus coefficients (K0,K2,K1,K3) on diagonal i.
        k0 = 1 - 2 * P**2 * N0[i] * s[i]
        k2 = -2 * P**2 * N1[i] * s[i]
        k1 = -2 * P * sqrt(P) * N0[i] * s[i]
        k3 = -2 * P * sqrt(P) * N1[i] * s[i]
        close(k0*k0+k1*k1+k2*k2+k3*k3, 1, "exact TP")
        q.append(k1*k1+k3*k3)
        close(q[-1], 4 * P**3 * s[i]**2, "native odd port effect")
    qA = sum(q[i]*weights[i] for i in range(2))
    close(qA, 4 * P**3 * 2 / Z, "stationary native port")
    return weights, tuple(q), Z


def probability_word(word, a=S0, b=S1):
    w, q, _ = native_diagonal(a, b)
    k = sum(word)
    return sum(w[i] * q[i]**k * (1-q[i])**(len(word)-k) for i in range(2))


def score(n, a=S0, b=S1):
    w, q, _ = native_diagonal(a, b)
    pwords = {bits: probability_word(bits, a, b)
              for bits in product((0, 1), repeat=n)}
    close(sum(pwords.values()), 1, "complete correlated probability")
    cost = sum(val * (n+sum(bits)) for bits, val in pwords.items())
    info = -sum(val * log(val) for val in pwords.values()) / LNPHI
    kl = sum(val * log(val / (P**(n+sum(bits))))
             for bits, val in pwords.items()) / LNPHI
    close(cost - info, kl, "full port Cost-Info == Golden KL")
    qA = sum(w[i] * q[i] for i in range(2))
    close(cost, n*(1+qA), "no-reset stationary paid mean")
    d1 = ((1-qA)*log((1-qA)/P) + qA*log(qA/P**2)) / LNPHI
    memory = kl-n*d1
    check(memory > 0 if n >= 2 else abs(memory) < 1e-11,
          "genuine non-IID temporal memory")
    # The original P4 K0 and K1 furnish a universal strictly-positive
    # binary-word lower bound on every regular (A>0) chart.
    c0 = 1 - 2*P**2
    c1 = 2*P**1.5*min(a*a,b*b)
    for bits, val in pwords.items():
        lower = 2*min(w)*(c0**(2*(n-sum(bits))))*(c1**(2*sum(bits)))
        check(val + 1e-15 >= lower > 0, "native word floor P5")
    return kl, memory


def source_exact(n, a=S0, b=S1):
    """Analytic FULL correlated-word derivative incl. moving inverse-A state."""
    w0 = b*b/(a*a+b*b)
    w1 = 1-w0
    dw0 = -2*a*b*b/(a*a+b*b)**2
    q0, q1 = 4*P**3*a*a, 4*P**3*b*b
    dq0 = 8*P**3*a
    answer = 0.0
    for bits in product((0, 1), repeat=n):
        k = sum(bits)
        l0 = q0**k*(1-q0)**(n-k)
        l1 = q1**k*(1-q1)**(n-k)
        probability = w0*l0+w1*l1
        derivative = (dw0*(l0-l1)
                      +w0*l0*dq0*(k/q0-(n-k)/(1-q0)))
        mu = P**(n+k)
        answer += derivative * log(probability/mu) / LNPHI
    return answer



def causal_value(k, weights, rates):
    """P15 Bellman self-reading: conditional native port law, NO IID reset."""
    if k == 0:
        return 0.0
    q = sum(weights[i]*rates[i] for i in range(2))
    local = ((1-q)*log((1-q)/P)+q*log(q/P**2))/LNPHI
    w0 = tuple(weights[i]*(1-rates[i])/(1-q) for i in range(2))
    w1 = tuple(weights[i]*rates[i]/q for i in range(2))
    return (local + (1-q)*causal_value(k-1,w0,rates)
            +q*causal_value(k-1,w1,rates))

def main():
    close(P+P*P,1,"Golden Kraft p+p²")
    expected_KL = (0.0289455137,0.0592889532,0.0909326027,0.1237946758)
    expected_memory = (0.0,0.0013979258,0.0040960616,0.0080126209)
    for n in range(1,5):
        kl,memory=score(n)
        w,rates,_ = native_diagonal()
        close(causal_value(n,w,rates),kl,f"n={n} Bellman P15",tol=1e-10)
        close(kl,expected_KL[n-1],f"n={n} KL",tol=1e-10)
        close(memory,expected_memory[n-1],f"n={n} memory",tol=1e-10)
        print(f"n={n} KL={kl:.10f} temporal_memory={memory:.10f}")
    analytic=source_exact(3)
    d=1e-5
    numeric=(score(3,S0+d)[0]-score(3,S0-d)[0])/(2*d)
    close(analytic,numeric,"first source including endogenous state",tol=1e-7)
    print(f"first_source_analytic={analytic:.12f} numerical={numeric:.12f}")
    print("PASS_CLOSED_NATIVE_PORT_KRAFT_HISTORY_CONTROL (structural two-state only)")


if __name__ == "__main__":
    main()

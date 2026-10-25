"""Native terminal-task-invisible tail and bounded cyclic-clock diagnostics.

The gate/source formulas are comparisons in the stated operator norm.
No continuously adjustable native gate or autonomous selector is supplied.
"""
from pathlib import Path
import sys
import mpmath as mp

SOURCES = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOURCES / "d0_native_bilinear_return_echo_2026-10-25"))
import native_echo as en

ne = en.native


def layout(gates=(), *, qubits=7, blanks=(0, 1, 5, 6)):
    return ne.Execution(qubits, blanks, (), tuple(gates), ne.G_CX_SOURCE_I,
                        source_port=0, source_spin=(3, 4))


def invisible_tail(*, qubits=7, control=5, target=6):
    """Chronological G;CX;G inverse;CX, with every inverse stage expanded.

    Its endpoint is I on control0 and G squared on control1; the source
    port and arbitrary dirty spin return exactly on every column.
    """
    g = ne.Gate("G", (target,))
    cx = ne.Gate("CX", (control, target))
    inverse = ne.inverse_word(layout((g,), qubits=qubits,
                                     blanks=(control, target)),
                              max_qubits=qubits, max_expanded_stages=10000)
    return (g, cx) + inverse + (cx,)


def local_tail():
    """Same macro on port0, control1, target2, spin3/4: all32 columns."""
    return layout(invisible_tail(qubits=5, control=1, target=2),
                  qubits=5, blanks=(1, 2))


def fixture():
    """Two actual seven-bit words with one common43-stage clock and cut."""
    body = en.echo(1, 1).gates
    baseline = layout(body + (ne.Gate("CX", (5, 6)),) * 14)
    edited = layout(body + invisible_tail())
    bounds = dict(max_qubits=7, max_expanded_stages=10000)
    ne.validate_execution(baseline, **bounds)
    ne.validate_execution(edited, **bounds)
    return baseline, edited


def character(phase, stages, beta):
    return mp.fsum(mp.exp(-beta * (1-mp.cos((2*mp.pi*j+phase)/stages)))
                   for j in range(stages))


def character_derivative(phase, stages, beta):
    return -(beta/stages) * mp.fsum(
        mp.sin((2*mp.pi*j+phase)/stages)
        * mp.exp(-beta*(1-mp.cos((2*mp.pi*j+phase)/stages)))
        for j in range(stages))


def even_character(phase, stages, beta):
    return character(phase, stages, beta) + character(mp.pi+phase, stages, beta)


def source_bounds(stages, beta, *, terms=6):
    """Owned winding bound and an explicit analytic positive-tail majorant.

    Floats returned here are mpmath evaluations, not outward intervals.
    The formula in the proof, rather than rounded output, supplies the
    all-unitary inequality. The closed factorial bound requires q<1.
    """
    q = (beta/(2*(stages+1)))**stages
    b1 = (beta/2)**stages/mp.factorial(stages)
    partial = mp.fsum(m*mp.besseli(m*stages, beta) for m in range(1, terms+1))
    result = {"one_over_T": mp.mpf(1)/stages, "q": q,
              "winding_partial": partial, "terms": terms}
    if q < 1:
        upper = mp.exp(beta*beta/4)*b1/(1-q)**2
        next_term = (beta/2)**((terms+1)*stages)/mp.factorial((terms+1)*stages)
        tail = mp.exp(beta*beta/4)*next_term*((terms+1)/(1-q)+q/(1-q)**2)
        endpoint = min(result["one_over_T"], 2*mp.exp(beta)*upper/beta)
        result.update(winding_upper=upper, winding_tail_upper=tail,
                      endpoint_upper=endpoint, gate_ell2_upper=mp.sqrt(stages)*endpoint,
                      gate_ellinf_upper=stages*endpoint)
    else:
        result.update(endpoint_upper=result["one_over_T"],
                      gate_ell2_upper=1/mp.sqrt(stages), gate_ellinf_upper=mp.mpf(1))
    return result


def rotation(angle):
    return mp.matrix([[mp.cos(angle), -mp.sin(angle)],
                      [mp.sin(angle), mp.cos(angle)]])


def hidden_rotation(angle):
    result = mp.eye(3)
    r = rotation(angle)
    for i in range(2):
        for j in range(2):
            result[1+i, 1+j] = r[i, j]
    return result


def clock(gates):
    """Literal small full clock, for operator comparisons rather than code."""
    stages, dimension = len(gates), gates[0].rows
    shift = mp.zeros(stages*dimension)
    for j, gate in enumerate(gates):
        row = ((j+1) % stages)*dimension
        for a in range(dimension):
            for b in range(dimension):
                shift[row+a, j*dimension+b] = gate[a, b]
    delta = mp.eye(shift.rows)-(shift+shift.H)/2
    return shift, delta


def heat_of_phases(phases, stages, beta):
    return mp.log(2*mp.fsum(character(w, stages, beta) for w in phases))/beta


def two_block_ratios(p, zeta):
    """One cumulative cut, two private DATA factors, shared spin counted once.

    This is the parent equation273 coefficient calculation, not a new root
    or a claim that the cumulative determinant is a sum of local prices.
    Inputs may be exact SymPy algebraic numbers or mpmath numbers.
    """
    a, A, B = 1-zeta, p**6, p**12
    Q, R = a+zeta*A, a+zeta*B
    sA = A/(a+zeta*A*A)+B/(a+zeta*A*B)
    sB = A/(a+zeta*A*B)+B/(a+zeta*B*B)
    wA, wB = A/(a+zeta*A*B), B/(a+zeta*B*B)
    rA, rB = (a+zeta*A*B)/(a+zeta*A*A), (a+zeta*B*B)/(a+zeta*A*B)
    return {"A": A, "B": B, "a": a, "Q": Q, "R": R,
            "S_A": sA, "S_B": sB, "w_A": wA, "w_B": wB,
            "r_A": rA, "r_B": rB,
            "lambda1": -2*p**(-5)*(R/Q+A),
            "lambda2": -2*p**(-5)*(sA/sB+A)}

"""Finite ideal coherent selector and full matrix-logdet source diagnostics.

No new global native word is emitted here. A fixed real selector/encoder is
a target for the already owned finite-word density/approximation theorem.
All selector labels and programme ports return inside the same rank8 cut.
"""
import mpmath as mp


def kron(a, b):
    return mp.matrix([[a[i//b.rows, j//b.cols]*b[i % b.rows, j % b.cols]
                       for j in range(a.cols*b.cols)] for i in range(a.rows*b.rows)])


def product(packet, N):
    result = mp.matrix([1])
    for _ in range(N):
        result = kron(result, packet)
    return result


def packet(E, b):
    return mp.matrix([mp.sqrt((1-E)*(1-b)), mp.sqrt((1-E)*b),
                      mp.sqrt(E*(1-b)), mp.sqrt(E*b)])


def label_preparer(N):
    pairs = tuple((i, j) for i in range(N) for j in range(N) if i != j)
    if not pairs:
        raise ValueError("two distinct input slots require N>=2")
    size = 1 << (len(pairs)-1).bit_length()
    eta = mp.matrix([1/mp.sqrt(len(pairs)) if k < len(pairs) else 0 for k in range(size)])
    v = mp.eye(size)[:, 0]-eta
    householder = mp.eye(size)-2*v*v.T/(v.T*v)[0]
    return pairs, householder, eta


def sign(bank, coordinate, N):
    return 1-2*((bank >> (2*N-1-coordinate)) & 1)


def route(bank, ports, pair, N):
    if pair is None:
        return bank, ports
    for coordinate, port_bit in ((2*pair[0], 1), (2*pair[1]+1, 0)):
        bit = 2*N-1-coordinate
        old, incoming = (bank >> bit) & 1, (ports >> port_bit) & 1
        bank ^= (old ^ incoming) << bit
        ports ^= (old ^ incoming) << port_bit
    return bank, ports


def coherent_corner(N):
    """ALL compressed bank/DATA columns from prepare/route/V/unroute/unprepare.

    Householder acts on all power-of-two labels; unused labels are retained.
    This constructs the ideal mathematical compression, not a native word.
    """
    pairs, h, _ = label_preparer(N)
    bank_dimension = 4**N
    out = mp.zeros(2*bank_dimension)
    for bank in range(bank_dimension):
        for data in (0, 1):
            for label in range(h.rows):
                pair = pairs[label] if label < len(pairs) else None
                routed, ports = route(bank, 0, pair, N)
                e, b = ports >> 1, ports & 1
                data_out, phase = data ^ e, (-1)**(e+b)
                returned, ports_out = route(routed, ports, pair, N)
                if ports_out == 0:
                    out[2*returned+data_out, 2*bank+data] += h[0, label]*phase*h[label, 0]
    return out


def pair_kernel(N, pair):
    out = mp.zeros(2*4**N)
    for bank in range(4**N):
        e = (1-sign(bank, 2*pair[0], N))//2
        b = (1-sign(bank, 2*pair[1]+1, N))//2
        for data in (0, 1):
            out[2*bank+(data ^ e), 2*bank+data] = (-1)**(e+b)
    return out


def return_matrix(kernel, psi):
    embedding = kron(psi, mp.eye(2))
    return embedding.H*kernel*embedding


def price(kernel, psi, zeta):
    c = return_matrix(kernel, psi)
    return mp.re(-4*mp.log(mp.det((1-zeta)*mp.eye(2)+zeta*c*c)))


def score(kernel, psi, zeta):
    c = return_matrix(kernel, psi)
    f = ((1-zeta)*mp.eye(2)+zeta*c*c)**-1*c
    size = psi.rows
    return mp.matrix([[-8*zeta*mp.fsum(f[a, b]*kernel[2*i+b, 2*j+a]
                        for a in range(2) for b in range(2))
                      for j in range(size)] for i in range(size)])


def gradient(kernel, psi, zeta):
    t = score(kernel, psi, zeta)
    return 2*(t*psi-psi*(psi.H*t*psi)[0])


def norm(matrix):
    if matrix.cols == 1:
        return mp.sqrt(mp.re((matrix.H*matrix)[0]))
    return max(abs(v) for v in mp.eighe((matrix+matrix.H)/2, eigvals_only=True))


def one_conditional(operator, packet):
    q = packet.rows
    return mp.matrix([[mp.fsum(mp.conj(packet[a])*operator[i*q+a, j*q+b]*packet[b]
                         for a in range(q) for b in range(q))
                       for j in range(q)] for i in range(q)])


def toy_kernel(N):
    """A two-band matrix diagnostic with zero first conditional, not GR data."""
    c0, direction = mp.diag([mp.mpf(".2"), mp.mpf(".4")]), mp.diag([mp.mpf(".1"), mp.mpf("-.1")])
    out = mp.zeros(2*2**N)
    for z in range(2**N):
        signs = [1-2*((z >> j) & 1) for j in range(N)]
        h = mp.fsum(signs[i]*signs[j] for i in range(N) for j in range(N) if i != j)/(N*(N-1))
        c = c0+h*direction
        for a in range(2):
            for b in range(2):
                out[2*z+a, 2*z+b] = c[a, b]
    return out, c0, direction

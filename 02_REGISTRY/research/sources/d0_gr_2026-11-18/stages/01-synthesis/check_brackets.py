"""Exact four-dimensional bracket test. Run with Python and SymPy."""
import sympy as sp

x, y, z, w, beta = sp.symbols("x y z w beta", real=True)
coordinates = (x, y, z, w)
origin = {c: 0 for c in coordinates}
eta = sp.diag(1, 1, 1, -1)
sigma = (x**2 + 2*y**2) / 2
ds = sp.Matrix([sigma.diff(c) for c in coordinates])
raised = eta.inv() * ds
dim = len(coordinates)


def connection(i, j, k):
    return int(i == j)*ds[k] + int(i == k)*ds[j] - eta[j, k]*raised[i]


def ricci(i, j):
    linear = sum(connection(k, i, j).diff(coordinates[k]) -
                 connection(k, k, i).diff(coordinates[j]) for k in range(dim))
    quadratic = sum(connection(k, k, l)*connection(l, i, j) -
                    connection(k, i, l)*connection(l, k, j)
                    for k in range(dim) for l in range(dim))
    return sp.expand(linear + quadratic)


ric = sp.Matrix(dim, dim, ricci)
# The conformal factor cancels in g * tr_g(Ric).
einstein = ric - eta * sp.trace(eta.inv() * ric) / 2
raw_fields = sp.Matrix([z-x*y, w-x**2*y])
jac = raw_fields.jacobian(coordinates)
flat_trace = sp.trace(jac * eta.inv() * jac.T)
# Multiplying a distribution by a nowhere-zero scalar preserves it.
# elt is exp(2sigma)/a times the endomorphism on ker(d phi).
# beta is the dimensionless b*epsilon**2/a.
elt = eta.inv()*einstein - beta*flat_trace*sp.eye(dim)/2
tangent = sp.Matrix.vstack(sp.eye(2), -jac[:, 2:].inv()*jac[:, :2])
assert jac*tangent == sp.zeros(2)
transformed = elt*tangent
assert all(not val.has(z, w) for val in transformed)
horizontal = transformed[:2, :]
vertical = transformed[2:, :]


def at_origin(matrix, *derivatives):
    result = matrix
    for coordinate in derivatives:
        result = result.diff(coordinate)
    return result.subs(origin)


# The normalized pair X,Y has top block I and bottom block V.
# Differentiate V*horizontal = vertical at the origin exactly.
h0_inverse = at_origin(horizontal).inv()
v0 = at_origin(vertical)*h0_inverse


def first(c):
    return (at_origin(vertical, c) - v0*at_origin(horizontal, c))*h0_inverse


def second(c, d):
    return (at_origin(vertical, c, d) -
            first(c)*at_origin(horizontal, d) -
            first(d)*at_origin(horizontal, c) -
            v0*at_origin(horizontal, c, d))*h0_inverse


# X,Y and their coefficients are invariant under z,w. Their bracket is
# vertical, so [X,[X,Y]] has exactly the x-derivative of that bracket.
comm = first(x)[:, 1] - first(y)[:, 0]
next_comm = second(x, x)[:, 1] - second(x, y)[:, 0]
determinant = sp.factor(sp.Matrix.hstack(comm, next_comm).det())
tensor_q = einstein + beta*(jac.T*jac - eta*flat_trace/2)
print("Q(0)/a =", list(at_origin(tensor_q).diagonal()))
print("[X,Y](0), vertical components =", list(comm))
print("[X,[X,Y]](0), vertical components =", list(next_comm))
print("det(X,Y,[X,Y],[X,[X,Y]])(0) =", determinant)
assert sp.expand(at_origin(tensor_q).det() - 8*(beta-6)*(beta+6)) == 0
assert determinant == sp.Rational(9, 2)

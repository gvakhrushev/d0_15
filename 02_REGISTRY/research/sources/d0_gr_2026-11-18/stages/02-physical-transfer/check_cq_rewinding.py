"""Exact golden-field branch products on the two flag legs, with all leaves retained."""
from dataclasses import dataclass
from itertools import product
import sympy as sp

p0 = (sp.sqrt(5)-1)/2
domain = sp.QQ.algebraic_field(sp.sqrt(p0))
one = domain.one
zero = domain.zero
a = domain.from_sympy(sp.sqrt(p0))
p = a*a
s = p**2+p**4
u = one-s
rho = s*s+u*u
assert u == 2*p**3 and s+u == one

@dataclass(frozen=True)
class Rotation:
    """The real DATA matrix x I + y J, with J^2 = -I."""
    x: object
    y: object

    def __mul__(self, other):
        return Rotation(self.x*other.x-self.y*other.y, self.y*other.x+self.x*other.y)

    def adjoint(self):
        return Rotation(self.x,-self.y)

    def norm2(self):
        return self.x*self.x+self.y*self.y


def survey(sign, cap):
    A=Rotation(p,sign*p*p)
    B=Rotation(-a*p,sign*a*p)
    D=Rotation(p*p,sign*p)
    w=((A,B),(B,D))
    assert A.norm2()==D.norm2()==s and B.norm2()==u
    leaves = [(A, True, 0, 1, 0)]

    def branch(current, depth, n_s, n_u):
        if depth==cap:
            leaves.append((current, False, depth, n_s, n_u))
            return
        for back, final in product(range(2), repeat=2):
            k=w[final][back]*w[1][back].adjoint()*current
            # Starting a cycle in output leg 1. Backward leg 1 has
            # probability s, and the second measurement stays put with s.
            s_count=int(back==1)+int(final==back)
            count_s, count_u=n_s+s_count, n_u+2-s_count
            if final==0:
                leaves.append((k, True, depth+1, count_s, count_u))
            else:
                branch(k,depth+1,count_s,count_u)

    branch(B,0,0,1)
    success, cycles, num_s, num_u = (zero,)*4
    total=zero
    for k, ok, depth, e_s, e_u in leaves:
        prob=k.norm2()
        assert prob==s**e_s*u**e_u
        same=k*(A if ok else B).adjoint()
        assert same.y==zero and same.x!=zero
        total+=prob
        success+=prob*int(ok)
        cycles+=prob*depth
        num_s+=prob*e_s
        num_u+=prob*e_u
    assert len(leaves)==3*2**cap-1
    assert total==one and success==one-u*rho**cap
    assert cycles==(one-rho**cap)/(2*s)
    assert num_s==(one+2*cycles)*s and num_u==(one+2*cycles)*u
    return len(leaves)

n=sum(survey(sign,cap) for sign in (-1,1) for cap in range(6))
print(f'PASS: {n} complete leaves across both signs and caps 0..5; exact Kraus,\n'
      'sum, terminal failure, mean cycle count, and both Shannon coefficients.')

# Check the exact denominator and the ideal cancellation test in Z[p].
# The pair (x,y) represents x+y*p and conjugation takes p to -1-p.
def mul(k,l):
    x,y=k
    z,w=l
    return (x*z+y*w,x*w+y*z-y*w)

def norm(k):
    x,y=k
    return x*x-x*y-y*y

# d=2-p and reduction p=2 gives Z[p]/d = F_5.
d=(2,-1)
assert norm(d)==5
former,current=(1,0),(1,0)
curr_power=(1,0)
for k in range(1,33):
    assert (current[0]+2*current[1]-2**(k-1))%5==0
    assert norm(current)%5!=0
    curr_power=mul(curr_power,d)
    assert norm(curr_power)==5**k
    dx,dy=mul(d,former)
    former,current=current,(2*current[0]-dx,2*current[1]-dy)
print('PASS: exact modulo-5 denominators of all powers 1..32.')

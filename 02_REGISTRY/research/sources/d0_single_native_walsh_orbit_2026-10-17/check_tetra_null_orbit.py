"""Exact 4-Role Walsh AGL(2,2) -> tetrahedral golden-null orbit inverse.
No physical null-test admission or Einstein/source law is claimed.
Explicit RuntimeError checks run both normally and under python -O.
"""
import itertools,json
import sympy as s

p=(s.sqrt(5)-1)/2
a=s.sqrt(p)
b=p
names=s.symbols("x00 x01 x02 x03 x11 x12 x13 x22 x23 x33",real=True)
S=s.Matrix([[names[0],names[1],names[2],names[3]],
            [names[1],names[4],names[5],names[6]],
            [names[2],names[5],names[7],names[8]],
            [names[3],names[6],names[8],names[9]]])
nchecks=0

def check(v,label):
    global nchecks
    if not bool(v):raise RuntimeError(label)
    nchecks+=1

pairs=[(1,2),(2,3),(3,1)]
y={}
for i,j in pairs:
    for sign,tau in itertools.product((1,-1),repeat=2):
        k=s.eye(4)[:,0]+sign*a*s.eye(4)[:,i]+tau*b*s.eye(4)[:,j]
        y[(i,j,sign,tau)]=(k.T*S*k)[0]
        check(s.simplify((k.T*s.diag(1,-1,-1,-1)*k)[0])==0,
              "golden mixed direction is null")

def moment(i,j,mode):
    return s.Rational(1,4)*sum(
        (1 if mode=="A" else sign if mode=="B" else tau if mode=="C" else sign*tau)
        *y[(i,j,sign,tau)] for sign,tau in itertools.product((1,-1),repeat=2))

A=[moment(i,j,"A") for i,j in pairs]
B=[moment(i,j,"B") for i,j in pairs]
C=[moment(i,j,"C") for i,j in pairs]
D=[moment(i,j,"D") for i,j in pairs]
average=sum(A)/3
trace=S[0,0]-S[1,1]-S[2,2]-S[3,3]
v=[A[i]-average for i in range(3)]
den=p**3+p**6
diff=[(p**2*v[i]-p**3*v[(i+1)%3]+p**4*v[(i+2)%3])/den for i in range(3)]
restored={(0,0):(3*average+trace)/4}
for i,(role,j) in enumerate(pairs):
    restored[(role,role)]=(average-trace)/4+diff[i]
    restored[(0,role)]=B[i]/(4*a)+C[(i-1)%3]/(4*b)
    restored[(min(role,j),max(role,j))]=D[i]/(2*a*b)
for key,value in restored.items():
    check(s.simplify(value-S[key])==0,"exact symbolic ten-component reconstruction")

# Every permutation of four Roles is affine on GF(2)^2:
# 6 invertible 2x2 matrices *4 translations. Nonzero characters are three.
bits=(0,1)
characters=[(0,1),(1,0),(1,1)]
GL=[]
for m in itertools.product(bits,repeat=4):
    mat=((m[0],m[1]),(m[2],m[3]))
    if (m[0]*m[3]+m[1]*m[2])%2:GL.append(mat)
check(len(GL)==6,"GL2 size")
def apply(mat,v):
    return ((mat[0][0]*v[0]+mat[0][1]*v[1])%2,
            (mat[1][0]*v[0]+mat[1][1]*v[1])%2)
signed_matrices=set()
nproper=0
for mat in GL:
    for shift in itertools.product(bits,repeat=2):
        R=s.zeros(3)
        transp=((mat[0][0],mat[1][0]),(mat[0][1],mat[1][1]))
        for j,chi in enumerate(characters):
            image=apply(transp,chi)
            row=characters.index(image)
            sign=(-1)**((chi[0]*shift[0]+chi[1]*shift[1])%2)
            R[row,j]=sign
        check(R.T*R==s.eye(3),"signed character action orthogonal")
        signed_matrices.add(tuple(R))
        if R.det()==1:nproper+=1
check(len(signed_matrices)==24 and nproper==12,"full and proper four-Role images")
orbit=set()
for tuple_R in signed_matrices:
    R=s.Matrix(3,3,tuple_R)
    if R.det()==1:
        orbit.add(tuple(str(x) for x in R*s.Matrix([a,b,0])))
check(len(orbit)==12,"one golden vector 12-orbit")

# Packed symmetric basis: offdiagonal columns have factor two.
basis=[(0,0),(0,1),(0,2),(0,3),(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)]
rows=[]
for i,j in pairs:
    for sign,tau in itertools.product((1,-1),repeat=2):
        k=s.eye(4)[:,0]+sign*a*s.eye(4)[:,i]+tau*b*s.eye(4)[:,j]
        rows.append([(2 if r!=c else 1)*k[r]*k[c] for r,c in basis])
matrix=s.Matrix(rows)
check(matrix.rank()==9,"golden tetrahedral 12 null rank nine")
trow=s.Matrix([[1 if rc==(0,0) else -1 if rc[0]==rc[1] else 0 for rc in basis]])
check(matrix.col_join(trow).rank()==10,"scale/trace completes ten")
axis=[]
for i in range(1,4):
    for sign in (1,-1):
        k=s.eye(4)[:,0]+sign*s.eye(4)[:,i]
        axis.append([(2 if r!=c else 1)*k[r]*k[c] for r,c in basis])
check(s.Matrix(axis).rank()==6,"axial directions alone insufficient")

# Extra 24-point proper-cube orbit provides a stronger uniform packed l1 inverse.
C24=s.Rational(1,16)+1/(6*p**3)+1/(16*a)+1/(16*a*b)
check(float(C24)<1,"strong frame constant under one")
check(s.simplify(p-p**2-p**3)==0,"native port/gap/orbit common p^3")
print(json.dumps({"status":"PASS","exact_checks":nchecks,"role_affine_group":24,
                  "even_role_proper_group":12,"golden_null_rank":9,
                  "golden_plus_trace_rank":10,"axis_rank":6,
                  "24probe_packed_inverse_C":str(s.N(C24,16)),
                  "native_test_admission_proved":False,
                  "complete_Einstein_source_proved":False},sort_keys=True))

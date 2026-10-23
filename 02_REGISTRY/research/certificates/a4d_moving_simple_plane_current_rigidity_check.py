#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact moving-simple-plane current rigidity.

This is a structural continuation of a4d_y_slow_exact_plane_check.py.
Two neighbouring layers may have different nondegenerate spatial difference
parallelograms in the same canonical spacelike 12-plane and independent
Cayley amplitudes.  The literal full Euler equations are differentiated on
shared links.

Results:
  * every Gram/solder Euler row at a layer vanishes identically before
    imposing connection stationarity;
  * temporal-link Euler rows vanish identically;
  * spatial-link Euler is an exact two-layer current difference;
  * stationarity transports both difference vectors by one conformal 2x2 map;
  * the remaining area row forces equal amplitude squares, so the transport
    becomes SO(2) and the complete spatial Gram is preserved.

No continuum approximation or Fourier census is used.
"""
from __future__ import annotations

import sympy as sp
import a4d_y_slow_exact_plane_check as Y

I4, GEN = Y.I4, Y.GEN


def ck(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name, flush=True)


def main():
    # Current and incoming layer shapes in the canonical spacelike 12-plane.
    a,b,c,d,A,B,C,D,z,y = sp.symbols(
        "a b c d A B C D z y", real=True)
    e0=sp.Matrix([1,0,0,0])
    e3=sp.Matrix([0,0,0,1])
    u=sp.Matrix([0,a,b,0]); v=sp.Matrix([0,c,d,0])
    U0=sp.Matrix([0,A,B,0]); V0=sp.Matrix([0,C,D,0])
    current=sp.Matrix.hstack(e0,e3,e3+u,e3+v)
    previous=sp.Matrix.hstack(e0,e3,e3+U0,e3+V0)
    ck("CURRENT_COFRAME_DET", sp.factor(current.det()-(a*d-b*c))==0)
    ck("PREVIOUS_COFRAME_DET", sp.factor(previous.det()-(A*D-B*C))==0)

    J=GEN[3]  # J12
    Cz=Y.cayley_simple(J,1,z)
    Cy=Y.cayley_simple(J,1,y)
    wave_z=[Cz,I4,Y.linv(Cz),I4]
    wave_y=[Cy,I4,Y.linv(Cy),I4]

    def link(x,role):
        if role != 0:
            return I4
        wave=wave_z if x[0] >= 0 else wave_y
        return wave[sum(x)%4]

    def solder(x):
        return current if x[0] >= 0 else previous

    # Metric response at a base cell is local to that cell's simple plane.
    # It is identically zero for arbitrary neighbouring data.
    for phase in range(4):
        site=(0,phase,0,0)
        ck(f"PHASE_{phase}_ALL_16_SOLDER_ROWS_ZERO",
           Y.solder_euler(solder,link,site)==sp.zeros(4))
        ck(f"PHASE_{phase}_TEMPORAL_LINK_EULER_ZERO",
           all(Y.edge_euler(solder,link,site,0,g)==0 for g in GEN))

    # One phase suffices for the two-layer transport formulas; the other
    # phases differ only by the owned reciprocal/sign pattern.
    site=(0,0,0,0)
    rows={role:[sp.factor(Y.edge_euler(solder,link,site,role,g))
                for g in GEN] for role in (1,2,3)}

    den=(y*y+4)*(z*z+4)
    expected1=[
      -2*((y*y+4)*(a*z+2*b-c*z-2*d)
           -(z*z+4)*(A*y+2*B-C*y-2*D))/den,
      -2*((z*z+4)*(2*A-B*y-2*C+D*y)
           -(y*y+4)*(2*a-b*z-2*c+d*z))/den,
      A*D-B*C-a*d+b*c,0,0,0]
    expected2=[
      -2*((y*y+4)*(c*z+2*d)-(z*z+4)*(C*y+2*D))/den,
      -2*((z*z+4)*(2*C-D*y)-(y*y+4)*(2*c-d*z))/den,
      0,0,0,0]
    expected3=[
       2*((y*y+4)*(a*z+2*b)-(z*z+4)*(A*y+2*B))/den,
       2*((z*z+4)*(2*A-B*y)-(y*y+4)*(2*a-b*z))/den,
       0,0,0,0]
    ck("ROLE1_EXACT_CURRENT_ROWS",
       all(sp.factor(x-e)==0 for x,e in zip(rows[1],expected1)))
    ck("ROLE2_EXACT_CURRENT_ROWS",
       all(sp.factor(x-e)==0 for x,e in zip(rows[2],expected2)))
    ck("ROLE3_EXACT_CURRENT_ROWS",
       all(sp.factor(x-e)==0 for x,e in zip(rows[3],expected3)))

    # The K1/K2 rows on roles 3 and 2 transport the two difference vectors
    # by the same conformal map.
    M=lambda q: sp.Matrix([[q,2],[2,-q]])
    R=sp.simplify(M(z)*M(y)/(y*y+4))
    ck("TRANSPORT_CONFORMAL_GRAM",
       sp.simplify(R.T*R-(z*z+4)/(y*y+4)*sp.eye(2))==sp.zeros(2))
    ck("TRANSPORT_DETERMINANT",
       sp.factor(R.det()-(z*z+4)/(y*y+4))==0)

    prev_u=sp.Matrix([A,B]); prev_v=sp.Matrix([C,D])
    cur_u=sp.simplify(R*prev_u); cur_v=sp.simplify(R*prev_v)
    transport_sub={a:cur_u[0],b:cur_u[1],c:cur_v[0],d:cur_v[1]}
    ck("ROLE2_ROLE3_ZERO_ON_CONFORMAL_TRANSPORT",
       all(sp.factor(rows[r][j].subs(transport_sub))==0
           for r in (2,3) for j in range(6)))

    area0=A*D-B*C
    area=a*d-b*c
    transported_area=sp.factor(area.subs(transport_sub))
    ck("TRANSPORT_AREA_SCALING",
       sp.factor(transported_area-(z*z+4)/(y*y+4)*area0)==0)
    # Combining the transport rows with the independent role-1 K3 area row
    # gives (z^2-y^2)*area0=0 after clearing the positive denominators.
    ck("AREA_ROW_FORCES_EQUAL_AMPLITUDE_SQUARES",
       sp.factor((transported_area-area0)*(y*y+4)
                 -(z*z-y*y)*area0)==0)

    # Nondegenerate current layers therefore have y=+/- z.
    Rplus=sp.simplify(R.subs(y,z))
    Rminus=sp.simplify(R.subs(y,-z))
    ck("SAME_SIGN_TRANSPORT_IDENTITY", Rplus==sp.eye(2))
    ck("OPPOSITE_SIGN_TRANSPORT_SO2",
       sp.simplify(Rminus.T*Rminus)==sp.eye(2)
       and sp.factor(Rminus.det()-1)==0)

    # Both exact alternatives solve every spatial link row.
    for label,yy,RR in (("PLUS",z,Rplus),("MINUS",-z,Rminus)):
        sub={y:yy,
             a:(RR*prev_u)[0], b:(RR*prev_u)[1],
             c:(RR*prev_v)[0], d:(RR*prev_v)[1]}
        ck(f"{label}_ALL_SPATIAL_EULER_ROWS_ZERO",
           all(sp.factor(rows[r][j].subs(sub))==0
               for r in (1,2,3) for j in range(6)))
        Gprev=sp.Matrix.hstack(prev_u,prev_v).T*sp.Matrix.hstack(prev_u,prev_v)
        Gcur=sp.Matrix.hstack(sp.Matrix([sub[a],sub[b]]),
                             sp.Matrix([sub[c],sub[d]])).T*sp.Matrix.hstack(
                             sp.Matrix([sub[a],sub[b]]),
                             sp.Matrix([sub[c],sub[d]]))
        ck(f"{label}_SPATIAL_DIFFERENCE_GRAM_PRESERVED",
           sp.simplify(Gcur-Gprev)==sp.zeros(2))


    # The opposite-sign transition is exactly the same internal Cayley
    # rotation applied to the whole spatial triad, not a new physical Gram.
    qbase=sp.Matrix(sp.symbols("q0:4", real=True))
    prev_general=sp.Matrix.hstack(e0,qbase,qbase+U0,qbase+V0)
    G4=sp.eye(4)
    G4[1,1],G4[1,2]=Rminus[0,0],Rminus[0,1]
    G4[2,1],G4[2,2]=Rminus[1,0],Rminus[1,1]
    current_general=sp.simplify(G4*prev_general)
    Cyminus=Y.cayley_simple(J,1,-z)
    wave_minus=[Cyminus,I4,Y.linv(Cyminus),I4]
    def link_general(x,role):
        if role != 0:
            return I4
        wave=wave_z if x[0] >= 0 else wave_minus
        return wave[sum(x)%4]
    def solder_general(x):
        return current_general if x[0] >= 0 else prev_general
    ck("OPPOSITE_SIGN_IS_FULL_SPATIAL_LORENTZ_TRANSPORT",
       all(sp.factor(Y.edge_euler(solder_general,link_general,(0,0,0,0),role,g))==0
           for role in (1,2,3) for g in GEN))
    Gprev=sp.simplify(prev_general[:,1:].T*Y.ETA*prev_general[:,1:])
    Gcurr=sp.simplify(current_general[:,1:].T*Y.ETA*current_general[:,1:])
    ck("OPPOSITE_SIGN_FULL_SPATIAL_GRAM_PRESERVED",
       sp.simplify(Gcurr-Gprev)==sp.zeros(3))

    print("RESULT A4D-MOVING-SIMPLE-PLANE-CURRENT-RIGIDITY-CERTIFIED",flush=True)
    print("SCOPE canonical one-coordinate spacelike difference-plane family; "
          "arbitrary neighbouring time columns remain free by the parent theorem.",flush=True)


if __name__=="__main__":
    main()

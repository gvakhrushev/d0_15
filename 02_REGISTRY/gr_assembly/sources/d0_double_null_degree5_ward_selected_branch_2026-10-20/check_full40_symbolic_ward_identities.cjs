#!/usr/bin/env node
"use strict";
/*
 * Coefficientwise Laurent-polynomial Ward checks for the original flat
 * 40-row Palatini symbol. Integer coefficients are used throughout; the
 * link Hessian is stored doubled to clear its sole factor 1/2.
 *
 * Together with check_full40_schur_rank_modular.cjs, this makes the generic
 * rank argument exact: ten independent analytic Ward directions bound the
 * Schur rank above by six, and one F_1009 rank-six witness bounds it below.
 * This is a linearized geometric statement, not native price selection,
 * nonlinear closure, or continuum recovery.
 */

const N = 4;
const PAIRS = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]];
const EXP_ZERO = [0, 0, 0, 0];

function clean(p) {
  for (const [k, v] of p) if (v === 0n) p.delete(k);
  return p;
}
function key(e) { return e.join(","); }
function parse(k) { return k.split(",").map(Number); }
function constant(n) {
  const v = BigInt(n);
  return v === 0n ? new Map() : new Map([[key(EXP_ZERO), v]]);
}
function monomial(coefficient, exponents) {
  const c = BigInt(coefficient);
  return c === 0n ? new Map() : new Map([[key(exponents), c]]);
}
function pAdd(a, b) {
  const out = new Map(a);
  for (const [k, v] of b) out.set(k, (out.get(k) || 0n) + v);
  return clean(out);
}
function pNeg(a) { return new Map([...a].map(([k, v]) => [k, -v])); }
function pSub(a, b) { return pAdd(a, pNeg(b)); }
function pMul(a, b) {
  const out = new Map();
  for (const [ka, va] of a) for (const [kb, vb] of b) {
    const ea = parse(ka), eb = parse(kb);
    const k = key(ea.map((x, i) => x + eb[i]));
    out.set(k, (out.get(k) || 0n) + va * vb);
  }
  return clean(out);
}
function pScale(a, n) {
  const c = BigInt(n);
  return c === 0n ? new Map() : clean(new Map([...a].map(([k, v]) => [k, v * c])));
}
function pEqual(a, b) {
  clean(a); clean(b);
  return a.size === b.size && [...a].every(([k, v]) => b.get(k) === v);
}
function pMatrix(rows, cols, fill = constant(0)) {
  return Array.from({ length: rows }, () => Array.from({ length: cols }, () => new Map(fill)));
}
function mAdd(A, B) { return A.map((r, i) => r.map((x, j) => pAdd(x, B[i][j]))); }
function mSub(A, B) { return A.map((r, i) => r.map((x, j) => pSub(x, B[i][j]))); }
function mScale(A, n) { return A.map(r => r.map(x => pScale(x, n))); }
function mMul(A, B) {
  return A.map((row, i) => B[0].map((_, j) => {
    let out = constant(0);
    for (let k = 0; k < B.length; k++) out = pAdd(out, pMul(A[i][k], B[k][j]));
    return out;
  }));
}
function mApply(A, v) {
  return A.map(row => row.reduce((out, x, i) => pAdd(out, pMul(x, v[i])), constant(0)));
}
function mTranspose(A) { return A[0].map((_, j) => A.map(r => r[j])); }
function invertVariables(A) {
  return A.map(row => row.map(poly => new Map([...poly].map(([k, v]) => [key(parse(k).map(x => -x)), v]))));
}
function allZero(v) { return v.every(x => x.size === 0); }
function unitMatrix() {
  return Array.from({ length: N }, (_, i) => Array.from({ length: N }, (_, j) => constant(i === j ? 1 : 0)));
}
const ZERO_MATRIX = () => pMatrix(N, N);
function basis(a, b) {
  return Array.from({ length: N }, (_, i) => Array.from({ length: N }, (_, j) => constant(i === a && j === b ? 1 : 0)));
}
const ETA = [
  [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1],
].map(row => row.map(constant));
const GENS = PAIRS.map(([i, j]) => mMul(mSub(basis(i, j), basis(j, i)), ETA));
function epsilon4(v) {
  if (new Set(v).size !== 4) return 0;
  let sign = 1;
  for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) if (v[i] > v[j]) sign = -sign;
  return sign;
}
function pDot(position) { return monomial(1, position); }
function shift(position, dir, amount = 1) {
  return position.map((x, i) => x + (i === dir ? amount : 0));
}
function pairing(F, u, v, R) {
  const A = mMul(R, ETA);
  let total = constant(0);
  for (let a = 0; a < N; a++) for (let b = a + 1; b < N; b++) {
    const [c, d] = [0, 1, 2, 3].filter(k => k !== a && k !== b);
    const area = pSub(pMul(F[a][u], F[b][v]), pMul(F[b][u], F[a][v]));
    total = pAdd(total, pScale(pMul(area, A[c][d]), epsilon4([a, b, c, d])));
  }
  return total;
}
function pairCoframeDerivative(a, mu, u, v, R) {
  if (mu !== u && mu !== v) return constant(0);
  const F = unitMatrix();
  for (let b = 0; b < N; b++) F[b][mu] = constant(a === b ? 1 : 0);
  return pairing(F, u, v, R);
}
function linkLinear(axis, inputGenerator) {
  const point = [0, 0, 0, 0];
  const out = Array.from({ length: 24 }, () => constant(0));
  const field = (position, direction) => direction === axis
    ? mScale(GENS[inputGenerator], 1).map(row => row.map(x => pMul(x, pDot(position))))
    : ZERO_MATRIX();
  for (let direction = 0; direction < 4; direction++) for (let j = 0; j < 6; j++) {
    let value = constant(0);
    const X = GENS[j];
    for (const [r, t] of PAIRS) {
      if (direction !== r && direction !== t) continue;
      const other = direction === r ? t : r;
      const [u, v] = [0, 1, 2, 3].filter(k => k !== r && k !== t);
      for (const base of [point, shift(point, other, -1)]) {
        const edges = [
          [base, r, 1], [shift(base, r), t, 1],
          [shift(base, t), r, -1], [base, t, -1],
        ];
        const W = edges.map(([position, dir, sign]) => mScale(field(position, dir), sign));
        const P1 = W.reduce(mAdd, ZERO_MATRIX());
        let dP0 = ZERO_MATRIX(), dP1 = ZERO_MATRIX();
        for (let k = 0; k < 4; k++) {
          const [position, dir, sign] = edges[k];
          if (dir !== direction || !position.every((x, i) => x === point[i])) continue;
          const d0 = mScale(X, sign);
          const d1 = sign === 1 ? mMul(X, field(position, dir)) : mMul(field(position, dir), X);
          dP0 = mAdd(dP0, d0);
          let term = d1;
          for (let l = 0; l < k; l++) term = mAdd(term, mMul(W[l], d0));
          for (let l = k + 1; l < 4; l++) term = mAdd(term, mMul(d0, W[l]));
          dP1 = mAdd(dP1, term);
        }
        // Store twice the derivative, keeping every Laurent coefficient integral.
        const twiceDR = mSub(mScale(dP1, 2), mAdd(mMul(P1, dP0), mMul(dP0, P1)));
        value = pAdd(value, pScale(pairing(unitMatrix(), u, v, twiceDR), epsilon4([r, t, u, v])));
      }
    }
    out[6 * direction + j] = value;
  }
  return out;
}
function symbols() {
  const L2 = pMatrix(24, 24), B = pMatrix(24, 16), C = pMatrix(16, 24);
  for (let j = 0; j < 24; j++) {
    const column = linkLinear(Math.floor(j / 6), j % 6);
    for (let i = 0; i < 24; i++) L2[i][j] = column[i];
  }
  for (let direction = 0; direction < 4; direction++) for (let j = 0; j < 6; j++) {
    for (const [r, t] of PAIRS) {
      if (direction !== r && direction !== t) continue;
      const other = direction === r ? t : r;
      const [u, v] = [0, 1, 2, 3].filter(k => k !== r && k !== t);
      const eps = epsilon4([r, t, u, v]);
      const zInv = monomial(1, [0, 0, 0, 0].map((_, i) => i === other ? -1 : 0));
      const coefficient = pScale(pSub(constant(1), zInv), eps * (direction === r ? 1 : -1));
      for (let a = 0; a < 4; a++) for (let mu = 0; mu < 4; mu++) {
        B[6 * direction + j][4 * a + mu] = pAdd(
          B[6 * direction + j][4 * a + mu],
          pMul(coefficient, pairCoframeDerivative(a, mu, u, v, GENS[j])),
        );
      }
    }
  }
  for (const [r, t] of PAIRS) {
    const [u, v] = [0, 1, 2, 3].filter(k => k !== r && k !== t);
    for (const direction of [r, t]) for (let j = 0; j < 6; j++) {
      const factor = direction === r
        ? pSub(constant(1), monomial(1, [0, 0, 0, 0].map((_, i) => i === t ? 1 : 0)))
        : pSub(monomial(1, [0, 0, 0, 0].map((_, i) => i === r ? 1 : 0)), constant(1));
      const R = GENS[j].map(row => row.map(x => pMul(x, factor)));
      for (let a = 0; a < 4; a++) for (let mu = 0; mu < 4; mu++) {
        C[4 * a + mu][6 * direction + j] = pAdd(
          C[4 * a + mu][6 * direction + j],
          pScale(pairCoframeDerivative(a, mu, u, v, R), epsilon4([r, t, u, v])),
        );
      }
    }
  }
  return { L2, B, C };
}
function audit() {
  const { L2, B, C } = symbols();
  const B2 = mScale(B, 2);
  const gradientWard = [];
  for (let alpha = 0; alpha < 4; alpha++) {
    const coframeGradient = Array.from({ length: 16 }, (_, i) =>
      Math.floor(i / 4) === alpha
        ? pSub(constant(1), monomial(1, [0, 0, 0, 0].map((_, j) => j === i % 4 ? -1 : 0)))
        : constant(0));
    gradientWard.push(allZero(mApply(B, coframeGradient)));
  }
  const lorentzWard = [];
  for (let k = 0; k < 6; k++) {
    const coframe = GENS[k].flat();
    const link = Array.from({ length: 24 }, (_, i) => {
      const direction = Math.floor(i / 6), generator = i % 6;
      return generator === k
        ? pSub(constant(1), monomial(1, [0, 0, 0, 0].map((_, j) => j === direction ? 1 : 0)))
        : constant(0);
    });
    lorentzWard.push(allZero(mApply(L2, link).map((x, i) => pAdd(x, mApply(B2, coframe)[i]))));
    lorentzWard.push(allZero(mApply(C, link)));
  }
  const adjointL = L2.map((_, i) => L2.map(r => r[i]));
  const adjointB = mTranspose(B);
  const adjointChecks = [
    adjointL.every((row, i) => row.every((x, j) => pEqual(x, invertVariables(L2)[i][j]))),
    C.every((row, i) => row.every((x, j) => pEqual(x, invertVariables(adjointB)[i][j]))),
  ];
  const checks = [...gradientWard, ...lorentzWard, ...adjointChecks];
  if (!checks.every(Boolean)) throw new Error(`symbolic Ward failure: ${JSON.stringify({gradientWard, lorentzWard, adjointChecks})}`);
  return {
    status: "PASS_COEFFICIENTWISE_LAURENT_WARDS",
    coefficientRing: "Z[z_u^±1,z_v^±1,z_x^±1,z_y^±1]",
    exactChecks: checks.length,
    backwardCoframeGradientWards: gradientWard.length,
    localLorentzLinkAndCoframeWards: 6,
    variationalAdjointIdentities: ["L(z)^T=L(z^-1)", "C(z)=B(z^-1)^T"],
    linkHessianScale: "L2=2*L clears the only 1/2; B2=2*B in the Lorentz Ward",
    scope: "exact flat linearized Palatini symbol only; rank lower bound comes from the separate F_1009 witness; no native price or nonlinear/continuum closure",
  };
}
if (require.main === module) console.log(JSON.stringify(audit(), null, 2));
module.exports = { audit, symbols };

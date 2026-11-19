#!/usr/bin/env node
"use strict";
/*
 * Exact characteristic-zero TT modes of the original full40 Schur symbol.
 * The input Laurent matrices are built coefficientwise over Z by
 * check_full40_symbolic_ward_identities.cjs and evaluated exactly over Q.
 *
 * At each listed two-periodic null wave, this verifies rank(S)=4, the two
 * transverse-traceless coframes are null, and the ten Lorentz/backward-
 * gradient gauge vectors plus those two modes have rank 12. Thus the
 * 12-dimensional kernel at these points is exactly gauge + two TT modes.
 * It does not classify all characteristic directions or the full dispersion.
 */

const { symbols } = require("./check_full40_symbolic_ward_identities.cjs");

function gcd(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b !== 0n) [a, b] = [b, a % b];
  return a || 1n;
}
function Q(n, d = 1n) {
  n = BigInt(n); d = BigInt(d);
  if (d < 0n) [n, d] = [-n, -d];
  const g = gcd(n, d);
  return { n: n / g, d: d / g };
}
const qAdd = (a, b) => Q(a.n * b.d + b.n * a.d, a.d * b.d);
const qNeg = a => Q(-a.n, a.d);
const qSub = (a, b) => qAdd(a, qNeg(b));
const qMul = (a, b) => Q(a.n * b.n, a.d * b.d);
const qDiv = (a, b) => Q(a.n * b.d, a.d * b.n);
const zero = () => Q(0);

function evaluate(poly, z) {
  let total = zero();
  for (const [monomial, coefficient] of poly) {
    let term = Q(coefficient);
    const exponents = monomial.split(",").map(Number);
    for (let i = 0; i < 4; i++) {
      let base = Q(z[i]);
      let exponent = exponents[i];
      if (exponent < 0) { base = qDiv(Q(1), base); exponent = -exponent; }
      for (let j = 0; j < exponent; j++) term = qMul(term, base);
    }
    total = qAdd(total, term);
  }
  return total;
}
function matrixRank(input) {
  const A = input.map(row => row.map(x => Q(x.n, x.d)));
  let rank = 0;
  for (let col = 0; col < A[0].length && rank < A.length; col++) {
    let pivot = rank;
    while (pivot < A.length && A[pivot][col].n === 0n) pivot++;
    if (pivot === A.length) continue;
    [A[pivot], A[rank]] = [A[rank], A[pivot]];
    const divisor = A[rank][col];
    for (let j = col; j < A[rank].length; j++) A[rank][j] = qDiv(A[rank][j], divisor);
    for (let i = 0; i < A.length; i++) if (i !== rank && A[i][col].n !== 0n) {
      const factor = A[i][col];
      for (let j = col; j < A[i].length; j++) A[i][j] = qSub(A[i][j], qMul(factor, A[rank][j]));
    }
    rank++;
  }
  return rank;
}
function solve(A0, B0) {
  const n = A0.length, k = B0[0].length;
  const A = A0.map((row, i) => [...row.map(x => Q(x.n, x.d)), ...B0[i].map(x => Q(x.n, x.d))]);
  for (let col = 0; col < n; col++) {
    let pivot = col;
    while (pivot < n && A[pivot][col].n === 0n) pivot++;
    if (pivot === n) throw new Error(`singular link block at column ${col}`);
    [A[pivot], A[col]] = [A[col], A[pivot]];
    const divisor = A[col][col];
    for (let j = col; j < n + k; j++) A[col][j] = qDiv(A[col][j], divisor);
    for (let i = 0; i < n; i++) if (i !== col && A[i][col].n !== 0n) {
      const factor = A[i][col];
      for (let j = col; j < n + k; j++) A[i][j] = qSub(A[i][j], qMul(factor, A[col][j]));
    }
  }
  return A.map(row => row.slice(n));
}
function apply(A, v) {
  return A.map(row => row.reduce((sum, x, i) => qAdd(sum, qMul(x, v[i])), zero()));
}
function basis(a, b) {
  return Array.from({ length: 4 }, (_, i) => Array.from({ length: 4 }, (_, j) => Q(i === a && j === b ? 1 : 0)));
}
const ETA = [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]];
function multiply4(A, B) {
  return A.map(row => B[0].map((_, j) => row.reduce((s, x, k) => s + Number(x) * Number(B[k][j]), 0)));
}
const PAIRS = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]];
const GENS = PAIRS.map(([i, j]) => {
  const A = basis(i, j).map((row, r) => row.map((x, c) => Number(x.n) - Number(basis(j, i)[r][c].n)));
  return multiply4(A, ETA).flat().map(Q);
});
function auditAt(z, symbol) {
  const L2 = symbol.L2.map(row => row.map(p => evaluate(p, z)));
  const B = symbol.B.map(row => row.map(p => qMul(Q(2), evaluate(p, z))));
  const C = symbol.C.map(row => row.map(p => evaluate(p, z)));
  const linkRank = matrixRank(L2);
  if (linkRank !== 24) throw new Error(`link block rank ${linkRank} at ${z}`);
  // L2=2L, so L2^{-1}(2B)=L^{-1}B.
  const X = solve(L2, B);
  const S = C.map(row => Array.from({ length: 16 }, (_, j) =>
    qNeg(row.reduce((sum, x, i) => qAdd(sum, qMul(x, X[i][j])), zero()))));
  const plus = Array.from({ length: 16 }, (_, i) => Q(i === 10 ? 1 : i === 15 ? -1 : 0));
  const cross = Array.from({ length: 16 }, (_, i) => Q(i === 11 || i === 14 ? 1 : 0));
  const ttResiduals = [apply(S, plus), apply(S, cross)];
  if (ttResiduals.some(v => v.some(x => x.n !== 0n))) throw new Error(`TT vector not null at ${z}`);
  const gradients = Array.from({ length: 4 }, (_, a) => Array.from({ length: 16 }, (_, i) =>
    Math.floor(i / 4) === a ? qSub(Q(1), qDiv(Q(1), Q(z[i % 4]))) : zero()));
  const gaugeNulls = [...GENS, ...gradients].every(v => apply(S, v).every(x => x.n === 0n));
  const gaugeFrame = Array.from({ length: 16 }, (_, i) =>
    [...GENS.map(v => v[i]), ...gradients.map(v => v[i])]);
  const frame = gaugeFrame.map((row, i) => [...row, plus[i], cross[i]]);
  const schurRank = matrixRank(S), gaugeRank = matrixRank(gaugeFrame), frameRank = matrixRank(frame);
  if (!gaugeNulls || schurRank !== 4 || frameRank !== gaugeRank + 2 || frameRank > 12) {
    throw new Error(`unexpected ranks at ${z}: Schur=${schurRank}, gauge=${gaugeRank}, gauge+TT=${frameRank}`);
  }
  return { z, linkRank, schurRank, kernelDimension: 12, gaugeRank,
    gaugePlusTTDimension: frameRank, additionalKernelDirections: 12 - frameRank,
    gaugeNulls, ttPlusNull: true, ttCrossNull: true, exactField: "Q" };
}
function audit() {
  const symbol = symbols();
  const results = [auditAt([-1, 1, 1, 1], symbol), auditAt([1, -1, 1, 1], symbol)];
  return {
    status: "PASS_EXACT_RATIONAL_TWO_TT_NULL_POLARIZATIONS",
    carrier: "two-periodic original lattice; one null Role direction at a time",
    polarizationBasis: "e^2_x-e^3_y and e^2_y+e^3_x",
    results,
    scope: "two exact discrete null-wave points only; not the full characteristic variety, dispersion, nonlinear roots, or native physical-price selection",
  };
}
if (require.main === module) console.log(JSON.stringify(audit(), null, 2));
module.exports = { audit };

#!/usr/bin/env node
"use strict";
// D0 #334: scoped algebraic check of a COMPLETE cost-marked terminal 0/10 reporter.
// Test model, NOT a declaration that Book03 selects this cut, mark, or Info.
const assert = require("node:assert/strict");
const phi = (1 + Math.sqrt(5)) / 2, p = 1 / phi, zeta = 2 ** -20;
const L = 4 * p ** 3;
const r0 = 1 - (1 - zeta * L) * (1 - zeta * L * (1 + p ** 6));
const close = (a, b, eps = 1e-11) => Math.abs(a - b) <= eps * (1 + Math.abs(b));
function book(r, opts = {}) {
  const {
    mark = Math.log(phi), ready = 4 / 5, return1 = 1 / 2,
    return2 = 1 / 4, cEarly = 1, c0 = 1, c1 = 2, common = 0
  } = opts;
  const v = (1 - ready) * Math.exp(-mark * (cEarly + common));
  const u0 = ready * Math.exp(-mark * (c0 + common));
  const u1 = ready * Math.exp(-mark * (c1 + common));
  const N = v + (1 - r) * u0 + r * u1;
  const b = [return1 * v, return2 * v];
  assert.ok(N > 0 && b.every(x => x >= 0 && x <= N));
  const J = -b.reduce((sum, x) => sum + Math.log1p(-zeta * (1 - x / N)), 0);
  const Dr = b.reduce((sum, x) =>
    sum + zeta * (u1 - u0) * x /
      (N * ((1 - zeta) * N + zeta * x)), 0);
  return { J, Dr, N, b, v, u0, u1 };
}
assert.ok(close(p + p * p, 1, 1e-14));
assert.ok(r0 > 0 && r0 < 1 / 2);
const measured = book(r0);
assert.ok(close(book(r0, {mark: 0}).N, 1, 1e-14));
const finiteStep = 1e-4;
const fd = (book(r0 + finiteStep).J - book(r0 - finiteStep).J) / (2 * finiteStep);
assert.ok(close(fd, measured.Dr, 1e-11));
assert.ok(measured.Dr < 0);
assert.equal(book(r0, {mark: 0}).Dr, 0); // no cost mark
assert.equal(book(r0, {c1: 1}).Dr, 0); // equal report net charges
assert.equal(book(r0, {return1: 0, return2: 0}).Dr, 0); // no early return
const shifted = book(r0, {common: 7});
assert.ok(close(shifted.J, measured.J, 1e-13));
assert.ok(close(shifted.Dr, measured.Dr, 1e-13));
// The different report cut is explicitly NOT the fixed initialized-work cut.
function reportCut(r, opts={}) {
  const {mark = Math.log(phi), ready = 4 / 5} = opts;
  const v = (1 - ready) * Math.exp(-mark);
  const u0 = ready * Math.exp(-mark);
  const u1 = ready * Math.exp(-2 * mark);
  const N = v + u0 * (1 - r) + u1 * r;
  const T = r * u1 / N;
  const J = -2 * Math.log1p(-zeta * (1 - T));
  const Dr = -2 * zeta * u1 * (v + u0) /
    (N * N * (1 - zeta + zeta * T));
  return {J, Dr};
}
const rep = reportCut(r0);
const repfd = (reportCut(r0 + finiteStep).J - reportCut(r0 - finiteStep).J)/(2 * finiteStep);
assert.ok(close(repfd, rep.Dr, 1e-11));
assert.ok(rep.Dr < 0);
const hPrime = Math.log((1-r0)/r0)/Math.log(phi);
assert.ok(hPrime>0);
// Original 0/10 CQ slope is 1-hPrime, also negative at r0.
assert.ok(1-hPrime<0);
console.log(JSON.stringify({
  status: "SCOPED_PASS", checks: 12, phi, p, zeta, r0, mark: "ln(phi)",
  model: {ready: 4/5, early_cost: 1, report_costs: [1,2],
          early_return_spectrum_unmarked: [(1-4/5)/2,(1-4/5)/4]},
  initialized_cut: {J: measured.J, source: measured.Dr, finite_difference: fd},
  report_cut_ALTERNATIVE: {J: rep.J, source: rep.Dr},
  controls: ["unmarked zero","equal net report charges zero",
             "vanishing early return zero", "common full-charge shift cancels",
             "true r0 and native 0/10 CQ slope nonzero"],
  physics_status: "GR_closed=false; actual Book03 choice, Info, heat, clock and input admission open"
}, null, 2));

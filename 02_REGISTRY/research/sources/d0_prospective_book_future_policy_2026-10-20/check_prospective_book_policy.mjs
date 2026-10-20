// Original D0 K(9,11,13) prospective finite-history Book continuation.
// Exact integer graph/history counts; finite soft Bellman and field sources;
// conditional Q8 Golden verification costs. Research, NOT full G0 admission.
function check(ok, what) {
  if (!ok) throw new Error("FAIL: " + what);
}
function near(x, y, err, what) {
  check(Math.abs(x - y) < err, what + ": " + x + " != " + y);
}
const phi = (1 + Math.sqrt(5)) / 2;
const p = 1 / phi;
const ell = Math.log(phi);
const group = Array.from({ length: 33 }, (_, u) => u < 9 ? 0 : (u < 20 ? 1 : 2));
const edge = Array.from({ length: 33 }, (_, u) =>
  Array.from({ length: 33 }, (_, v) => Number(group[u] !== group[v])));
let directed = 0, n2 = 0, n3 = 0, flipped3 = 0;
let anchored3 = 0, anchoredFlipped3 = 0;
const flipped = (u, v) => (u === 0 && v === 20) || (u === 20 && v === 0);
for (let u = 0; u < 33; u++) {
  for (let v = 0; v < 33; v++) {
    if (!edge[u][v]) continue;
    directed++;
    if (edge[v][u]) n2++;
    for (let w = 0; w < 33; w++) {
      if (!(edge[v][w] && edge[w][u])) continue;
      n3++;
      if (u === 0) anchored3++;
      const odd = Number(flipped(u,v)) + Number(flipped(v,w)) + Number(flipped(w,u));
      check(odd <= 1, "simple triangle one central flip");
      if (odd) {
        flipped3++;
        if (u === 0) anchoredFlipped3++;
      }
    }
  }
}
check(directed === 718 && n2 === 718 && n3 === 7722, "whole original support");
check(flipped3 === 66 && anchored3 === 286 && anchoredFlipped3 === 22,
  "actual single central edge Q8 sign and rooted A0 triangles");

// Every length-N original cost-one path has the SAME Book scalar weight p^N.
// Its future partition counts obey original three-zone adjacency M, exactly.
const M = [[0n,11n,13n],[9n,0n,13n],[9n,11n,0n]];
const futureCounts = [[1n,1n,1n]];
for (let n = 1; n <= 32; n++) {
  const prev = futureCounts[n - 1];
  futureCounts.push(M.map(row => row.reduce((s, v, k) => s + v * prev[k], 0n)));
}
check(futureCounts[1].map(String).join(",") === "24,22,20", "first native futures");
check(futureCounts[2].map(String).join(",") === "502,476,458", "second native futures");

// Perron future: bulk limit of these finite boundary-neutral path counts;
// no separately guessed uniform row-normalized random walk.
let r = [1,1,1], rho = 0;
for (let k = 0; k < 180; k++) {
  const mr = M.map(row => row.reduce((s, x, j) => s + Number(x) * r[j], 0));
  rho = mr[0] / r[0];
  r = mr.map(x => x / mr[0]);
}
near(rho**3 - 359*rho - 2574, 0, 1e-8, "ORIGINAL cubic");
const AB = n => 11 * Number(futureCounts[n-1][1]) / Number(futureCounts[n][0]);
const ABbulk = 11 * r[1] / (rho * r[0]);
near(AB(32), ABbulk, 5e-10, "bulk native Doob AB");
check(Math.abs(AB(1) - AB(2)) > .02, "finite different horizons NOT projective");
check(Math.abs(AB(1) - ABbulk) > .01, "naive degree walk NOT Perron law");

const clockPressure = Math.log(p * rho) / ell;
near(clockPressure, 5.408037229516196, 1e-10, "original scalar native clock pressure");
check(p * rho > 1, "all-cutoff raw infinite Book sum diverges");
check(p * rho * phi**-(clockPressure+0.01) < 1, "greater work makes raw-depth sum converge");
check(p * rho * phi**-(clockPressure-0.01) > 1, "smaller work cannot normalize all depths");

// Test moving ORIGINAL primitive edge Cost; all supported costs remain >=1.
const base = (u,v) => 1.12 + ((u*7+v*11)%7)/1000;
const a = (u,v) => Number(u === 0 && v === 9);
function recurse(theta, depth) {
  let Z = Array(33).fill(1);
  let A = Array(33).fill(0);
  let B = Array(33).fill(0);
  const levels = [{Z,A,B}];
  for (let n = 1; n <= depth; n++) {
    const z1 = Array(33).fill(0), a1 = Array(33).fill(0), b1 = Array(33).fill(0);
    for (let u=0; u<33; u++) for (let v=0; v<33; v++) if (edge[u][v]) {
      const d = a(u,v), weight = phi**-(base(u,v)+theta*d);
      z1[u] += weight * Z[v];
      a1[u] += weight * (d * Z[v] + A[v]);
      b1[u] += weight * (d*d * Z[v] + 2*d*A[v] + B[v]);
    }
    Z = z1; A = a1; B = b1;
    levels.push({Z,A,B});
  }
  return levels;
}
for (const theta of [-0.02,0,0.02])
  for (let u=0; u<33; u++) for (let v=0; v<33; v++)
    if (edge[u][v]) check(base(u,v)+theta*a(u,v)>=1, "ActionProtocol Cost floor");
const depth = 4, R = recurse(0,depth);
const Z = R[depth].Z[0], V = -Math.log(Z)/ell;
const source1 = R[depth].A[0]/Z;
const variance = R[depth].B[0]/Z - source1**2;
const source2 = -ell * variance;
let totalQ = 0, wrongAction = 0, KL = 0;
const outgoing = edge[0].reduce((s,x)=>s+x,0);
for (let v=0; v<33; v++) if (edge[0][v]) {
  const q = phi**-base(0,v) * R[depth-1].Z[v] / Z;
  const wrong = 1/outgoing;
  totalQ += q;
  const continuationValue = -Math.log(R[depth-1].Z[v])/ell;
  wrongAction += wrong*(base(0,v)+continuationValue)
    + wrong*Math.log(wrong)/ell;
  KL += wrong*Math.log(wrong/q)/ell;
}
near(totalQ,1,1e-12,"one-step complete future normalizer");
near(wrongAction,V+KL,1e-11,"finite positive Cost-minus-counting-Info KL identity");
check(KL > 0, "strict uniqueness among alternative next-step probability vectors");
const h = .001, vplus = -Math.log(recurse(h,depth)[depth].Z[0])/ell;
const vminus = -Math.log(recurse(-h,depth)[depth].Z[0])/ell;
near((vplus-vminus)/(2*h),source1,2e-7,"true moving normalized first source");
near((vplus-2*V+vminus)/h**2,source2,3e-6,"full normalized covariance second source");
check(variance>0 && source2<0,"real original edge-price response");

// THREE genuine Q8 verification tasks, distinct controller/clock obligations.
// Book 8440: 718 backtracks at p^3 and 7722 triangles at p^5.
// One changed undirected a0-c0 sheet affects 66 based native triangles.
const qTarget = 4*p**3;
const qAnchor = qTarget*anchoredFlipped3/anchored3;
const qPassive = flipped3*qTarget*p**5/(n2*p**3+n3*p**5);
near(qAnchor,qTarget/13,1e-14,"middle rooted-three-tick task");
const ratioAnchorPassive=qAnchor/qPassive;
const ratioTargetAnchor=qTarget/qAnchor;
near(ratioAnchorPassive,9+(359/429)*phi**2,1e-11,"passive-to-rooted full-cost threshold");
near(ratioTargetAnchor,13,1e-12,"rooted-to-targeted full-cost threshold");
near(qTarget/qPassive,117+(359/33)*phi**2,1e-11,"owned original two-stage ratio");
const maxTrials=(q,miss)=>Math.ceil(Math.log(miss)/Math.log1p(-q));
check(maxTrials(qPassive,0.01)===708
  && maxTrials(qAnchor,0.01)===62
  && maxTrials(qTarget,0.01)===2,"0.01 complete-attempt cap");
check(maxTrials(qPassive,1e-6)===2122
  && maxTrials(qAnchor,1e-6)===184
  && maxTrials(qTarget,1e-6)===5,"1e-6 complete-attempt cap");

// Complete ORIGINAL finite future Cost–Info ledger and its local stage cocycle.
// Each equal-cost canonical path has probability 1/count under a fixed cut.
const count4 = Number(futureCounts[4][0]);
check(count4 === 241994, "exact original A0 depth-4 future count");
const canonicalCodeEntropy = Math.log(count4)/ell;
const canonicalValue = 4-canonicalCodeEntropy;
near(canonicalValue,-Math.log(p**4*count4)/ell,1e-11,
  "canonical entire-history code/Cost equality");
const pathRecord = [0,9,0,20,0];
let pathCode = 0, pathCost = 0, pathBorn = 1, pathRaw = 1;
for (let i=0; i<depth; i++) {
  const u=pathRecord[i], v=pathRecord[i+1], remaining=depth-i;
  check(edge[u][v]===1, "chronological actual K913 path allowed");
  const weight = phi**-base(u,v);
  const stage = weight*R[remaining-1].Z[v]/R[remaining].Z[u];
  const stageSurprisal = -Math.log(stage)/ell;
  const stagePotentialChange = -Math.log(R[remaining-1].Z[v])/ell
    + Math.log(R[remaining].Z[u])/ell;
  near(stageSurprisal,base(u,v)+stagePotentialChange,1e-11,
    "complete future source/cost coboundary at native stage");
  pathBorn *= stage;
  pathRaw *= weight;
  pathCode += stageSurprisal;
  pathCost += base(u,v);
}
near(pathBorn,pathRaw/Z,1e-13,"true complete cylinder exact telescope");
near(pathCost-pathCode,V,1e-11,"all-history exact Cost-minus-counting-Info");
check(canonicalCodeEntropy>4 && canonicalValue<0,
  "real native multiplicity price, no blanket positive path entropy claim");

console.log("PASS ORIGINAL 33 / 718 / 8440 / Q8 exact integer counts");
console.log("PASS genuine finite future-history soft-Bellman / KL / positive scores");
console.log("PASS horizon-change and wrong degree-walk hostile controls");
console.log("PASS original native Perron continuation and clock-pressure threshold");
console.log("PASS three-tier conditional Golden test and full-price break-even ratios");
console.log(JSON.stringify({
  p, rho, absolute_per_tick_pressure:clockPressure,
  transition_A_to_B:{N1:AB(1),N2:AB(2),N32:AB(32),bulk:ABbulk},
  finite_depth4:{value:V,first_source:source1,second_source:source2,KL},
  bright_probabilities:{passive:qPassive,anchored:qAnchor,targeted:qTarget},
  break_even_full_paid_prices:{
    anchored_over_passive:ratioAnchorPassive,
    targeted_over_anchored:ratioTargetAnchor,
    targeted_over_passive:qTarget/qPassive},
  trials_for_miss_1e_minus_6:{
    passive:maxTrials(qPassive,1e-6),
    anchored:maxTrials(qAnchor,1e-6),
    targeted:maxTrials(qTarget,1e-6)}
}, null, 2));

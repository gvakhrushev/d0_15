# WRK-A4D-LABELLED-ENDPOINT-CLASSICAL-DESCENT

## Class

WORKER

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Objective

Lean-own the **path-provenance seam** independently of the relative A/e
relation.

The repo already owns slot-faithful endpoint-independence iff trivial labelled
holonomy on \`List ChainStep\`.

This worker packages that result as a precise endpoint-locality passport and
adds hostile witnesses showing that endpoint descent is logically independent
of local relation graphification.

## Read first

- \`03_FORMALIZATION/D0/Geometry/A4DLabelledPathHolonomyDescent.lean\`;
- \`03_FORMALIZATION/D0/Geometry/ArchivePathWordAlgebra.lean\`;
- \`03_FORMALIZATION/D0/Geometry/A4DReferenceJunctionCompressionBoundary.lean\`;
- PR #123 memo for the relation/vertical-defect vocabulary only.

## Preferred module

\`03_FORMALIZATION/D0/Geometry/A4DLabelledEndpointLocalityPassport.lean\`

## Mandatory definitions

For a generic positive labelled link family, define a literal predicate
\`EndpointLocal\` meaning that path evaluation depends only on:

- the start site;
- the final endpoint;

while retaining the slot-faithful \`List ChainStep\` carrier before quotient.

Do not use the older Prop-edge \`ChainPath E\` carrier for the main theorem.

## Mandatory theorem package

### 1. Endpoint locality iff trivial labelled holonomy

Repackage/reuse the owned theorem as an explicit passport:

\[
\text{EndpointLocal}
\iff
\text{every labelled loop has identity transport}.
\]

No weakening to plaquette-flatness.

### 2. Induced endpoint transport

Under EndpointLocal, define the induced endpoint map and prove:

- identity at equal endpoints;
- composition through an intermediate endpoint;
- inverse under endpoint reversal.

### 3. Exact L=2 slot firewall

At \(L=2\),

\[
\mathrm{fwd}\ r\ne\mathrm{bwd}\ r
\]

as labels even though endpoints coincide.

Endpoint locality must imply the exact two-positive-link period already owned.

### 4. Noncontractible-cycle firewall

Give/reuse an exact finite witness with local plaquette-flatness but nontrivial
cycle holonomy.

Prove local flatness does not imply EndpointLocal.

### 5. Independence from local relation graphification

Package the logic abstractly:

a local fibre/relation condition at each edge does not by itself imply trivial
labelled loop holonomy.

Provide one exact generic link-family witness where local edge maps are
perfectly single-valued/invertible but one labelled loop has nonidentity
transport.

### 6. Converse independence

Provide one endpoint-local identity-transport witness while allowing an
independent non-graph local A/e relation datum.

This theorem may be formulated as a product of independent structures rather
than coupling unrelated modules.

The purpose is to show that path descent does not imply graphification.

### 7. Endpoint quotient boundary

State precisely what information is forgotten by passing from the labelled
path parent to endpoint transport.

Do not claim the quotient is physically mandatory.

## Firewalls

Do not:

- identify endpoint locality with \(M=0\);
- identify endpoint locality with \(R=0\);
- claim plaquette flatness is enough;
- erase L=2 label distinction before proving the period;
- start finite \(F\);
- touch continuum/GR/stress/time/golden work.

## Exit condition

Lean owns an explicit endpoint-locality passport equivalent to trivial labelled
holonomy, with L=2 and noncontractible-cycle firewalls and exact witnesses that
path descent is logically independent from local A/e relation graphification.

## GitHub-first flow

Fresh current main → lifecycle start → Draft PR → narrow build → incremental
\`D0.All\` → support registration → self-retire → \`Lifecycle: REVIEW\` →
Ready → do not self-merge.

No \`sorry\`, no new axioms, no \`lake clean\`.

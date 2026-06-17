# D0 Baryon 40/56 Decomposition

## Definitions

- V_shell ≅ ℂ³ = span{|9⟩, |11⟩, |13⟩} (Core-13 three-orbit frozen shell geometry from PDG passport shadow).
- Flavour carrier: V_B^flavour = V_shell^⊗³ , dim=27.
- Symmetric flavour sector: Sym³(ℂ³), rank=10 (certified by S3 symmetrizer).
- Spin dyad: ℂ² , symmetric sector Sym³(ℂ²), rank=4.

## Theorem

The internal baryon spin-flavour carriers before any PDG passport are:

Π_B^{40} = Π_{S3}^{flavour} ⊗ Π_{S3}^{spin} , rank=40

Π_B^{56} = (1/6) ∑_{σ∈S3} P_σ^{flavour} ⊗ P_σ^{spin} , rank=56

With inclusion:

Π_B^{56} Π_B^{40} = Π_B^{40} = Π_B^{40} Π_B^{56}

Thus 56 = 40 + 16 (mixed spin-flavour complement).

Anonymous poles:

U_eff^{B,k} = Π_B^k P U P Π_B^k , k∈{40,56}

det(I − ζ U_eff^{B,k}) = 0

## Proof (constructive)

The projectors are built from S3 symmetrizers on the respective carriers (see vp_cvft_baryon_40_56_decomposition.py for explicit numpy construction using permutation representations and rank via eigvalsh).

- rank_flavour_sym = 10
- rank_spin_sym = 4
- rank_40 = 40 (kron product)
- rank_56 = 56 (diagonal average, equals binom(6+3-1,3))
- Inclusion and 16 complement verified numerically and algebraically.

## Negative Controls (expected rejected shortcuts)

- FAIL_RANK40_AS_FULL_BARYON_CARRIER
- FAIL_PDG_SORTING_BEFORE_SPIN_FLAVOUR_TRANSFER
- FAIL_COMPLEX_POLES_FROM_BARE_F
- FAIL_RANDOM_NONHERMITIAN_RESONANCE_OPERATOR

## Cert Tokens

From 05_CERTS/vp_cvft_baryon_40_56_decomposition.py :

PASS_S3_FLAVOUR_AND_SPIN_REPRESENTATIONS

PASS_FLAVOUR_S3_SYMMETRIC_RANK_10

PASS_SPIN_S3_SYMMETRIC_RANK_4

PASS_BARYON_SPIN_FLAVOUR_RANK_40

PASS_BARYON_DIAGONAL_SPIN_FLAVOUR_RANK_56

PASS_RANK40_SUBSECTOR_OF_RANK56

PASS_BARYON_MIXED_SPIN_FLAVOUR_RANK_16

PASS_BARYON_SPIN_FLAVOUR_NO_PDG_ASSIGNMENT

(and the four FAIL_ negative controls)

## Book Patch Text (for Book 04)

The existing PDG/Core-13 passport does not merely show that masses have φ-lattice representatives. Its structural content is the frozen three-orbit shell geometry. D0 now identifies this three-orbit geometry with the finite shell carrier V_shell = span{|9⟩,|11⟩,|13⟩} ≅ ℂ³.

The baryon flavour carrier is the three-body lift V_B^flavour = V_shell^⊗³ , dim=27.

The exchange-symmetric flavour sector has rank dim Sym³(ℂ³)=10.

With the binary spin dyad (D₂≅ℂ²), D0 obtains two internal spin-flavour carriers before any PDG passport:

Π_B^{40} = Π_{S3}^{flavour} ⊗ Π_{S3}^{spin} , rank=40

and

Π_B^{56} = (1/6) ∑_{σ∈S3} P_σ^{flavour} ⊗ P_σ^{spin} , rank=56

The rank-40 carrier is a canonical subcarrier of the rank-56 diagonal spin-flavour carrier:

Π_B^{56} Π_B^{40} = Π_B^{40} , Π_B^{40} Π_B^{56} = Π_B^{40}

Thus the internal decomposition is 56=40+16.

The rank-16 complement is the mixed spin-flavour diagonal-symmetric sector. Anonymous pole sets are then defined by U_eff^{B,k} = Π_B^k P U P Π_B^k , k∈{40,56}, det(I−ζ U_eff^{B,k})=0 .

PDG names, GeV conversion, physical mass assignment and decay widths remain passport-layer operations. The internal spin-flavour carrier is finite and closed before those external labels are applied.

(The legacy text treating the scalar projector or other boundaries as open no-gos is superseded by the certified carriers above.)

import D0.Bridge.InternalConeSpeed
import D0.Bridge.TickGaugeLorentz
import D0.Born
import D0.Core.BornFiniteEffects
import D0.Core.BornQuadraticResponse
import D0.Core.BornQuadraticOrigin
import D0.Topology.BoundaryBoundary
import D0.Topology.TripartiteComplex
import D0.Geometry.ArchiveVariation
import D0.Geometry.ArchiveVariationDual
import D0.Geometry.ArchiveStressRepresentative
import D0.Geometry.ArchivePoissonEquation
import D0.Interface.ScalarPoissonReduction
import D0.Matter.ArchivePartialTrace
import D0.Matter.GeneratedMatterSource
import D0.Matter.LocalTraceSource
import D0.Interface.MatterLocalization
import D0.Matter.VectorFieldEquation
import D0.Matter.VectorOperatorOrigin
import D0.Matter.CKMBasisMismatch
import D0.Matter.CKMBasisOrigin
import D0.Matter.CKMNontrivialFlavourAlgebra
import D0.Matter.CKMPhasonHolonomy
import D0.Matter.GenerationSelectorOrigin
import D0.Matter.GenerationOverlapResponseOrigin
import D0.Matter.FiniteSelector
import D0.Matter.Book04Selectors
import D0.Matter.Book04ConcreteSelectors
import D0.Matter.Book04FullSupportSelectors
import D0.Matter.Book04CenteredSupportSelectors
import D0.Matter.Book04CombinatorialSelectorOrigins
import D0.Matter.Book04CoefficientOrigin
import D0.Matter.BaryonS3Symmetrizer
import D0.Matter.BaryonMultipletBoundary
import D0.Matter.Book04OperatorBoundary
import D0.Matter.PhasonStrainGenerations
import D0.Matter.MesonDefectTransferAlgebra
import D0.Matter.MesonDefectTransferOrigin
import D0.Matter.MesonPhasonDomainWalls
import D0.Matter.NuclearShellContactSRC
import D0.Matter.HiggsScalarProjectorConstructive
import D0.Geometry.EdgeMetricEquation
import D0.Geometry.EdgeStiffnessOrigin
import D0.Algebra.ArchiveCommutatorOperators
import D0.Algebra.HurwitzLocalBoundary
import D0.Algebra.D0InternalDimensionSelector
import D0.Algebra.GaugeKineticPositivity
import D0.Bridge.Assumptions.YangMillsKilling
import D0.Bridge.OperatorOriginIndex
import D0.Gauge.FlatTensorNoGo
import D0.Gauge.NonAbelianDiscreteCurvature
import D0.Gauge.BianchiResidual
import D0.Gauge.YangMillsKillingPositivity
import D0.Gauge.MatrixRepGaugeTransform
import D0.Gauge.WilsonLinkGaugeCovariance
import D0.Gauge.GradedBianchiIdentity
import D0.Gauge.SMGaugeDecomposition
import D0.Cosmology.ArchiveHomogeneousState
import D0.Cosmology.ZeroMeanModes
import D0.Cosmology.TransientAcceleration
import D0.Cosmology.InstabilitySaturation
import D0.Cosmology.EntropyArchiveFlow
import D0.Cosmology.PhasonFlipEntropy
import D0.Cosmology.LinearizedEntropyFlow
import D0.Cosmology.ArchiveVolumeBounds
import D0.Cosmology.ConcreteEntropyArchiveFlow
import D0.Cosmology.EntropyJacobianSign
import D0.Cosmology.FloorMassProjection
import D0.Cosmology.CoreShapePassportBoundary
import D0.Cosmology.SurveyReproducibilitySplit
import D0.Probability.EntropyFlowJacobian
import D0.Geometry.FiniteSpin2
import D0.Geometry.FiniteSpin2WaveOperator
import D0.Geometry.TorusCore13GeometryOrigin
import D0.Geometry.HurwitzRigidPhaseGenerator
import D0.Geometry.PhaseReturnBranchCount
import D0.Geometry.PhaseUnfoldingQuasicrystal
import D0.Geometry.HeatTraceA2Decomposition
import D0.Geometry.HigherCurvatureSuppression
import D0.Geometry.SpectralActionLadder
import D0.Gravity.EntropicArchiveInterface
import D0.Gravity.MacroEinsteinInterface
import D0.Core.FixedDetectorTimeLadder
import D0.Dynamics.ToralAutomorphism
import D0.Dynamics.GaloisConjugateBalance
import D0.Dynamics.DarkSectorCoarseGrain
import D0.Dynamics.TraceHeatLucasCore
import D0.Dynamics.TraceHeatCapacityGravity
import D0.Dynamics.MasterEvolutionTheorem
import D0.Condensed.CondensedPhiVacuum
import D0.Physics.QuasiGenerationsInflation
import D0.Physics.ArchivePhasonDarkMatter
import D0.Physics.WindowOffsetChirality
import D0.Physics.PhasonFlipInertia
import D0.Physics.WindowFractionalCharge
import D0.Physics.QuasicrystalPhenomenology
import D0.Physics.GaloisLorentzSignature
import D0.Matter.NeutrinoPhasonWaves
import D0.Passport.IceCubePhasonDecoherence
import D0.NoGo.StressTestSuite
import D0.Traceability.StatusTaxonomy
import D0.Bridge.SICalibrationBoundary
import D0.Bridge.SICalibrationClosure
import D0.Bridge.InterpretationSpine
import D0.Topology.GradedIncidenceComplex
import D0.TheoremLedger.ReleaseStatus
import D0.Matter.ChargedLeptonMassTransfer
import D0.Matter.CKMExactTransfer
import D0.Geometry.FiniteSpin2Dynamics
import D0.Matter.ChargedLeptonTransferCertificate
import D0.Matter.CKMExactMatrixCertificate
import D0.Geometry.FiniteSpin2DOF

namespace D0.Bridge

/-- Book-04 operator-boundary index entries: the meson-`400`, Higgs scalar-projector, and bundled
no-go closures (the baryon entry is the structure field `book04BaryonMultipletBoundary`). -/
def book04Meson400Boundary : Prop :=
  ¬ D0.Matter.CanPromoteMesonMasses D0.Matter.lowerHodge400SeedOnly

def book04HiggsScalarProjectorBoundary : Prop :=
  ¬ D0.Matter.CanPromoteHiggsYukawaCore D0.Matter.missingScalarProjectorBridge

def book04OperatorBoundariesClosed : D0.Matter.Book04OperatorBoundaryClosed :=
  D0.Matter.book04_operator_boundaries_closed

inductive FinalBridgeStatus where
  | coreClosed
  | certClosed
  | noGo
  | bridgeCalibration
  | empiricalPassport
  | externalDataRequired
  deriving DecidableEq, Repr

def finalBridgeStatusLabel : FinalBridgeStatus → String
  | FinalBridgeStatus.coreClosed => "CORE-CLOSED"
  | FinalBridgeStatus.certClosed => "CERT-CLOSED"
  | FinalBridgeStatus.noGo => "NO-GO"
  | FinalBridgeStatus.bridgeCalibration => "BRIDGE-CALIBRATION"
  | FinalBridgeStatus.empiricalPassport => "EMPIRICAL-PASSPORT"
  | FinalBridgeStatus.externalDataRequired => "EXTERNAL-DATA-REQUIRED"

def finalBridgeStatusTable : List (String × FinalBridgeStatus) :=
  [ ("finite Lean foundations", FinalBridgeStatus.coreClosed)
  , ("Python-backed finite certificates", FinalBridgeStatus.certClosed)
  , ("explicit no-go / boundary layers", FinalBridgeStatus.noGo)
  , ("local Hurwitz/Lagrange dimensions 1/2/4/8", FinalBridgeStatus.coreClosed)
  , ("global Hurwitz/Lagrange classification external background", FinalBridgeStatus.bridgeCalibration)
  , ("matrix-representation Yang-Mills layer", FinalBridgeStatus.coreClosed)
  , ("Wilson-link finite gauge covariance", FinalBridgeStatus.coreClosed)
  , ("graded incidence Bianchi identity", FinalBridgeStatus.coreClosed)
  , ("smooth/continuum calibration bridges", FinalBridgeStatus.bridgeCalibration)
  , ("SI spectral bridge calibration coefficients", FinalBridgeStatus.bridgeCalibration)
  , ("external-data passports", FinalBridgeStatus.empiricalPassport)
  , ("missing packaged external data", FinalBridgeStatus.externalDataRequired)
  , ("Book 04 meson/baryon/Higgs direct-promotion boundaries", FinalBridgeStatus.noGo)
  ]

/--
A non-vacuous final foundation index.

This structure deliberately contains theorem-shaped fields rather than status labels.
The release is considered internally indexed only when already-proved finite-core,
Born-readout, gauge, spectral-gravity, and bridge-boundary statements can be
assembled into one Lean object.  This replaces the former vacuous `True` index.
-/
structure FinalFoundationIndex where
  bornWeightsNormalized :
    ∀ (r : D0.TwoChannelPositiveResponse),
      D0.responseBornWeight0 r + D0.responseBornWeight1 r = 1
  bornReadoutUnique :
    ∀ (r : D0.TwoChannelPositiveResponse) (q : D0.TwoChannelReadout r),
      q.p0 = D0.responseBornWeight0 r ∧ q.p1 = D0.responseBornWeight1 r
  finiteBornReadoutUnique :
    ∀ {ι : Type} [Fintype ι]
      (r : D0.FinitePositiveResponse ι) (q : D0.FiniteBornReadout r),
        ∀ i, q.probability i = D0.finiteResponseBornWeight r i
  finiteBornNoAlternative :
    ∀ {ι : Type} [Fintype ι]
      (r : D0.FinitePositiveResponse ι) (q : D0.FiniteBornReadout r),
        (∃ i, q.probability i ≠ D0.finiteResponseBornWeight r i) → False

  finiteEffectBornReadoutUnique :
    ∀ {ι σ : Type} [Fintype ι] [Fintype σ]
      (F : D0.FiniteEffectFrame ι σ) (q : D0.FiniteEffectBornReadout F),
        ∀ i, q.probability i = D0.finiteEffectBornWeight F i
  finiteEffectBornNoHiddenResponse :
    ∀ {ι σ : Type} [Fintype ι] [Fintype σ]
      (F : D0.FiniteEffectFrame ι σ) (q : D0.FiniteEffectBornReadout F),
        (∃ i, q.probability i ≠ D0.finiteEffectBornWeight F i) → False
  finiteCoarseBornReadoutUnique :
    ∀ {ι σ κ : Type} [Fintype ι] [Fintype σ] [Fintype κ] [DecidableEq κ]
      (F : D0.FiniteEffectFrame ι σ) (C : D0.FiniteCoarseGraining F κ)
      (q : D0.FiniteCoarseBornReadout F C),
        ∀ k, q.probability k = D0.finiteCoarseBornWeight F C k
  finitePowerReadoutNoAlternative :
    ∀ {ι : Type} [Fintype ι]
      (r : D0.FinitePositiveResponse ι) (q : D0.FinitePowerReadoutCandidate r),
        (∃ i, q.probability i ≠ D0.finiteResponseBornWeight r i) → False
  finiteTensorBornReadoutUnique :
    ∀ {ι κ : Type} [Fintype ι] [Fintype κ]
      (T : D0.FiniteTensorResponse ι κ) (q : D0.FiniteTensorBornReadout T),
        ∀ x, q.probability x = D0.finiteResponseBornWeight T.response_product x
  phaseBlindQuadraticResponseIsNormSqScaled :
    ∀ (Q : D0.PhaseQuadraticResponse), D0.QuarterTurnInvariant Q →
      ∀ z, D0.phaseQuadraticEval Q z = Q.xx * D0.amplitudeNormSq z
  unitPhaseBlindQuadraticResponseIsNormSq :
    ∀ (Q : D0.UnitPhaseQuadraticResponse),
      ∀ z, D0.phaseQuadraticEval Q.response z = D0.amplitudeNormSq z
  finiteAmplitudeBornReadoutUnique :
    ∀ {ι σ : Type} [Fintype ι] [Fintype σ]
      (A : D0.FiniteAmplitudeEffectFrame ι σ) (q : D0.FiniteAmplitudeBornReadout A),
        ∀ i, q.probability i = D0.finiteAmplitudeBornWeight A i
  finiteAmplitudeBornNoAlternative :
    ∀ {ι σ : Type} [Fintype ι] [Fintype σ]
      (A : D0.FiniteAmplitudeEffectFrame ι σ) (q : D0.FiniteAmplitudeBornReadout A),
        (∃ i, q.probability i ≠ D0.finiteAmplitudeBornWeight A i) → False
  tripartiteNoThreeSimplices :
    ∀ a b c d : D0.Part, ¬ D0.FourCliqueParts a b c d
  ckmBasisMismatchUnique :
    ∀ {n : ℕ} {Op : Type}
      (up down : D0.Matter.FiniteOperatorBasis n Op)
      (C : D0.Matter.BasisMismatchCandidate up down),
        C.matrix = D0.Matter.basisMismatchMatrix up down
  ckmNoAlternativeAtFixedBases :
    ∀ {n : ℕ} {Op : Type}
      (up down : D0.Matter.FiniteOperatorBasis n Op)
      (M : Matrix (Fin n) (Fin n) ℚ),
        M ≠ D0.Matter.basisMismatchMatrix up down →
          ¬ ∃ C : D0.Matter.BasisMismatchCandidate up down, C.matrix = M
  ckmOriginCandidateMatrixUnique :
    ∀ {n : ℕ} {Op : Type}
      (O : D0.Matter.CKMBasisOrigin n Op)
      (C : D0.Matter.CKMOriginCandidate O),
        C.matrix = D0.Matter.ckmOriginMatrix O
  ckmNoFreeMatrixAtFixedBasisOrigin :
    ∀ {n : ℕ} {Op : Type}
      (O : D0.Matter.CKMBasisOrigin n Op)
      (M : Matrix (Fin n) (Fin n) ℚ),
        M ≠ D0.Matter.ckmOriginMatrix O →
          ¬ ∃ C : D0.Matter.CKMOriginCandidate O, C.matrix = M
  concreteCKMBasisOrigin : D0.Matter.CKMBasisOrigin 3 D0.Matter.CKMFlavorOperator
  finiteSelectorHasFiniteSupport :
    ∀ {α : Type} (S : D0.Matter.FiniteSelector α), Fintype α
  finiteSelectorUnique :
    ∀ {α : Type} (S : D0.Matter.FiniteSelector α) {a b : α},
      D0.Matter.StrictSelected S a → D0.Matter.StrictSelected S b → a = b
  finiteSelectorNoFreeAlternative :
    ∀ {α : Type} (C : D0.Matter.StrictSelectorCertificate α)
      (b : α), b ≠ C.selected → ¬ D0.Matter.StrictSelected C.selector b
  differentSelectionRequiresScoreChange :
    ∀ {α : Type} (C D : D0.Matter.StrictSelectorCertificate α),
      C.selected ≠ D.selected → ¬ ∀ x, C.selector.score x = D.selector.score x
  book04SelectorNoFreeAlternative :
    ∀ (C : D0.Matter.Book04SelectorClaim)
      (b : C.Candidate), b ≠ C.selected → ¬ D0.Matter.StrictSelected C.selector b
  book04DifferentSelectedRequiresScoreChange :
    ∀ (C : D0.Matter.Book04SelectorClaim)
      (D : D0.Matter.StrictSelectorCertificate C.Candidate),
        C.selected ≠ D.selected → ¬ ∀ x, C.selector.score x = D.selector.score x
  concreteChargedLeptonElectronTerminalClaim : D0.Matter.Book04SelectorClaim
  concreteElectroweakDepth35Claim : D0.Matter.Book04SelectorClaim
  concreteProtonReadout306Claim : D0.Matter.Book04SelectorClaim
  concreteNeutronArchiveSiblingClaim : D0.Matter.Book04SelectorClaim
  concreteBetaUnlockDepth19Claim : D0.Matter.Book04SelectorClaim
  fullSupportElectroweakDepth35Claim : D0.Matter.Book04SelectorClaim
  fullSupportProtonReadout306Claim : D0.Matter.Book04SelectorClaim
  fullSupportBetaUnlockDepth19Claim : D0.Matter.Book04SelectorClaim
  electroweakDepth35FullSupportNoAlternative :
    ∀ b : D0.Matter.ElectroweakDepthFullSupport,
      b ≠ D0.Matter.electroweakDepth35FullTarget →
        ¬ D0.Matter.StrictSelected D0.Matter.electroweakDepthFullSelector b
  protonReadout306FullSupportNoAlternative :
    ∀ b : D0.Matter.ProtonReadoutFullSupport,
      b ≠ D0.Matter.protonReadout306FullTarget →
        ¬ D0.Matter.StrictSelected D0.Matter.protonReadoutFullSelector b
  betaUnlockDepth19FullSupportNoAlternative :
    ∀ b : D0.Matter.BetaUnlockDepthFullSupport,
      b ≠ D0.Matter.betaUnlockDepth19FullTarget →
        ¬ D0.Matter.StrictSelected D0.Matter.betaUnlockDepthFullSelector b
  book04FullSupportSelectorsClosed : D0.Matter.Book04FullSupportSelectorsClosed
  centeredElectroweakDepth35Claim : D0.Matter.Book04SelectorClaim
  centeredProtonReadout306Claim : D0.Matter.Book04SelectorClaim
  centeredBetaUnlockDepth19Claim : D0.Matter.Book04SelectorClaim
  electroweakDepth35CenteredNoAlternative :
    ∀ b : Fin 71,
      b ≠ D0.Matter.centeredSupportMidpoint 35 →
        ¬ D0.Matter.StrictSelected (D0.Matter.centeredSupportSelector (R := 35)) b
  protonReadout306CenteredNoAlternative :
    ∀ b : Fin 613,
      b ≠ D0.Matter.centeredSupportMidpoint 306 →
        ¬ D0.Matter.StrictSelected (D0.Matter.centeredSupportSelector (R := 306)) b
  betaUnlockDepth19CenteredNoAlternative :
    ∀ b : Fin 39,
      b ≠ D0.Matter.centeredSupportMidpoint 19 →
        ¬ D0.Matter.StrictSelected (D0.Matter.centeredSupportSelector (R := 19)) b
  book04CenteredSupportSelectorsClosed : D0.Matter.Book04CenteredSupportSelectorsClosed
  book04CombinatorialSelectorOriginsClosed : D0.Matter.Book04CombinatorialSelectorOriginsClosed
  electroweakSelectorRadiusFromOmega8 : D0.Matter.electroweakSelectorRadius = 35
  protonReadoutSelectorRadiusFromHighGain : D0.Matter.protonReadoutSelectorRadius = 306
  betaUnlockSelectorRadiusFromWeakUnlock : D0.Matter.betaUnlockSelectorRadius = 19
  concreteChargedLeptonCoefficientOrigin : D0.Matter.ChargedLeptonCoefficientOrigin
  chargedLeptonCoefficientOriginRowUnique :
    ∀ (O : D0.Matter.ChargedLeptonCoefficientOrigin),
      O.row = D0.Matter.ChargedLeptonCoefficientRow.operatorOrigin
  chargedLeptonCoefficientTableForced :
    ∀ (O : D0.Matter.ChargedLeptonCoefficientOrigin),
      O.ratio = D0.Matter.chargedLeptonRatioCoefficient
          D0.Matter.ChargedLeptonCoefficientRow.operatorOrigin ∧
        O.exponent = D0.Matter.chargedLeptonDepthExponent
          D0.Matter.ChargedLeptonCoefficientRow.operatorOrigin ∧
          O.bridge = D0.Matter.chargedLeptonBridgeFactor
            D0.Matter.ChargedLeptonCoefficientRow.operatorOrigin
  chargedLeptonCoefficientNoFreeRowAlternative :
    ∀ (row : D0.Matter.ChargedLeptonCoefficientRow),
      row ≠ D0.Matter.ChargedLeptonCoefficientRow.operatorOrigin →
        ¬ D0.Matter.StrictSelected D0.Matter.chargedLeptonCoefficientRowSelector row
  chargedLeptonCoefficientsNoFreeRetuning :
    ∀ (O : D0.Matter.ChargedLeptonCoefficientOrigin),
      ¬ (O.ratio ≠ D0.Matter.chargedLeptonRatioCoefficient
            D0.Matter.ChargedLeptonCoefficientRow.operatorOrigin ∨
        O.exponent ≠ D0.Matter.chargedLeptonDepthExponent
            D0.Matter.ChargedLeptonCoefficientRow.operatorOrigin ∨
          O.bridge ≠ D0.Matter.chargedLeptonBridgeFactor
            D0.Matter.ChargedLeptonCoefficientRow.operatorOrigin)
  book04BaryonMultipletBoundary :
    ¬ D0.Matter.CanPromoteBaryonMultiplet D0.Matter.nucleonLineOnlyBaryonOperator
  smGaugeFactorsClosed :
    D0.Gauge.frozenSMGaugeDecomposition.factors = D0.Gauge.frozenSMGaugeFactorLedger
  smGenerationLedgerClosed :
    D0.Gauge.frozenSMGaugeDecomposition.representationLedger = D0.generation
  smGenerationAnomalyFree :
    D0.gravU1Sum = 0 ∧
      D0.cubicU1Sum = 0 ∧
        D0.su2su2u1Sum = 0 ∧
          D0.su3su3u1Sum = 0
  smNoAlternativeGaugeFactors :
    ∀ (F : List D0.Gauge.SMGaugeFactor),
      F ≠ D0.Gauge.frozenSMGaugeFactorLedger →
        ¬ ∃ C : D0.Gauge.FrozenSMGaugeDecomposition, C.factors = F
  smNoAlternativeGenerationLedger :
    ∀ (R : List D0.WeylField),
      R ≠ D0.generation →
        ¬ ∃ C : D0.Gauge.FrozenSMGaugeDecomposition, C.representationLedger = R
  smEftBridgeRequiresFrozenDecomposition :
    ∀ (B : D0.Gauge.SMEFTBridgeAfterFreeze),
      B.finiteLedger.factors = D0.Gauge.frozenSMGaugeFactorLedger ∧
        B.finiteLedger.representationLedger = D0.generation
  cosmologyInternalShapeIndependent :
    ∀ (O : D0.Cosmology.InternalArchiveCosmologyObject)
      (ep₁ ep₂ : D0.Cosmology.EmpiricalParams),
        D0.Cosmology.internalArchiveShapeEvaluated O ep₁ =
          D0.Cosmology.internalArchiveShapeEvaluated O ep₂
  surveyPassportPreservesInternalShape :
    ∀ (P : D0.Cosmology.SurveyLikelihoodPassport),
      D0.Cosmology.surveyPassportInternalShape P = P.internalObject.entropyTransferShape
  surveyComparisonRequiresNonemptyManifest :
    ¬ D0.Cosmology.SurveyComparisonReproducible []
  surveyLikelihoodCannotPromoteToCoreCosmology :
    ∀ (P : D0.Cosmology.SurveyLikelihoodPassport),
      ¬ D0.Cosmology.CanPromoteSurveyPassportToCore P
  frozenArchiveCosmologyCoreShapeClosed :
    ∀ (F : D0.Cosmology.FrozenArchiveCosmology)
      (ep₁ ep₂ : D0.Cosmology.EmpiricalParams),
        D0.Cosmology.internalArchiveShapeEvaluated F.object ep₁ =
          D0.Cosmology.internalArchiveShapeEvaluated F.object ep₂
  gaugeKineticNonnegative :
    ∀ {n : Type} [Fintype n] [DecidableEq n]
      (K : Matrix n n ℝ) (hK : K.transpose = -K) (c : ℝ) (hc : c > 0),
        D0.Algebra.gaugeKineticAction K c ≥ 0
  spectralA2IsEHProxy :
    ∀ {N : Type} [Fintype N] [DecidableEq N]
      (L : Matrix N N ℝ) (ρ : N → ℝ)
      (h_pos : ∀ i, ρ i > 0) (h_symm : ∀ i j, L i j = L j i),
        D0.Geometry.SpectralActionLadder.spectralTracePower L ρ 2 =
          D0.Geometry.HeatTraceA2Decomposition.diagonalSquareTerm L ρ
            + 2 * D0.Geometry.HeatTraceA2Decomposition.discreteEHActionProxy L ρ
  finiteSpin2TTCarrierClosed :
    ∀ {ι : Type} [Fintype ι] (m : D0.Geometry.FiniteTTMode ι),
      (∀ i j, m.h i j = m.h j i) ∧
        D0.Geometry.finiteMetricTrace m.toFiniteMetricMode = 0 ∧ m.transverse
  finiteWeakFieldQuotientYieldsTT :
    ∀ {ι : Type} [Fintype ι] (q : D0.Geometry.FiniteWeakFieldQuotient ι),
      (∀ i j, q.ttRepresentative.h i j = q.ttRepresentative.h j i) ∧
        D0.Geometry.finiteMetricTrace q.ttRepresentative.toFiniteMetricMode = 0 ∧
          q.ttRepresentative.transverse
  finiteGaugeTraceQuotientClosed :
    ∀ {ι : Type} [Fintype ι] (q : D0.Geometry.FiniteWeakFieldQuotient ι),
      q.quotientReconstruction ∧
        q.conservedStressKillsLongitudinal ∧ q.conservedStressKillsTrace
  finiteConservedStressSpin2CouplingClosed :
    ∀ {ι : Type} [Fintype ι] (q : D0.Geometry.FiniteWeakFieldQuotient ι),
      q.conservedStressKillsLongitudinal ∧ q.conservedStressKillsTrace ∧
        ((∀ i j, q.ttRepresentative.h i j = q.ttRepresentative.h j i) ∧
          D0.Geometry.finiteMetricTrace q.ttRepresentative.toFiniteMetricMode = 0 ∧
            q.ttRepresentative.transverse)
  finiteTraceModeRemovedFromSpin2Carrier :
    ∀ {ι : Type} [Fintype ι] (q : D0.Geometry.FiniteWeakFieldQuotient ι),
      D0.Geometry.finiteMetricTrace q.ttRepresentative.toFiniteMetricMode = 0
  internalConeSpeedIsOne :
    ∀ (g : D0.Bridge.InternalKinematicGauge),
      D0.Bridge.internalConeSpeed g = 1
  finiteCausalTickSectionForcesSameTick :
    ∀ (s : D0.Bridge.FiniteCausalTickSection), s.lineTick = s.timeTick
  finiteCausalTickSectionConeSpeedIsOne :
    ∀ (s : D0.Bridge.FiniteCausalTickSection),
      D0.Bridge.internalConeSpeed (D0.Bridge.finiteCausalTickSectionGauge s) = 1
  commonTickRescalingPreservesConeSpeed :
    ∀ (s : D0.Bridge.FiniteCausalTickSection) (lambda : ℚ) (hlambda : 0 < lambda),
      D0.Bridge.internalConeSpeed
          (D0.Bridge.finiteCausalTickSectionGauge
            (D0.Bridge.rescaleFiniteCausalTickSection s lambda hlambda)) =
        D0.Bridge.internalConeSpeed (D0.Bridge.finiteCausalTickSectionGauge s)
  asymmetricTicksNotInternalGauge :
    ∀ (line time : ℚ), line ≠ time →
      ¬ ∃ s : D0.Bridge.FiniteCausalTickSection,
        s.lineTick = line ∧ s.timeTick = time
  finiteLorentzTickGaugeConeSpeedClosed :
    ∀ (C : D0.Bridge.FiniteLorentzTickGaugeClosure),
      D0.Bridge.internalConeSpeed
        (D0.Bridge.finiteCausalTickSectionGauge C.tickSection) = 1
  finiteLorentzTickGaugeSignatureClosed :
    ∀ (C : D0.Bridge.FiniteLorentzTickGaugeClosure),
      D0.roleSignature = (1, 3)
  finiteLorentzTickGaugeNoEuclideanExport :
    ∀ (C : D0.Bridge.FiniteLorentzTickGaugeClosure),
      D0.roleSignature ≠ (4, 0)
  finiteLorentzTickGaugeNoSplitExport :
    ∀ (C : D0.Bridge.FiniteLorentzTickGaugeClosure),
      D0.roleSignature ≠ (2, 2)
  finiteLorentzTickRescalingPreservesClosure :
    ∀ (C : D0.Bridge.FiniteLorentzTickGaugeClosure) (lambda : ℚ) (hlambda : 0 < lambda),
      D0.Bridge.internalConeSpeed
          (D0.Bridge.finiteCausalTickSectionGauge
            (D0.Bridge.rescaleFiniteCausalTickSection C.tickSection lambda hlambda)) = 1 ∧
        D0.roleSignature = (1, 3)
  siCalibrationCannotPromoteToCore :
    ¬ D0.Traceability.canPromoteTo
      D0.Traceability.D0Status.BRIDGE_CALIBRATION
      D0.Traceability.D0Status.CORE_CLOSED
  empiricalPassportCannotPromoteToCore :
    ¬ D0.Traceability.canPromoteTo
      D0.Traceability.D0Status.EMPIRICAL_PASSPORT
      D0.Traceability.D0Status.CORE_CLOSED

/-- Concrete witness for the non-vacuous final foundation index. -/
def finalFoundationIndexWitness : FinalFoundationIndex where
  bornWeightsNormalized := D0.finite_response_born_weights_sum_one
  bornReadoutUnique := D0.finite_born_readout_unique
  finiteBornReadoutUnique := D0.finite_born_readout_unique_on_finite_outcomes
  finiteBornNoAlternative := D0.finite_born_no_alternative_readout

  finiteEffectBornReadoutUnique := D0.finite_effect_born_readout_unique
  finiteEffectBornNoHiddenResponse := D0.finite_effect_born_no_hidden_response
  finiteCoarseBornReadoutUnique := D0.finite_coarse_born_readout_unique
  finitePowerReadoutNoAlternative := D0.finite_power_readout_no_alternative
  finiteTensorBornReadoutUnique := D0.finite_tensor_born_readout_unique
  phaseBlindQuadraticResponseIsNormSqScaled := D0.phase_blind_quadratic_response_is_norm_sq_scaled
  unitPhaseBlindQuadraticResponseIsNormSq := D0.unit_phase_blind_quadratic_response_is_norm_sq
  finiteAmplitudeBornReadoutUnique := D0.finite_amplitude_born_readout_unique
  finiteAmplitudeBornNoAlternative := D0.finite_amplitude_born_no_alternative
  tripartiteNoThreeSimplices := D0.no_three_simplices_K_9_11_13
  ckmBasisMismatchUnique := D0.Matter.ckm_class_unique_as_operator_basis_mismatch
  ckmNoAlternativeAtFixedBases := D0.Matter.ckm_no_free_matrix_at_fixed_bases
  ckmOriginCandidateMatrixUnique := D0.Matter.ckm_origin_candidate_matrix_unique
  ckmNoFreeMatrixAtFixedBasisOrigin := D0.Matter.ckm_no_free_matrix_at_fixed_basis_origin
  concreteCKMBasisOrigin := D0.Matter.concreteCKMBasisOrigin
  finiteSelectorHasFiniteSupport := D0.Matter.finiteSelectorSupportFintype
  finiteSelectorUnique := D0.Matter.strict_selected_unique
  finiteSelectorNoFreeAlternative := D0.Matter.physical_selector_no_free_alternative
  differentSelectionRequiresScoreChange := D0.Matter.different_selection_requires_score_change
  book04SelectorNoFreeAlternative := D0.Matter.book04_selector_claim_no_free_alternative
  book04DifferentSelectedRequiresScoreChange := D0.Matter.book04_different_selected_requires_score_change
  concreteChargedLeptonElectronTerminalClaim := D0.Matter.chargedLeptonElectronTerminalClaim
  concreteElectroweakDepth35Claim := D0.Matter.electroweakDepth35Claim
  concreteProtonReadout306Claim := D0.Matter.protonReadout306Claim
  concreteNeutronArchiveSiblingClaim := D0.Matter.neutronArchiveSiblingClaim
  concreteBetaUnlockDepth19Claim := D0.Matter.betaUnlockDepth19Claim
  fullSupportElectroweakDepth35Claim := D0.Matter.electroweakDepth35FullSupportClaim
  fullSupportProtonReadout306Claim := D0.Matter.protonReadout306FullSupportClaim
  fullSupportBetaUnlockDepth19Claim := D0.Matter.betaUnlockDepth19FullSupportClaim
  electroweakDepth35FullSupportNoAlternative := D0.Matter.electroweak_depth35_full_support_no_free_alternative
  protonReadout306FullSupportNoAlternative := D0.Matter.proton_readout306_full_support_no_free_alternative
  betaUnlockDepth19FullSupportNoAlternative := D0.Matter.beta_unlock_depth19_full_support_no_free_alternative
  book04FullSupportSelectorsClosed := D0.Matter.book04FullSupportSelectorsClosed
  centeredElectroweakDepth35Claim := D0.Matter.electroweakDepth35CenteredClaim
  centeredProtonReadout306Claim := D0.Matter.protonReadout306CenteredClaim
  centeredBetaUnlockDepth19Claim := D0.Matter.betaUnlockDepth19CenteredClaim
  electroweakDepth35CenteredNoAlternative := D0.Matter.electroweak_depth35_centered_no_free_alternative
  protonReadout306CenteredNoAlternative := D0.Matter.proton_readout306_centered_no_free_alternative
  betaUnlockDepth19CenteredNoAlternative := D0.Matter.beta_unlock_depth19_centered_no_free_alternative
  book04CenteredSupportSelectorsClosed := D0.Matter.book04CenteredSupportSelectorsClosed
  book04CombinatorialSelectorOriginsClosed := D0.Matter.book04CombinatorialSelectorOriginsClosed
  electroweakSelectorRadiusFromOmega8 := D0.Matter.electroweak_selector_radius_from_omega8
  protonReadoutSelectorRadiusFromHighGain := D0.Matter.proton_readout_selector_radius_from_high_gain
  betaUnlockSelectorRadiusFromWeakUnlock := D0.Matter.beta_unlock_selector_radius_from_weak_unlock
  concreteChargedLeptonCoefficientOrigin := D0.Matter.concreteChargedLeptonCoefficientOrigin
  chargedLeptonCoefficientOriginRowUnique := D0.Matter.charged_lepton_coefficient_origin_row_unique
  chargedLeptonCoefficientTableForced := D0.Matter.charged_lepton_coefficient_table_forced
  chargedLeptonCoefficientNoFreeRowAlternative := D0.Matter.charged_lepton_coefficient_no_free_row_alternative
  chargedLeptonCoefficientsNoFreeRetuning := D0.Matter.charged_lepton_coefficients_no_free_retuning
  book04BaryonMultipletBoundary := D0.Matter.nucleon_line_cannot_promote_full_baryon_multiplet
  smGaugeFactorsClosed := D0.Gauge.frozen_sm_gauge_factors_closed
  smGenerationLedgerClosed := D0.Gauge.frozen_sm_generation_ledger_closed
  smGenerationAnomalyFree := D0.Gauge.frozen_sm_generation_anomaly_free
  smNoAlternativeGaugeFactors := D0.Gauge.no_alternative_sm_factors_at_frozen_ledger
  smNoAlternativeGenerationLedger := D0.Gauge.no_alternative_sm_generation_ledger_at_frozen_decomposition
  smEftBridgeRequiresFrozenDecomposition := D0.Gauge.sm_eft_bridge_requires_frozen_decomposition
  cosmologyInternalShapeIndependent := D0.Cosmology.internal_archive_shape_independent_of_empirical_parameters
  surveyPassportPreservesInternalShape := D0.Cosmology.survey_passport_preserves_internal_archive_shape
  surveyComparisonRequiresNonemptyManifest := D0.Cosmology.survey_comparison_requires_nonempty_manifest
  surveyLikelihoodCannotPromoteToCoreCosmology := D0.Cosmology.survey_likelihood_cannot_promote_to_core_cosmology
  frozenArchiveCosmologyCoreShapeClosed := D0.Cosmology.frozen_archive_cosmology_core_shape_closed
  gaugeKineticNonnegative := D0.Algebra.gaugeKineticAction_nonnegative
  spectralA2IsEHProxy := D0.Geometry.SpectralActionLadder.a2_is_eh_proxy
  finiteSpin2TTCarrierClosed := D0.Geometry.finite_spin2_tt_carrier_closed
  finiteWeakFieldQuotientYieldsTT := D0.Geometry.finite_weak_field_quotient_yields_tt_representative
  finiteGaugeTraceQuotientClosed := D0.Geometry.finite_gauge_trace_quotient_closed
  finiteConservedStressSpin2CouplingClosed := D0.Geometry.finite_conserved_stress_spin2_coupling_closed
  finiteTraceModeRemovedFromSpin2Carrier := D0.Geometry.finite_trace_mode_removed_from_spin2_carrier
  internalConeSpeedIsOne := D0.Bridge.internal_cone_speed_eq_one
  finiteCausalTickSectionForcesSameTick := D0.Bridge.finite_causal_tick_section_forces_same_tick
  finiteCausalTickSectionConeSpeedIsOne := D0.Bridge.finite_causal_tick_section_cone_speed_eq_one
  commonTickRescalingPreservesConeSpeed := D0.Bridge.common_tick_rescaling_preserves_internal_cone_speed
  asymmetricTicksNotInternalGauge := D0.Bridge.asymmetric_ticks_not_internal_gauge
  finiteLorentzTickGaugeConeSpeedClosed := D0.Bridge.finite_lorentz_tick_gauge_cone_speed_closed
  finiteLorentzTickGaugeSignatureClosed := D0.Bridge.finite_lorentz_tick_gauge_signature_closed
  finiteLorentzTickGaugeNoEuclideanExport := D0.Bridge.finite_lorentz_tick_gauge_no_euclidean_export
  finiteLorentzTickGaugeNoSplitExport := D0.Bridge.finite_lorentz_tick_gauge_no_split_export
  finiteLorentzTickRescalingPreservesClosure := D0.Bridge.finite_lorentz_tick_rescaling_preserves_closure
  siCalibrationCannotPromoteToCore := D0.Bridge.si_calibration_cannot_promote_to_core_closed
  empiricalPassportCannotPromoteToCore := D0.Traceability.external_likelihood_cannot_promote_to_core_closed

/--
Final foundation index witness.
This object now depends on actual previously proved components and on the new
finite Born uniqueness theorem; it is no longer `trivial` over `True`.
-/
def D0_FINAL_FOUNDATION_INDEX : FinalFoundationIndex :=
  finalFoundationIndexWitness


-- Book 04 concrete selector owners

#check D0.Matter.chargedLeptonElectronTerminalClaim
#check D0.Matter.electroweakDepth35Claim

#check D0.Matter.electroweakDepth35FullSupportClaim
#check D0.Matter.protonReadout306FullSupportClaim
#check D0.Matter.betaUnlockDepth19FullSupportClaim
#check D0.Matter.electroweak_depth35_full_support_no_free_alternative
#check D0.Matter.proton_readout306_full_support_no_free_alternative
#check D0.Matter.beta_unlock_depth19_full_support_no_free_alternative
#check D0.Matter.book04FullSupportSelectorsClosed
#check D0.Matter.electroweakDepth35CenteredClaim
#check D0.Matter.protonReadout306CenteredClaim
#check D0.Matter.betaUnlockDepth19CenteredClaim
#check D0.Matter.electroweak_depth35_centered_no_free_alternative
#check D0.Matter.proton_readout306_centered_no_free_alternative
#check D0.Matter.beta_unlock_depth19_centered_no_free_alternative
#check D0.Matter.book04CenteredSupportSelectorsClosed
#check D0.Matter.book04CombinatorialSelectorOriginsClosed
#check D0.Matter.electroweak_selector_radius_from_omega8
#check D0.Matter.proton_readout_selector_radius_from_high_gain
#check D0.Matter.beta_unlock_selector_radius_from_weak_unlock
#check D0.Matter.protonReadout306Claim
#check D0.Matter.neutronArchiveSiblingClaim
#check D0.Matter.betaUnlockDepth19Claim
#check D0.Matter.charged_lepton_terminal_no_free_alternative
#check D0.Matter.electroweak_depth35_no_free_alternative
#check D0.Matter.proton_readout306_no_free_alternative
#check D0.Matter.neutron_archive_sibling_no_free_alternative
#check D0.Matter.beta_unlock_depth19_no_free_alternative

-- Book 04 charged-lepton coefficient-origin owners

#check D0.Matter.ChargedLeptonCoefficientOrigin
#check D0.Matter.concreteChargedLeptonCoefficientOrigin
#check D0.Matter.charged_lepton_coefficient_origin_row_unique
#check D0.Matter.charged_lepton_coefficient_table_forced
#check D0.Matter.charged_lepton_coefficient_no_free_row_alternative
#check D0.Matter.charged_lepton_coefficients_no_free_retuning
#check D0.Matter.baryon_multiplet_requires_spin_flavour_decuplet_operator
#check D0.Matter.nucleon_line_cannot_promote_full_baryon_multiplet
#check D0.Matter.baryon_triple_carrier_card
#check D0.Matter.sorted_triple_card_eq_ten
#check D0.Matter.antisymmetric_line_annihilated_by_s3_symmetrizer
#check D0.Matter.baryon_s3_symmetrizer_closure
#check D0.Matter.lower_hodge_lift_has_internal_degeneracy
#check D0.Matter.lower_hodge_seed_not_meson_mass_operator
#check D0.Matter.meson_transfer_operator_uses_lifted_flavour_defect
#check D0.Matter.meson_defect_transfer_algebra_closure

-- Born 2.0 finite effect/coarse/tensor owners

#check D0.finite_effect_born_readout_unique
#check D0.finite_effect_born_no_hidden_response
#check D0.finite_coarse_born_readout_unique
#check D0.finite_power_readout_no_alternative
#check D0.finite_tensor_born_readout_unique
#check D0.phase_blind_quadratic_response_is_norm_sq_scaled
#check D0.unit_phase_blind_quadratic_response_is_norm_sq
#check D0.finite_amplitude_born_readout_unique
#check D0.finite_amplitude_born_no_alternative

-- Topological primitives
#check D0.boundary_boundary_zero
#check D0.no_three_simplices_K_9_11_13

-- Variation / stress / Poisson
#check D0.matrix_hs_square_expansion
#check D0.first_variation_trace_square
#check D0.pairing_depends_only_on_symmetric_part
#check D0.skew_part_annihilates_admissible_variations
#check D0.raw_gradient_equivalent_to_canonical_stress
#check D0.canonical_stress_symmetric
#check D0.poisson_requires_neutral_source
#check D0.poisson_solution_unique_mod_constant

-- Matter source / partial trace / localization
#check D0.Matter.sum_localTraceDensity_eq_trace
#check D0.Matter.localTraceDensity_neutral_of_trace_zero
#check D0.Matter.generated_matter_source_neutral_if_anomaly_free
#check D0.Matter.localized_matter_source_neutral_if_anomaly_free
#check D0.Matter.basis_mismatch_matrix_unique
#check D0.Matter.ckm_class_unique_as_operator_basis_mismatch
#check D0.Matter.ckm_no_free_matrix_at_fixed_bases
#check D0.Matter.ckm_origin_candidate_matrix_unique
#check D0.Matter.ckm_no_free_matrix_at_fixed_basis_origin
#check D0.Matter.concreteCKMBasisOrigin
#check D0.Matter.concrete_ckm_origin_no_free_matrix
#check D0.Matter.generation_ordinal_adjacency_noncommute
#check D0.Matter.generation_up_down_selectors_noncommute
#check D0.Matter.generation_selectors_do_not_commute
#check D0.Matter.d0_generation_selectors_force_nonpermutation_overlap
#check D0.Matter.IsPermutationWitness
#check D0.Matter.IsUnistochasticOverlap
#check D0.Matter.generation_overlap_response_origin_closure
#check D0.Matter.finiteSelectorSupportFintype
#check D0.Matter.strict_selected_unique
#check D0.Matter.physical_selector_no_free_alternative
#check D0.Matter.different_selection_requires_score_change
#check D0.Matter.book04_selector_claim_no_free_alternative
#check D0.Matter.book04_different_selected_requires_score_change

-- Operator origin
#check D0.Algebra.commutator_self_zero
#check D0.Algebra.commutator_skew_of_skew
#check D0.Bridge.gauge_curvature_origin_closed
#check D0.Bridge.vector_operator_origin_closed
#check D0.Bridge.edge_stiffness_origin_closed

-- Scalar / vector / edge equations
#check D0.scalar_stationarity_implies_archive_poisson
#check D0.Matter.skew_stationarity_implies_vector_equation
#check D0.Matter.vector_operator_origin_applies_to_field_equation
#check D0.Geometry.symmOffDiag_stationarity_implies_edge_equation
#check D0.Geometry.edge_stiffness_preserves_symmOffDiag


-- SM-facing finite gauge/matter decomposition owners
#check D0.Gauge.frozenSMGaugeDecomposition
#check D0.Gauge.frozen_sm_gauge_factors_closed
#check D0.Gauge.frozen_sm_generation_ledger_closed
#check D0.Gauge.frozen_sm_generation_anomaly_free
#check D0.Gauge.no_alternative_sm_factors_at_frozen_ledger
#check D0.Gauge.no_alternative_sm_generation_ledger_at_frozen_decomposition
#check D0.Gauge.sm_eft_bridge_requires_frozen_decomposition
#check D0.Gauge.frozen_sm_eft_bridge_boundary_closed

-- Gauge kinetic positivity
#check D0.Algebra.skew_square_trace_nonpositive
#check D0.Algebra.minus_trace_square_nonnegative
#check D0.Algebra.gaugeKineticAction_nonnegative

-- Non-abelian boundary / no-go
#check D0.Gauge.flat_tensor_of_two_skew_is_symmetric
#check D0.Gauge.naive_flat_tensor_nonabelian_boundary
#check D0.Gauge.nonabelian_curvature_preserves_skew
#check D0.Gauge.residual_expands_by_definitions
#check D0.Gauge.discreteYangMillsAction_nonnegative_of_killing_nonpos
#check D0.Bridge.nonabelian_completion_boundary

-- Hurwitz / Lagrange local boundary and exact remaining gap
#check D0.Algebra.dim_one_admissible
#check D0.Algebra.dim_two_admissible
#check D0.Algebra.dim_four_admissible
#check D0.Algebra.dim_eight_admissible
#check D0.Algebra.hurwitz_local_boundary_split
#check D0.Algebra.remaining_hurwitz_open_is_single_precise_statement
#check D0.Algebra.d0_internal_dimension_value
#check D0.Algebra.d0_internal_dimension_value_mem
#check D0.Algebra.d0_admissible_internal_dimension_iff
#check D0.Algebra.d0_selector_closes_core_internal_dimension
#check D0.Algebra.global_hurwitz_classification_not_core_dependency

-- Matrix representation gauge transform boundary
#check D0.Gauge.gaugeTransformFinite_well_typed
#check D0.Gauge.discreteMaurerCartan_well_typed
#check D0.Gauge.matrixRepCurvature_well_typed
#check D0.Gauge.gaugeTransformFinite_preserves_skew_of_orthogonal
#check D0.Gauge.matrixRepCurvature_preserves_skew
#check D0.Gauge.matrix_rep_yang_mills_action_nonnegative_of_skew
#check D0.Gauge.abstract_lieRing_finite_transform_requires_associative_representation

-- Wilson-link gauge covariance and graded Bianchi closure
#check D0.Gauge.wilson_link_group_carrier_derivable
#check D0.Gauge.wilson_loop_covariance
#check D0.Gauge.naive_local_gauge_covariance_counterexample_fin3
#check D0.Topology.graded_nilpotency
#check D0.Topology.discrete_exact_bianchi
#check D0.Topology.graded_bianchi_exact
#check D0.Gauge.abelian_bianchi_exact
#check D0.Gauge.graded_bianchi_exact
#check D0.Gauge.ungraded_bianchi_residual_counterexample_fin2

-- Entropy cosmology
#check D0.Cosmology.homogeneous_fixed_point
#check D0.Cosmology.zero_mean_mode_has_underdense_region
#check D0.Cosmology.underdense_geometric_mode_generates_positive_acceleration
#check D0.Cosmology.softmax_flow_mass_preserving
#check D0.Probability.entropy_flow_linearization_zero_mean
#check D0.Cosmology.projection_preserves_mass


-- Cosmology reproducibility split owners
#check D0.Cosmology.InternalArchiveCosmologyObject
#check D0.Cosmology.SurveyLikelihoodPassport
#check D0.Cosmology.internal_archive_shape_independent_of_empirical_parameters
#check D0.Cosmology.survey_passport_preserves_internal_archive_shape
#check D0.Cosmology.survey_comparison_requires_nonempty_manifest
#check D0.Cosmology.survey_likelihood_cannot_promote_to_core_cosmology
#check D0.Cosmology.frozen_archive_cosmology_core_shape_closed

-- Spectral GR ladder
#check D0.Geometry.HeatTraceA2Decomposition.heat_trace_sq_exact_decomposition
#check D0.Geometry.HeatTraceA2Decomposition.double_count_factor_guard
#check D0.Geometry.HigherCurvatureSuppression.higher_curvature_suppression_by_floor
#check D0.Geometry.HigherCurvatureSuppression.higher_curvature_terms_below_finite_readout_cut
#check D0.Geometry.SpectralActionLadder.a0_is_volume_proxy
#check D0.Geometry.SpectralActionLadder.a2_is_eh_proxy
#check D0.Geometry.SpectralActionLadder.higher_powers_floor_bounded
#check D0.Geometry.finite_spin2_supplies_tt_macro_carrier
#check D0.Gravity.boundary_capacity_nonnegative
#check D0.Gravity.graph_laplacian_symmetric
#check D0.Gravity.conserved_flux_no_creation
#check D0.Gravity.entropic_tension_energy_nonnegative
#check D0.Gravity.entropic_archive_interface_closure
#check D0.Gravity.spectral_a2_eh_bridge_closed
#check D0.Gravity.finite_gravity_macro_constraints_closed
#check D0.Gravity.macro_tension_einstein_hilbert_interface_closed
#check D0.Gravity.finite_gravity_witness_yields_einstein_hilbert_interface

-- Passport boundary
#check D0.Cosmology.core_shape_independent_of_empirical_parameters
#check D0.Cosmology.empirical_passport_not_core_closed
#check D0.Traceability.external_likelihood_cannot_promote_to_core_closed

-- SI bridge calibration boundary
#check D0.Bridge.c0_c2_scale_action_values_only
#check D0.Bridge.c0_c2_cannot_alter_a0_a2_trace_shapes
#check D0.Bridge.si_calibration_belongs_to_bridge_calibration_status
#check D0.Bridge.si_calibration_cannot_promote_to_core_closed
#check D0.Bridge.core_traces_are_dimensionless
#check D0.Bridge.calibration_changes_only_action_scaling
#check D0.Bridge.calibration_changes_units_not_core_shape
#check D0.Bridge.no_si_observable_without_external_calibration
#check D0.Bridge.h0_gn_lambda_are_not_core_observables
#check D0.Bridge.si_observables_require_external_calibration

-- Unified interpretation spine
#check D0.Bridge.interpretation_package_keeps_core_dimensionless
#check D0.Bridge.interpretation_package_does_not_mutate_core_shape
#check D0.Bridge.si_readout_uses_single_external_calibration
#check D0.Bridge.interpretation_spine_has_single_si_readout
#check D0.Bridge.empirical_comparison_is_after_si_readout
#check D0.Bridge.interpretation_package_rg_readout_coherent
#check D0.Bridge.interpretation_package_spectral_action_readout_coherent
#check D0.Bridge.interpretation_package_cosmology_shape_readout_coherent
#check D0.Bridge.interpretation_package_gauge_readout_coherent
#check D0.Bridge.interpretation_package_passports_external
#check D0.Bridge.interpretation_spine_coherence_contract
#check D0.Bridge.interpretation_package_from_existing_anchors_coherent

#check D0_FINAL_FOUNDATION_INDEX
#check D0.finite_born_readout_unique_on_finite_outcomes
#check D0.finite_born_no_alternative_readout
#check D0.parallelogram_response_is_quadratic_form
#check D0.quarter_turn_quadratic_forces_norm_square
#check D0.born_quadratic_origin_closed
#check D0.Geometry.finite_spin2_tt_carrier_closed
#check D0.Geometry.finite_weak_field_quotient_yields_tt_representative
#check D0.Geometry.finite_gauge_trace_quotient_closed
#check D0.Geometry.finite_conserved_stress_spin2_coupling_closed
#check D0.Geometry.finite_trace_mode_removed_from_spin2_carrier
#check D0.Geometry.torus_shell_card_eq_three
#check D0.Geometry.TorusParameter.outer_inner_ratio
#check D0.Geometry.TorusParameter.major_minor_ratio
#check D0.Geometry.TorusParameter.equator_ratio
#check D0.Geometry.radial_hopping_phase_drift_commutator_01
#check D0.Geometry.radial_hopping_phase_drift_noncommute
#check D0.Geometry.torusCore13GeometryOriginClosure
#check D0.Dynamics.trace_evolution_unfolds_d0_geometry
#check D0.Dynamics.det_T
#check D0.Dynamics.det_T_pow
#check D0.Dynamics.toral_volume_conservation_square
#check D0.Dynamics.trace_T_pow_eq_signed_lucas
#check D0.Dynamics.generationTrace_eq_three
#check D0.Dynamics.abcdTrace_eq_four
#check D0.Dynamics.memoryTorusTrace_eq_eleven
#check D0.Dynamics.dark_sector_even_window_readout_zero
#check D0.Core.detector_fixed_under_time_ladder
#check D0.Core.readout_depends_on_time_power
#check D0.Core.active_archive_trace_readout_integer
#check D0.Dynamics.heat_moment_T2_eq_even_lucas_trace
#check D0.Dynamics.heat_moment_eq_even_lucas
#check D0.Dynamics.lefschetz_spectrum_unfolds_scene
#check D0.Dynamics.boundary_capacity_is_quarter_cut_weight
#check D0.Dynamics.saturated_region_forces_boundary_encoding
#check D0.Dynamics.black_hole_capacity_saturation_rule
#check D0.Dynamics.heat_trace_entropy_gradient_admits_gravity_interface
#check D0.Geometry.phi_phase_is_nonperiodic
#check D0.Geometry.finite_return_modulus_unfolds_branches
#check D0.Geometry.quasicrystal_order_not_periodic_lattice
#check D0.Physics.quasi_generation_inflation_orbit
#check D0.Physics.archive_phason_strain_em_dark_metric_visible
#check D0.Physics.window_offset_forces_chiral_readout
#check D0.Physics.phason_flip_drag_positive_cost
#check D0.Cosmology.phason_flip_entropy_nonnegative
#check D0.Cosmology.archive_pressure_is_phason_flip_entropy_osmosis
#check D0.Cosmology.phason_flip_transfer_matrix_has_sde_polynomial
#check D0.Cosmology.sde_roots_are_phason_flip_relaxation_modes
#check D0.Physics.fractional_charge_window_weights
#check D0.condensed_phi_vacuum_support_closed
#check D0.cut_project_quasicrystal_matches_phase_unfolding
#check D0.Physics.d0_phi_cut_project_matches_condensed_phi_vacuum
#check D0.Physics.quasicrystal_phenomenology_operator_origin
#check D0.Physics.galois_lorentz_signature_closed
#check D0.Dynamics.T_squared_plus_T_minus_identity_eq_zero
#check D0.Dynamics.det_T_pow_square_eq_one
#check D0.Dynamics.lucas_heat_moment_bridge
#check D0.Dynamics.detector_is_fixed_under_ladder
#check D0.Dynamics.d0_phi_quasicrystal_vacuum_support
#check D0.Dynamics.master_evolution_theorem
#check D0.Matter.phason_mode_card_eq_three
#check D0.Matter.generation_phason_mode_card_eq_three
#check D0.Matter.baryon_phason_triple_card_eq_27
#check D0.Matter.baryon_phason_symmetric_sector_dim_eq_ten
#check D0.Matter.phason_s3_symmetrizer_admits_baryon_decuplet_transfer
#check D0.Matter.full_baryon_multiplet_requires_phason_s3_symmetrizer
#check D0.Matter.phason_strain_generations_baryon_closure
#check D0.Matter.meson_phason_domain_wall_card_eq_six
#check D0.Matter.meson_domain_wall_generation_carrier_card_eq_eighteen
#check D0.Matter.meson_domain_wall_transfer_uses_lifted_defect
#check D0.Matter.meson_phason_domain_wall_closure
#check D0.Matter.same_shell_contact_index_zero_for_unmatched_valence_protons
#check D0.Matter.same_shell_contact_turns_on_for_matched_valence_pn
#check D0.Matter.mass_number_alone_cannot_determine_src_contact
#check D0.Matter.neutron_excess_alone_cannot_determine_src_contact
#check D0.Matter.nuclear_shell_contact_src_closure
#check D0.Matter.neutrino_neutral_leakage_is_bulk_phason_wave
#check D0.Matter.neutral_phason_wave_has_no_em_coupling
#check D0.Matter.delta0_over_four_is_phason_birefringence_seed
#check D0.Matter.hurwitz_gap_scattering_kernel_admissible
#check D0.Matter.phason_wave_decoherence_kernel_positive
#check D0.Passport.icecube_decoherence_passport_requires_external_manifest
#check D0.Passport.empty_icecube_manifest_cannot_run
#check D0.Passport.icecube_passport_uses_frozen_phason_kernel
#check D0.Matter.torus_geometry_forces_generation_selector_noncommute
#check D0.Matter.torus_shell_noncommutativity_forces_nonpermutation_overlap_source
#check D0.Matter.permutation_witness_has_no_nontrivial_flavour_transfer
#check D0.Matter.overlap_response_can_force_nonpermutation_transfer
#check D0.Matter.torus_overlap_generates_nonpermutation_flavour_transfer
#check D0.Matter.nontrivial_flavour_defect_positive_response
#check D0.Matter.nontrivial_flavour_defect_admissible_for_meson_transfer
#check D0.Matter.torus_shell_noncommutator_is_phason_connection_curvature
#check D0.Matter.phason_parallel_transport_around_shells_is_unitary
#check D0.Matter.phason_holonomy_response_has_multisupport_row
#check D0.Matter.phason_holonomy_response_not_permutation
#check D0.Matter.ckm_cp_phase_is_chiral_phason_bundle_twist
#check D0.Matter.ckm_matrix_is_phason_holonomy_on_torus_core13
#check D0.Geometry.PiTT4_idempotent
#check D0.Geometry.PiTT4_is_tt
#check D0.Geometry.PiTT4_kills_trace
#check D0.Geometry.PiTT4_kills_gauge
#check D0.Geometry.WTT4_preserves_tt
#check D0.Geometry.WTT4_energy_nonnegative
#check D0.Geometry.spin2_coupling_depends_only_on_tt_stress
#check D0.Geometry.tt_polarization_card_eq_two
#check D0.Geometry.finiteSpin2WaveOperatorConcreteClosure
#check D0.Bridge.internal_cone_speed_eq_one
#check D0.Bridge.finite_causal_tick_section_forces_same_tick
#check D0.Bridge.finite_causal_tick_section_cone_speed_eq_one
#check D0.Bridge.common_tick_rescaling_preserves_internal_cone_speed
#check D0.Bridge.asymmetric_ticks_not_internal_gauge
#check D0.Bridge.finite_lorentz_tick_gauge_cone_speed_closed
#check D0.Bridge.finite_lorentz_tick_gauge_signature_closed
#check D0.Bridge.finite_lorentz_tick_gauge_no_euclidean_export
#check D0.Bridge.finite_lorentz_tick_gauge_no_split_export
#check D0.Bridge.finite_lorentz_tick_rescaling_preserves_closure

end D0.Bridge

-- Multi-sector real-closure owners beyond Book 04 selector rewriting
#check D0.Matter.commutes_XZ_forces_scalar_matrix
#check D0.Matter.nonzero_gauge_idempotent_eq_identity
#check D0.Matter.rank1_scalar_projector_breaks_su2_gauge_compatibility
#check D0.Matter.rank2_scalar_projector_exists
#check D0.Matter.minimal_positive_scalar_projector_rank_two
#check D0.Matter.minimal_positive_scalar_projector_unique
#check D0.Matter.higgs_yukawa_core_promotion_valid
#check D0.NoGo.no_go_isolated_phason_generation_carrier
#check D0.NoGo.no_go_isolated_phason_baryon_s3_sector
#check D0.NoGo.no_go_euclidean_signature_export
#check D0.NoGo.no_go_stress_test_suite_closed
#check D0.Geometry.massless_spin2_physical_dof_four_eq_two
#check D0.Geometry.spin2_component_reduction_four_dimensional
#check D0.Geometry.concrete_spin2_dynamics_two_polarizations_closed
#check D0.Geometry.finite_spin2_four_role_dof_eq_two
#check D0.Matter.concrete_ckm_matrix_entries_closed
#check D0.Matter.frozen_ckm_exact_matrix_closed
#check D0.Matter.meson_support_projector_idempotent
#check D0.Matter.flavour_defect_positive_response
#check D0.Matter.meson_positive_defect_transfer_admissible
#check D0.Matter.meson_defect_transfer_origin_closure
#check D0.Matter.charged_lepton_transfer_muon_ratio_closed
#check D0.Matter.charged_lepton_transfer_tau_ratio_closed
#check D0.Matter.charged_lepton_transfer_exponents_closed

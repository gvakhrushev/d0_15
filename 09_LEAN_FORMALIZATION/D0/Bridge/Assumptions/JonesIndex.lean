namespace D0.Bridge

namespace BridgeAssumption

/-- External owner of the Jones subfactor-index quantization (V. F. R. Jones, *Index for
subfactors*, Invent. Math. 72(1), 1–25, 1983). The classical theorem is the OBSTRUCTION: the
index `[M:N]` of a type-II₁ subfactor takes, in the interval `[1,4)`, only the discrete values
`{4cos²(π/n) : n=3,4,5,…}`. D0 proves only the n=5 VALUE `4cos²(π/5)=φ²` exactly
(`D0-JONES-INDEX-PHI-001`); the quantization itself is assumed, not re-proved. -/
structure JonesIndexQuantization where
  /-- No index value exists in the open interval `(1,4)` other than the `4cos²(π/n)` series. -/
  noOtherIndexBelowFour : Prop
  cited : noOtherIndexBelowFour

end BridgeAssumption

abbrev JonesIndexQuantization := BridgeAssumption.JonesIndexQuantization

end D0.Bridge

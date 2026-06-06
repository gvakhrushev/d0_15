namespace D0.Bridge

namespace BridgeAssumption

structure GoldenBadlyApproximableAssumption where
  statement : Prop
  cited : statement

end BridgeAssumption

abbrev GoldenBadlyApproximableAssumption :=
  BridgeAssumption.GoldenBadlyApproximableAssumption

end D0.Bridge

namespace D0.Bridge

namespace BridgeAssumption

structure CompactLieKillingNegative where
  statement : Prop
  cited : statement

end BridgeAssumption

abbrev CompactLieKillingNegative :=
  BridgeAssumption.CompactLieKillingNegative

end D0.Bridge

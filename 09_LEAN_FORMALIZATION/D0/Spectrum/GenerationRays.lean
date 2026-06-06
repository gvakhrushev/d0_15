import Mathlib.Tactic

namespace D0

/-!
No generation-ray theorem is proved here: the spectral-ray object has not been
mathematically defined from an exact finite D0 operator.
-/

def GenerationRayObjectDefined : Prop := False

theorem generation_rays_not_defined :
    ¬ GenerationRayObjectDefined := by
  intro h
  exact h

end D0


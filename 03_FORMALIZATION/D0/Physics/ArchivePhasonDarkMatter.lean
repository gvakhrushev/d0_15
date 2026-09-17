namespace D0.Physics

/-!
D0-QUASI-002 archive phason owner.

Archive phason strain is invisible to the active EM projection but contributes
positive finite strain energy to the metric/heat readout.
-/

structure PhasonStrainField where
  energy : Rat
  energy_nonnegative : 0 <= energy

def EMCouplingArchive (_w : PhasonStrainField) : Rat :=
  0

structure GravityCouplingArchive (w : PhasonStrainField) where
  response : Rat
  positive : 0 < response
  response_eq_energy : response = w.energy

def metricArchiveCoupling
    (w : PhasonStrainField) (h : 0 < w.energy) :
    GravityCouplingArchive w where
  response := w.energy
  positive := h
  response_eq_energy := rfl

theorem archive_phason_strain_is_dark_to_em
    (w : PhasonStrainField) :
    EMCouplingArchive w = 0 := by
  rfl

theorem archive_phason_strain_can_source_metric_response
    (w : PhasonStrainField) (h : 0 < w.energy) :
    exists G : GravityCouplingArchive w, 0 < G.response := by
  exact ⟨metricArchiveCoupling w h, h⟩

theorem archive_phason_strain_em_dark_metric_visible
    (w : PhasonStrainField) (h : 0 < w.energy) :
    EMCouplingArchive w = 0 /\
      exists G : GravityCouplingArchive w, 0 < G.response := by
  exact
    ⟨archive_phason_strain_is_dark_to_em w,
      archive_phason_strain_can_source_metric_response w h⟩

end D0.Physics

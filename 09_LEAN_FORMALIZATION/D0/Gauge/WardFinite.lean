import D0.Topology.BoundaryBoundary
import D0.Gauge.AnomalySums

namespace D0

structure WardFiniteCertificate where
  boundaryLaw : ∀ {m n k : ℕ} (I : IncidencePair m n k), I.d1 * I.d2 = 0
  anomalyGrav : gravU1Sum = 0
  anomalyCubic : cubicU1Sum = 0

def finiteWardCertificate : WardFiniteCertificate where
  boundaryLaw := boundary_boundary_zero
  anomalyGrav := grav_U1_anomaly_sum
  anomalyCubic := U1_cubic_anomaly_sum

end D0

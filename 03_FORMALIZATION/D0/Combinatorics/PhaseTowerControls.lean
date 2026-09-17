import D0.Combinatorics.PhaseTowerMinimality

namespace D0

theorem not_terminal_43 :
    ¬ TerminalSynchronized C0 43 := by
  intro h
  norm_num [TerminalSynchronized, C0, ABCDn, D2n, V11n, V9n, Omega8n] at h

theorem not_terminal_45 :
    ¬ TerminalSynchronized C0 45 := by
  intro h
  norm_num [TerminalSynchronized, C0, ABCDn, D2n, V11n, V9n, Omega8n] at h

theorem not_full_oriented_709 :
    ¬ FullOrientedSynchronized C0 709 := by
  intro h
  norm_num [FullOrientedSynchronized, C0, pointedAlphabet, fullOrientedLength,
    ABCDn, D2n, Vtotaln, V9n, V11n, V13n, Omega8n] at h

theorem not_full_oriented_711 :
    ¬ FullOrientedSynchronized C0 711 := by
  intro h
  norm_num [FullOrientedSynchronized, C0, pointedAlphabet, fullOrientedLength,
    ABCDn, D2n, Vtotaln, V9n, V11n, V13n, Omega8n] at h

end D0

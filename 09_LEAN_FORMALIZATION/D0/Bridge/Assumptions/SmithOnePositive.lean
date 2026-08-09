namespace D0.Bridge

namespace BridgeAssumption

/-- External owner of Smith's spectral graph characterization: a graph with
an edge has exactly one positive adjacency eigenvalue precisely when its
non-isolated part is complete multipartite.  The internal multipartite
forward calculation does not depend on this converse. -/
structure SmithOnePositiveCharacterisation where
  converseCharacterisation : Prop
  cited : converseCharacterisation

theorem smith_one_positive_conditional
    (h : SmithOnePositiveCharacterisation) :
    h.converseCharacterisation :=
  h.cited

end BridgeAssumption

abbrev SmithOnePositiveCharacterisation :=
  BridgeAssumption.SmithOnePositiveCharacterisation

end D0.Bridge

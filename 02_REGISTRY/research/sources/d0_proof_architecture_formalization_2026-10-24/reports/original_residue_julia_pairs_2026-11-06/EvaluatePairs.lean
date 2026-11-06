import D0.Algebra.OriginalBookResidueJuliaPairs
open D0.Algebra.OriginalBookResidueJuliaPairs


def main : IO Unit := do
  for minus in [false,true] do
    for mode in List.finRange 4 do
      for row in List.finRange 4 do
        let pair := residueRowPair minus mode row
        for port in List.finRange 2 do
          let m := if port.val = 0 then pair.1 else pair.2
          for i in List.finRange 16 do
            let entries := (List.finRange 16).map fun j => (m i j).val
            IO.println (String.intercalate "," (entries.map toString))
#eval main

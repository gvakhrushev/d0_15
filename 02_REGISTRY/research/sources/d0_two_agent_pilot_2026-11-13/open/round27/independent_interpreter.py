#!/usr/bin/env python3
"""Standalone signed-permutation interpreter; no compiler internals imported."""
def run(gates,word):
 phase=1
 for gate in gates:
  op=gate.op;w=gate.wires
  if op=='X':word ^= 1<<w[0]
  elif op=='CX':
   if word & (1<<w[0]):word ^= 1<<w[1]
  elif op=='CCX':
   mask=(1<<w[0])|(1<<w[1])
   if word&mask==mask:word ^= 1<<w[2]
  elif op=='Z':
   if word & (1<<w[0]):phase=-phase
  elif op=='CZ':
   mask=(1<<w[0])|(1<<w[1])
   if word&mask==mask:phase=-phase
  else:raise ValueError(op)
 return word,phase

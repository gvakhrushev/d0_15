#!/usr/bin/env python3
"""Fixed cap-K quantum-payload router; logical X/CX/CCX gate grammar.
Retains all attempts' A/B/C wires and one-hot choice; cleans survive work.
"""
from collections import Counter

def layout(K):
 assert isinstance(K,int) and K>=1
 attempts=[{'A':3*i,'B':3*i+1,'C':3*i+2} for i in range(K)]
 return {'K':K,'attempts':attempts,'output':3*K,'ready':3*K+1,
         'survive':list(range(3*K+2,4*K+3)),
         'chosen':list(range(4*K+3,5*K+3)),'qubits':5*K+3}

def router(K):
 q=layout(K);word=[('X',q['survive'][0])]
 for i in range(K):
  si,snext=q['survive'][i:i+2];flag=q['attempts'][i]['C'];ch=q['chosen'][i]
  word.extend([('CCX',si,flag,ch),('CX',si,snext),('CX',ch,snext)])
 # XOR OR(C) into arbitrary ready bit, without changing any attempt flag.
 word.extend([('X',q['ready']),('CX',q['survive'][-1],q['ready'])])
 for i in range(K):
  x=q['attempts'][i]['A'];o=q['output'];ch=q['chosen'][i]
  word.extend([('CX',x,o),('CCX',ch,o,x),('CX',x,o)])
 # Keep chosen as a record; erase survive in reverse using its defining XOR.
 for i in reversed(range(K)):
  word.extend([('CX',q['chosen'][i],q['survive'][i+1]),('CX',q['survive'][i],q['survive'][i+1])])
 word.append(('X',q['survive'][0]))
 c=Counter(g[0] for g in word)
 assert c=={'X':3,'CX':6*K+1,'CCX':2*K} and len(word)==8*K+4
 return q,word

def parity_kernel(q):
 # Owner's 2G+3CX kernel from three COMPUTATIONAL ZERO inputs.
 return [('G',q['A']),('G',q['B']),('CX',q['A'],q['C']),('CX',q['B'],q['C']),('CX',q['A'],q['B'])]

def serial(q,word):
 return {'schema':'d0.fixed.fair-payload-router.v1','basis':['X','CX','CCX'],'layout':q,
         'gates':[{'op':x[0],'wires':list(x[1:])} for x in word],
         'counts':dict(Counter(x[0] for x in word)),'retained':'all A/B/C attempts and chosen; survive cleared','native_compiled':False,'GR_closed':False}

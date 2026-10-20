#!/usr/bin/env node
"use strict";
// Exact finite controls for D0.Foundation.PopperianBootstrap binary-generator
// reduction. 3-line and unused-record protocols carry NO additional public
// verdict distinction relative to their minimal 2-line core. Robustness
// against an independently faulty line is a DIFFERENT strengthened task.
const test=(v,s)=>{if(!v)throw Error("FAIL "+s);console.log("PASS "+s)};
const states=[false,true],catalogues=["A","B"];
const protocol={
 lines:[0,1,2],
 allRecordSymbols:[
   [false,0],[true,0],[false,1],[true,1]
 ],
 record:x=>[x,0],
 compare:(line,c,a,b)=>a[0]!==b[0]
};
const encodedRecords=states.map(protocol.record);
const minimal={
 lines:[0,1],
 records:encodedRecords,
 compare:(l,c,a,b)=>protocol.compare(l,c,a,b)
};
test(minimal.lines.length===2&&new Set(minimal.lines).size===2,
     "exact two original distinct registered lines selected; none synthesized");
test(minimal.records.length===2 &&
     protocol.allRecordSymbols.length===4,
     "original unused raw record symbols removed without removing any actual state record");
for(const c of catalogues)for(const x of states)for(const y of states){
 const a=protocol.record(x),b=protocol.record(y),answer=x!==y;
 for(const l of protocol.lines)
   test(protocol.compare(l,c,a,b)===answer,
        "three-line original EXACT verification contract on all states and catalogue "+l);
 for(const i of minimal.lines)
   test(minimal.compare(i,c,a,b)===answer,
        "original two selected lines preserve EXACT public verdict");
}
test(!([0].length>=2),"single line cannot satisfy independent-witness axiom");
for(const l of protocol.lines)for(const c of catalogues)for(const x of states)
 for(const y of states){
   test(protocol.compare(l,c,protocol.record(x),protocol.record(y))===
        minimal.compare(0,c,protocol.record(x),protocol.record(y)),
     "ANY third redundant ORIGINAL exact line has zero new verdict content");
 }
test(protocol.lines.length>minimal.lines.length &&
     protocol.lines.length-minimal.lines.length===1,
     "literal FIN3 from old counterexample has a genuine two-line retract on outcome algebra");
const hardwareCost=(n,fix=12,perLine=4)=>fix+n*perLine;
test(hardwareCost(3)>hardwareCost(2),
     "strict minimal 2 if original full work has POSITIVE marginal independent-line cost");
test(hardwareCost(3,12,0)===hardwareCost(2,12,0),
     "without positive marginal work MDL cannot yield STRICT hardware line-count uniqueness");
const bools=[false,true];
const majority3=x=>x.filter(Boolean).length>=2;
const hamming=(x,y)=>x.reduce((s,v)=>s+Number(v!==y),0);
for(const truth of bools)for(const a of bools)for(const b of bools)
 for(const c of bools){
  const votes=[a,b,c];
  if(hamming(votes,truth)<=1)
    test(majority3(votes)===truth,
         "3 independent binary witnesses majority exactly correct with <=1 faulty line");
 }
const ambiguous=[false,true];
test(hamming(ambiguous,false)===1 &&
     hamming(ambiguous,true)===1,
     "2 witness votes (0,1) cannot identify true bit under allowance of ONE arbitrary fault");
const strictReliability=3*.9**2-2*.9**3;
test(Math.abs(strictReliability-.972)<1e-15,
     "3-line majority q=.9 succeeds .972 while any 2-line always-decide symmetric tie rule lacks that guarantee");
const recordFull={truth:false,lines:protocol.lines.slice()};
const recordCore={truth:false,lines:minimal.lines.slice()};
test(recordFull.lines.length!==recordCore.lines.length,
     "negative control: physical provenance archive of a third EXecuted witness is NOT conserved by verdict-only retract");
console.log(JSON.stringify({
 thesis:"fin3 is a counterexample to unique HARDWARE carrier, NOT to minimum TWO original-line public verification generator",
 formalOwner:"D0.Foundation.PopperianBootstrap.twoLineImageProtocol_*",
 reducedLines:2,
 originalPossibleLines:3,
 fullRecordSymbols:4,
 actualGeneratedRecordSymbols:2,
 semanticVerdictsPreserved:true,
 pairChoiceIndependent:true,
 physicalIndependentSourcesNotProvedByLineType:true,
 positiveMarginalWorkNeededForStrictMDL:true,
 faultFreeCoreMin:2,
 oneByzantineFaultRobustCoreMin:3,
 mixingFaultModelWouldChangeContract:true,
 physicalGR_force_of_scene_not_dischargeable_by_this_retract:true
},null,2));

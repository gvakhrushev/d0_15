// Exact existing Golden G inverse via native NOT conjugation; coherent
// fully charged U† CZ U palindrome without a nonnative inverse gate.
// This checks a literal 3-qubit native circuit, all 8 columns, no
// postselected output or erased measured transcript. No physical Book
// selection or native field resource writer claimed.
const ck=(x,m)=>{if(!x)throw Error("FAIL "+m)}
const p=(Math.sqrt(5)-1)/2,a=Math.sqrt(p);
const G=[[a,-p],[p,a]],X=[[0,1],[1,0]],H=[[1,1],[1,-1]].map(r=>r.map(x=>x/Math.sqrt(2)));
const mul=(A,B)=>A.map(row=>Array.from({length:B[0].length},(_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)));
const T=A=>A[0].map((_,j)=>A.map(x=>x[j]));
const I=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const diff=(A,B)=>Math.max(...A.flatMap((row,i)=>row.map((x,j)=>Math.abs(x-B[i][j]))));
ck(Math.abs(a*a+p*p-1)<1e-15,"native Golden p+p²=1");
ck(diff(mul(mul(X,G),X),T(G))<1e-15,"literal X G X is G^-1 exact");
ck(diff(mul(G,mul(X,mul(G,X))),I(2))<2e-15,"native inverse palindrome identity");
const N=3,d=1<<N;
const single=(qubit,A)=>Array.from({length:d},(_,i)=>Array.from({length:d},(_,j)=>{
 if((i & ~(1<<qubit))!==(j & ~(1<<qubit)))return 0;
 return A[(i>>qubit)&1][(j>>qubit)&1];
}));
const cnot=(c,t)=>Array.from({length:d},(_,i)=>Array.from({length:d},(_,j)=>+(i===(j^(((j>>c)&1)<<t)))));
const cz=(c,t)=>Array.from({length:d},(_,i)=>Array.from({length:d},(_,j)=>+(i===j)*(((j>>c)&1)&&((j>>t)&1)?-1:1)));
const steps=[
{n:"G",q:0},{n:"CNOT",c:0,t:1},{n:"G",q:2},{n:"H",q:1},
{n:"CNOT",c:1,t:2},{n:"G",q:1},{n:"X",q:0},
{n:"H",q:2},{n:"CNOT",c:0,t:2},{n:"G",q:0}
];
const gate=s=>s.n==="G"?single(s.q,G):s.n==="H"?single(s.q,H):s.n==="X"?single(s.q,X):cnot(s.c,s.t);
const exactInverseSteps=s=>s.n==="G"?[{n:"X",q:s.q},{n:"G",q:s.q},{n:"X",q:s.q}]:[s];
const assemble=word=>word.reduce((u,g)=>mul(gate(g),u),I(d));
const forward=assemble(steps);
const reverse=steps.slice().reverse().flatMap(exactInverseSteps);
const inverse=assemble(reverse);
ck(diff(inverse,T(forward))<4e-14,"all 8 original word columns inverted by native NOT/Golden/G/H/CNOT only");
ck(diff(mul(inverse,forward),I(d))<5e-14,"full data+work inversion, not only blank");
const natCZ=mul(mul(single(2,H),cnot(1,2)),single(2,H));
ck(diff(natCZ,cz(1,2))<4e-15,"phase CZ compiled from existing H and CNOT");
const palindrome=mul(mul(inverse,natCZ),forward);
ck(diff(mul(palindrome,palindrome),I(d))<1e-13,"complete genuine native reflection U† CZ U");
ck(diff(palindrome,T(palindrome))<1e-13,"reflection selfadjoint all columns");
const input=[1,0,0,0,0,0,0,0];
const clean=palindrome[0][0],raw=forward.map(row=>row[0]);
const click=raw.reduce((s,amp,i)=>s+(((i>>1)&1)&&((i>>2)&1)?amp*amp:0),0);
ck(Math.abs(clean-(1-2*click))<4e-14,"true success projector and completely recorded work");
const f=1-clean*clean;
ck(f>0&&f<1&&Math.abs(f-4*click*(1-click))<5e-14,"whole complementary F eigenvalue positive Book");
const chargedForward=steps.length,chargedInverse=reverse.length,chargedCZ=3;
ck(chargedInverse===chargedForward+2*steps.filter(g=>g.n==="G").length,"literal nonfree Golden inversion price");
function report(){return{
status:"PASS_NATIVE_GOLDEN_BOOLEAN_COHERENT_DOUBLE_PASS",
original_F_R_amplitude_G:[[a,-p],[p,a]],inverse_identity:"G^(-1) = X G X (same Golden gate + 2 charged NOT)",
complete_charged_gate_counts:{forward:chargedForward,reverse:chargedInverse,phase_comparator:chargedCZ,total:chargedForward+chargedInverse+chargedCZ},
all8_input_columns_unitary:true,pretrace_work_deferred:true,
coherent_clean_return_amplitude:clean,click_probability:click,true_Book_complement_eigenvalue:f,
requires_gate_factory_herald_coherent_or_correctly_conditioned:true,
original_field_resource_writer_selection_unproved:true,
full_native_Book_Info_selection_unproved:true,
GR_closed:false};}
if(typeof console!=="undefined")console.log(JSON.stringify(report(),null,2));

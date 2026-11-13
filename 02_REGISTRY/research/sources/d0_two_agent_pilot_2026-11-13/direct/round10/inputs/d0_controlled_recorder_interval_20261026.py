"""Independent dyadic certification of the returned signed SK DAG and W649.

Only integer outward arithmetic and the original algebraic G enter the
certificate; no printed quaternion, angle, net metric or float eps is trusted.
Native plane expansion is separately bound to the owned checked macro.
"""
import argparse,hashlib,importlib.util,json,math,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent

def digest(b): return hashlib.sha256(b).hexdigest()

class Dyadic:
    def __init__(self,bits): self.bits=bits;self.D=1<<bits
    def const(self,n): return (int(n)*self.D,int(n)*self.D)
    def neg(self,a): return (-a[1],-a[0])
    def add(self,a,b): return (a[0]+b[0],a[1]+b[1])
    def sub(self,a,b): return self.add(a,self.neg(b))
    def mul(self,a,b):
        ps=[x*y for x in a for y in b]
        return (min(ps)//self.D,-((-max(ps))//self.D))
    def rat(self,n,d=1):
        if d<=0: raise ValueError('positive denominator required')
        return ((n*self.D)//d,-((-(n*self.D))//d))
    def root(self,a):
        if a[0]<0: raise ValueError('negative square-root endpoint')
        low=math.isqrt(a[0]*self.D); high=math.isqrt(a[1]*self.D)
        if high*high<a[1]*self.D: high+=1
        return low,high
    def identity(self,n): return [[self.const(int(i==j)) for j in range(n)] for i in range(n)]
    def mm(self,A,B):
        if len(A[0])!=len(B): raise ValueError('matrix dimensions')
        return [[self.sum(self.mul(A[i][k],B[k][j]) for k in range(len(B)))
                 for j in range(len(B[0]))] for i in range(len(A))]
    def sum(self,vs):
        lo=hi=0
        for v in vs: lo+=v[0];hi+=v[1]
        return lo,hi
    @staticmethod
    def tr(A): return [list(row) for row in zip(*A)]
    def power(self,A,n):
        if n<0: return self.power(self.tr(A),-n)
        result=self.identity(len(A))
        while n:
            if n&1: result=self.mm(A,result)
            n//=2
            if n: A=self.mm(A,A)
        return result
    def plane(self,n,i,j,c,s):
        A=self.identity(n);A[i][i]=c;A[i][j]=self.neg(s);A[j][i]=s;A[j][j]=c
        return A
    def frobenius_upper(self,A,B):
        ss=sum(max(abs(v) for v in self.sub(a,b))**2 for ra,rb in zip(A,B) for a,b in zip(ra,rb))
        r=math.isqrt(ss)
        return r+int(r*r<ss)
    def field_poly(self,coefficients,a):
        value=self.const(0)
        for coefficient in coefficients:
            parts=coefficient.split('/')
            term=self.rat(int(parts[0]),int(parts[1]) if len(parts)==2 else 1)
            value=self.add(self.mul(value,a),term)
        return value

def load_checked(path,expected=None):
    b=path.read_bytes()
    if expected and digest(b)!=expected: raise ValueError('input SHA mismatch')
    return json.loads(b),digest(b)

def evaluate_bundle(bundle,iv):
    if bundle['schema']!='d0.so3-sk-signed-word/1': raise ValueError('schema')
    # p=(sqrt5-1)/2,a=sqrtp in the original positive real embedding.
    p=iv.mul(iv.sub(iv.root(iv.const(5)),iv.const(1)),iv.rat(1,2))
    a=iv.root(p)
    G=[[a,iv.neg(p)],[p,a]]
    G32=iv.power(G,32)
    generators={1:iv.plane(3,0,1,G32[0][0],G32[1][0]),
                2:iv.plane(3,0,2,G32[0][0],G32[1][0])}
    generators[-1]=iv.tr(generators[1]);generators[-2]=iv.tr(generators[2])
    matrices=[];counts=[]
    for index,node in enumerate(bundle['nodes']):
        kind=node['kind']
        if kind=='seq':
            A=iv.identity(3);n1=n2=0
            for letter in node['letters']:
                if type(letter) is not int or letter not in generators: raise ValueError('letter')
                A=iv.mm(generators[letter],A)
                n1+=int(abs(letter)==1);n2+=int(abs(letter)==2)
        elif kind=='inv':
            child=node['child']
            if type(child) is not int or not 0<=child<index: raise ValueError('non-topological inverse')
            A=iv.tr(matrices[child]);n1,n2=counts[child]
        elif kind=='cat':
            A=iv.identity(3);n1=n2=0
            for child in node['children']:
                if type(child) is not int or not 0<=child<index: raise ValueError('non-topological concatenation')
                A=iv.mm(matrices[child],A);c1,c2=counts[child];n1+=c1;n2+=c2
        else: raise ValueError('unknown node')
        if type(node['length']) is not int or node['length']!=n1+n2: raise ValueError('length mismatch')
        matrices.append(A);counts.append((n1,n2))
    targets={}
    for report in bundle['targets']:
        name=report['name'];r=report['root']
        if name not in ('theta_G','quarter') or name in targets or type(r) is not int or not 0<=r<len(matrices): raise ValueError('target')
        ideal=iv.plane(3,0,1,a,p) if name=='theta_G' else iv.plane(3,0,1,iv.const(0),iv.const(1))
        n1,n2=counts[r]
        if report['abstract_letter_length']!=n1+n2: raise ValueError('report length')
        targets[name]={'matrix':matrices[r],'counts':(n1,n2),
                       'error_int':iv.frobenius_upper(matrices[r],ideal),'root':r}
    if set(targets)!=set(('theta_G','quarter')): raise ValueError('missing target')
    reached=set();pending=[t['root'] for t in targets.values()]
    while pending:
        i=pending.pop()
        if i in reached: continue
        reached.add(i);node=bundle['nodes'][i]
        pending.extend(node.get('children',[]))
        if 'child' in node: pending.append(node['child'])
    if len(reached)!=len(bundle['nodes']): raise ValueError('unreachable witness nodes')
    return targets,a,p

def macro_counts(i,j):
    t=bin(i^j).count('1')-1
    if not 0<=t<=3: raise ValueError('plane')
    return {'G':32,'SourceI':32,'CX':70+2*t}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--bundle',type=Path,default=BASE/'d0_so3_sk_compiler_20261026.json')
    p.add_argument('--factor',type=Path,default=BASE/'d0_recorder_so16_factor_20261026.json')
    p.add_argument('--bits',type=int,default=256)
    p.add_argument('--output',type=Path,default=BASE/'d0_controlled_recorder_interval_20261026.json')
    args=p.parse_args()
    if args.bits<192: raise ValueError('at least192 certificate bits')
    bundle,bundle_sha=load_checked(args.bundle,'0d5d7fab0dcd22b06be115afb2da60164546c83daacf0d9be0abadf8e1d4c5ee')
    factor,factor_sha=load_checked(args.factor,'259953482ecab31a1fc8dc0e93c8e49fda2a9825cc5c3339100e6d8a7c0f7645')
    iv=Dyadic(args.bits)
    targets,a,pg=evaluate_bundle(bundle,iv)
    th,qu=targets['theta_G'],targets['quarter']
    angle={0:(iv.tr(qu['matrix']),qu['counts']),1:(th['matrix'],th['counts']),
           2:(iv.mm(qu['matrix'],iv.tr(th['matrix'])),tuple(x+y for x,y in zip(th['counts'],qu['counts']))),
           3:(qu['matrix'],qu['counts']),4:(iv.tr(th['matrix']),th['counts'])}
    whole=iv.identity(16);ideal_whole=iv.identity(16)
    inventory={'G':0,'SourceI':0,'CX':0};abstract=0
    for row in factor['chronological_givens']:
        i,j,k,ai=(row[x] for x in ('i','j','k','angle_id'))
        mat,counts=angle[ai]
        embedded=iv.identity(16)
        indices=(i,j,k)
        for u in range(3):
            for v in range(3): embedded[indices[u]][indices[v]]=mat[u][v]
        whole=iv.mm(embedded,whole)
        coeff=factor['unique_angles'][ai]
        c=iv.field_poly(coeff['cos_coeffs'],a);s=iv.field_poly(coeff['sin_coeffs'],a)
        ideal_whole=iv.mm(iv.plane(16,i,j,c,s),ideal_whole)
        for count,plane in zip(counts,((i,j),(i,k))):
            for key,value in macro_counts(*plane).items(): inventory[key]+=count*value
        abstract+=sum(counts)
    error_int=iv.frobenius_upper(whole,ideal_whole)
    # Bind every actually used plane/sign to the checked owned native macro.
    hp=BASE/'d0_controlled_plane_native_20261026.py'
    helper_sha=digest(hp.read_bytes())
    if helper_sha!='55929a5cc916cf9880907ec246fd7abf25366c4598320a6d63a341bbfe8f7ead':
        raise ValueError('native plane helper SHA')
    spec=importlib.util.spec_from_file_location('d0_recorder_interval_plane',hp)
    H=importlib.util.module_from_spec(spec);sys.modules[spec.name]=H;spec.loader.exec_module(H)
    compiler=H.Compiler(8,physical_port=0,spin=(5,6))
    used=set()
    for factor_row in factor['chronological_givens']:
        i,j,k=(factor_row[v] for v in ('i','j','k'))
        used.update(((i,j),(i,k)))
    hashes=[]
    for i,j in sorted(used):
        for sign in (1,-1):
            w,metadata=H.plane_word(compiler,(1,2,3,4),7,i,j,sign)
            actual=compiler.counts(w).as_dict();expected=macro_counts(i,j)
            if actual!={**expected,'N':sum(expected.values()),'g_port':32,'g_off':0}:
                raise ValueError('plane native inventory binding')
            if len(metadata['linear_CX'])!=bin(i^j).count('1')-1:
                raise ValueError('linear plane conjugation')
            ex=compiler.execution(w,expansion_limit=10000)
            H.native.validate_execution(ex,max_qubits=8,max_expanded_stages=10000)
            if any(g.op=='G' and g.wires!=(0,) for g in ex.gates):
                raise ValueError('off-port primitive G')
            if any(g.op=='CX' and g.wires[1]==7 for g in ex.gates):
                raise ValueError('orientation flag is not readonly')
            hashes.append(digest(H.native.canonical_json(ex).encode()))
    macro_set_sha=digest(('\n'.join(hashes)+'\n').encode())
    # One actual outer parking SWAP on each side handles the physical source
    # port as a target coordinate. No source-port content is silently blanked.
    inventory['CX']+=6
    Nv=sum(inventory.values())
    total={key:2*value for key,value in inventory.items()};total['CX']+=1
    Ntotal=sum(total.values())
    # Semantic inverse expands freshly signed, exact inverse macros. Literal
    # raw inverse is a DIFFERENT conservative word with the following count.
    literal_inverse={'G':inventory['G'],'CX':inventory['CX'],
                     'SourceI':4*inventory['G']+3*inventory['SourceI']}
    # Frobenius dominates operator norm; pure integer strict budgets.
    assert error_int*10**39<2*iv.D
    assert error_int*Ntotal*(1<<20)<iv.D
    assert error_int*Ntotal*10**29<2*iv.D
    # Complete feedback-normal debt at this specified projection target:
    # |DJ|<=8 z R delta/(1-z)^2*(N nu+2 mu), R=163840 in the
    # DATA16/Spin4/old128/free-tag extension, z=2^-20.
    zden=1<<20;R=163840
    debt_num=8*R*zden*error_int*Ntotal
    debt_den=(zden-1)**2*iv.D
    assert debt_num*10**29<2*debt_den
    result={'status':'PASS','arithmetic':'outward dyadic integer intervals',
      'bits':args.bits,'bundle_sha256':bundle_sha,'factor_sha256':factor_sha,
      'reachable_nodes':len(bundle['nodes']),'exact_Givens':len(factor['chronological_givens']),
      'angle_error_dyadics':{name:{'upper_numerator':t['error_int'],'denominator_power2':args.bits,
         'counts_axis1_axis2':t['counts']} for name,t in targets.items()},
      'full_SO16_error':{'upper_numerator':error_int,'denominator_power2':args.bits,
                        'strict_bound':'<2e-39'},
      'native_macro_helper_sha256':helper_sha,'native_macro_instance_count':len(hashes),
      'native_macro_instance_set_sha256':macro_set_sha,'abstract_plane_letters':abstract,'controlled_V_native_inventory':inventory,
      'controlled_V_raw_stages':Nv,'literal_inverse_inventory':literal_inverse,
      'implemented_inverse':'fresh signed inverse macro expansion, not literal raw inverse',
      'tagged_controller_inventory':total,'tagged_controller_stages':Ntotal,
      'strict_delta_times_total_stages_bound':'<2e-29 (hence <2^-20)',
      'cut_rank_promise':'FREE active tag and Spin4/DATA16/oldRIGHT128; outer parking spare BLANK, restored on all columns',
      'feedback_source_raw_stage_dual_bound':{'numerator':debt_num,'denominator':debt_den,
        'strict_bound':'<2e-29 for nu=1, mu=0, R=163840, z=2^-20; not a GR42 source bound'},
      'full_matrix_target':'W649 after physical port park, all16columns and exact false sector',
      'physical_full33_placement':False,'paired_cut_selection':False,'GR_closed':False}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

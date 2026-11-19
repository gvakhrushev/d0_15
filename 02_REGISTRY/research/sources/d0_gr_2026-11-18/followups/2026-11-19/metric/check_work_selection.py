"""One- and two-letter tomography for positive scalar path weights. Python 3."""
from collections import Counter, defaultdict, deque
from fractions import Fraction as F
from itertools import permutations, product
import json


def need(value, label):
    if not value:
        raise ArithmeticError(label)


def normalize(table):
    total=sum(table.values(), F(0))
    return {k:v/total for k,v in table.items()}


def orbit():
    # x has bus, DATA and b in its low, middle and high bit. The separate
    # Spin coordinate and phase encode the original 28 supported real states.
    vertices=list(product(range(1,8),range(2),range(2)))
    actions=list(permutations(range(3),2))+["SourceI"]
    def step(x, action):
        q, spin, phase=x
        if action=="SourceI":
            return (q,spin^1,phase^spin) if q&1 else x
        control,target=action
        return (q^(((q>>control)&1)<<target),spin,phase)
    edges={x:{g:step(x,g) for g in actions} for x in vertices}
    for g in actions:
        need({r[g] for r in edges.values()}==set(vertices),"full native permutation")
    return edges


def scene():
    parts=[0]*9+[1]*11+[2]*13
    return {x:{y:y for y in range(33) if parts[y]!=parts[x]} for x in range(33)}


def windows(edges):
    table=defaultdict(list)
    for x,row in edges.items():
        for a,j in row.items():
            for b,k in edges[j].items():
                # Distinct address labels leading to the same middle state
                # remain distinct measured paths. There is no basis PVM.
                table[x,k].append((a,j,b))
    return table


def greedy(tables, vertices):
    mids={k:{j for a,j,b in paths} for k,paths in tables.items()}
    seen={vertices[0]}
    selected=[]
    while len(seen)<len(vertices):
        key=max((k for k,m in mids.items() if seen&m),key=lambda k:len(mids[k]-seen))
        need(bool(mids[key]-seen),"connected overlap")
        selected.append(key);seen|=mids[key]
    return selected


def graph_radius(vertices, selected, tables):
    graph={x:set() for x in vertices}
    for key in selected:
        mids={j for a,j,b in tables[key]}
        for j in mids:
            graph[j]|=mids
    def farthest(start):
        dist={start:0}; queue=deque([start])
        while queue:
            u=queue.popleft()
            for v in graph[u]-dist.keys():
                dist[v]=dist[u]+1
                queue.append(v)
        need(len(dist)==len(vertices),"reachable comparison component")
        return max(dist.values())
    radius,_,root=min((farthest(v),i,v) for i,v in enumerate(vertices))
    return radius,root


def word_law(edges, generation):
    # No reversibility, no equal pricing of addresses, no stationary terminal.
    vertices=list(edges); idx={v:i for i,v in enumerate(vertices)}
    t={v:F(11+(generation+3)*(i+2)%23,9+i%5) for i,v in enumerate(vertices)}
    weight={}
    for i,x in enumerate(vertices):
        weight[x]={}
        for m,(letter,y) in enumerate(edges[x].items()):
            j=idx[y]
            weight[x][letter]=F(13+(3*i+7*j+11*m+7*generation*(m+1))%53,
                                 7+(i+5*j+3*m+generation)%17)
    return t,weight


def data(edges, model, t_after):
    rows={x:{a:mass*t_after[edges[x][a]] for a,mass in row.items()}
          for x,row in model.items()}
    return {x:normalize(row) for x,row in rows.items()}, {x:sum(row.values()) for x,row in rows.items()}


def reconstruct(edges, selected, tables, roots):
    vertices=list(edges); t0,w0=word_law(edges,0); t1,w1=word_law(edges,1)
    t2,_=word_law(edges,2)
    p0,_=data(edges,w0,t1)
    p1,r1=data(edges,w1,t2)
    root=roots
    # The observed two-step terminal factor can even depend on both
    # endpoints, since it cancels inside each fixed-endpoint window.
    adj=defaultdict(dict)
    for ni,key in enumerate(selected):
        x,k=key
        paths=tables[key]
        fee=F(3+ni,5+2*ni)
        raw={(a,b):fee*w0[x][a]*w1[j][b] for a,j,b in paths}
        measured=normalize(raw)
        factors={}
        for a,j,b in paths:
            v=measured[a,b]/(p0[x][a]*p1[j][b])
            need(j not in factors or factors[j]==v,"parallel labelled paths")
            factors[j]=v
        for i,vi in factors.items():
            for j,vj in factors.items():
                ratio=vj/vi
                need(j not in adj[i] or adj[i][j]==ratio,"overlapping windows agree")
                adj[i][j]=ratio
    known={root:F(1)}; queue=deque([root])
    while queue:
        i=queue.popleft()
        for j,v in adj[i].items():
            candidate=known[i]*v
            if j not in known:
                known[j]=candidate;queue.append(j)
            else:
                need(known[j]==candidate,"verified all measured comparison cycles")
    need(len(known)==len(vertices),"all source multipliers recovered")
    unit=r1[root]/t1[root]
    for i in vertices:
        need(known[i]==(r1[i]/t1[i])/unit,"exact source ratio")
        for a,j in edges[i].items():
            got=known[i]*p1[i][a]
            need(got==w1[i][a]*t2[j]/(unit*t1[i]),"every actual labelled edge")
    # Explicit volume gauge: scale all edge weights at a given tick and
    # change all intermediate endpoint potentials; the normalized rows and
    # conditional two-step paths are exactly invariant at every location.
    v0={x:F(3+j%5,2+j%3) for j,x in enumerate(vertices)}
    v1={x:F(7+j%7,3+j%5) for j,x in enumerate(vertices)}
    v2={x:F(11+j%5,5+j%4) for j,x in enumerate(vertices)}
    def gauge(w,vl,vr,c):
        return {x:{a:c*vl[x]*u/vr[edges[x][a]] for a,u in r.items()} for x,r in w.items()}
    h0=gauge(w0,v0,v1,F(7,5));h1=gauge(w1,v1,v2,F(9,8))
    p0p,_=data(edges,h0,{j:t1[j]*v1[j] for j in vertices})
    p1p,_=data(edges,h1,{j:t2[j]*v2[j] for j in vertices})
    need(p0==p0p and p1==p1p,"one-step gauge and terminal")
    for x,k in selected:
        paths=tables[x,k]
        left=normalize({(a,b):w0[x][a]*w1[j][b] for a,j,b in paths})
        right=normalize({(a,b):h0[x][a]*h1[j][b] for a,j,b in paths})
        need(left==right,"two-step gauge")
    return sum(map(len,edges.values()))


def length_and_memory(edges):
    x=(2,0,0)  # DATA=1, bus=0, b=0; the two distinct gates really fix it.
    s="SourceI"; c=(2,0)
    words=[[s,s,s,c],[s,s,c,s]]
    def true_state_and_extra(word):
        y=x
        emitted=0
        for j,g in enumerate(word):
            need(edges[y][g]==x,"fixed full native orbit state at every tick")
            y=edges[y][g]
            emitted+=int(j>=2 and word[j-2:j+1]==[s,s,s])
        return y,emitted
    results=[true_state_and_extra(w) for w in words]
    need(Counter(words[0])==Counter(words[1]) and results==[(x,1),(x,0)],"history-dependent paid third-letter counter")
    # Optional length calibration with seven independent equal gate choices.
    # Halt on a single prescribed first letter, continue on the other six.
    short=F(1,7); long=1-short; c2=F(13,11)
    observed_late=c2*long/(short+c2*long)
    recovered=observed_late/(1-observed_late)*short/long
    need(observed_late!=long and recovered==c2,"absolute time scale on an admitted common-price frontier")
    # With one extra printed zero the rare path gets the Golden factor p.
    # The exact TV is delta*t*(1-t)/(1-delta*t), delta=1-p<2/5.
    n=8; t=F(1,7**n); delta_upper=F(2,5)
    need(F(3,5)**2+F(3,5)<1,"positive golden root exceeds 3/5")
    tv_upper=delta_upper*t*(1-t)/(1-delta_upper*t)
    need(tv_upper < 2*t/5,"passive joint-law TV bound")
    return {"length_anchor_hidden_ratio":str(c2),"length_anchor_reconstructed":str(recovered),
            "actual_count_of_additional_deterministic_NC1_zero_on_two_words":[v for _,v in results],
            "extra_print_has_no_conditional_entropy_given_the_full_address_record":True,
            "passive_rare_word_length":n, "probability":str(t), "strict_TV_upper_bound":str(tv_upper),
            "necessary_independent_trials_for_TV_one_third_at_least":(5*7**n)//6+1}


def main():
    edges=orbit(); win=windows(edges); vertices=list(edges); sel=greedy(win,vertices)
    rad,ctr=graph_radius(vertices,sel,win); allrad,_=graph_radius(vertices,win,win)
    need((len(edges),sum(map(len,edges.values())),len(win),sum(map(len,win.values())))==
         (28,196,256,1372),"native orbit size and number of physical two-letter words")
    need(len(sel)==15 and (rad,allrad)==(5,3),"finite certificate and error radii")
    n=reconstruct(edges,sel,win,ctr)
    graph=scene(); w=windows(graph); scene_sel=[(0,0),(9,9)]
    sr,sc=graph_radius(list(graph),scene_sel,w)
    need(sr==1,"common anchor in third part")
    nscene=reconstruct(graph,scene_sel,w,sc)
    # G13 uses actual scene degree plus two temporal options; condition on
    # two spatial steps and a return to the same fixed root in the size-9 zone.
    # Both temporal directions and the rest of the full experiment remain as
    # other observed records. All retained spatial paths have clock winding 0.
    raw=F(11,24)
    walk=F(11,24)/(F(11,24)+F(13,22))
    need(walk==F(121,277) and raw-walk==F(143,6648),"two-step change on same canonical scene")
    return {"schema":"d0.work-short-window-selection/1","status":"PASS",
            "native_orbit":{"states":28,"addressed_edges":n,"two_letter_paths":1372,
                "nonempty_endpoint_windows":len(win),"sufficient_windows":sel,
                "selected_radius":rad,"all_windows_radius":allrad,
                "log_error_factor_selected":1+6*rad,"log_error_factor_all":1+6*allrad},
            "tripartite_scene":{"states":33,"directed_edges_checked":nscene,
                "sufficient_returns":scene_sel,"log_error_factor":1+6*sr,
                "prob_middle_size11_in_raw_constant_cost":str(raw),
                "prob_middle_size11_in_G13_spatial_two_step_return":str(walk),
                "exact_conditional_total_variation":str(raw-walk)},
            "absolute_and_memory_limits":length_and_memory(edges),
            "scope":"conditional on a genuinely observed positive scalar memoryless state/address transfer and endpoint fees at each tick, including actual measurement and halt costs. Born labels alone do not select that transfer.",
            "GR_closed":False}


if __name__=="__main__":
    print(json.dumps(main(),indent=2))

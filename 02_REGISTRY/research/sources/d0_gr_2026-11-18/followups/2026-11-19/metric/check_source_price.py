"""Replay the actual NPS14 parser and compare exact syntax lengths, not traversal fees."""
from hashlib import sha256
import importlib.util
from itertools import groupby, product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True


def need(test, message):
    if not test:
        raise ArithmeticError(message)


def load_control():
    here = Path(__file__).resolve().parent
    path = here.parents[3]/"d0_native_execution_domain_2026-10-24"/"native_execution.py"
    digest = sha256(path.read_bytes()).hexdigest()
    need(digest == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c",
         "pinned native operator/decoder")
    spec = importlib.util.spec_from_file_location("source_price_control",path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module,digest


def compact(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode("utf-8")


def flip_spaces(raw):
    count = len(raw)-len(raw.rstrip(b" "))
    return raw[:-1] if count%2 else raw+b" "


def run_encode(flat):
    # Bijection on the two *canonical* syntax domains, with unique maximal runs.
    obj = json.loads(flat)
    groups = groupby(obj["gates"])
    obj["gates"] = [[sum(1 for _ in members), instruction] for instruction,members in groups]
    return compact(obj)


def run_decode(coded):
    obj = json.loads(coded)
    flat = []
    previous = None
    for count,instruction in obj["gates"]:
        need(type(count)==int and count > 0 and instruction!=previous, "canonical positive run")
        flat.extend([instruction]*count)
        previous = instruction
    obj["gates"] = flat
    return compact(obj)


def main():
    ne,digest = load_control()
    e,b,r,t = 2,3,4,5
    bank = ne.Gate("CX",(b,e))
    reader = ne.Gate("CX",(e,r))
    spin = ne.Gate("SourceI",(e,0,1))
    tail = ne.Gate("CX",(r,t))
    word = (bank,reader,spin,spin,bank,tail,ne.Gate("G",(t,)),tail)

    def make(gates):
        return ne.Execution(6,(),(),gates,profile=ne.G_CX_SOURCE_I,source_port=e,
                            source_spin=(0,1),report_bits=(r,t))

    def decode(raw):
        return ne.execution_from_json(raw,max_qubits=6,max_expanded_stages=64)

    fixture = make(word)
    flat = ne.canonical_json(fixture).encode("utf-8")
    need(decode(flat)==fixture and compact(ne.execution_to_dict(fixture))==flat,
         "identical parameters to the all-column NPS14 witness")
    # All optional fields are non-default on this concrete fixture, so their
    # omission either fails membership or returns a different decoded object.
    omission = {}
    for key in ne.execution_to_dict(fixture):
        obj = ne.execution_to_dict(fixture)
        del obj[key]
        try:
            changed = decode(compact(obj))
        except ne.DomainError:
            changed = None
        need(changed!=fixture, "all NPS14 fields required for this very object")
        omission[key] = "rejected" if changed is None else "different execution"

    for k in range(8):
        raw = flat+k*b" "
        other = flip_spaces(raw)
        need(flip_spaces(other)==raw and raw!=other, "fixed-point-free format involution")
        need(decode(raw)==decode(other)==fixture, "same actual decoded stages and metadata")
    need(len(flip_spaces(flat))==len(flat)+1, "shortlex representative goes to longer synonym")
    body = decode(flip_spaces(flat))
    inv = ne.inventory(body,max_qubits=6,max_expanded_stages=8)
    need((inv.cx_count,inv.g_count,inv.source_i_count)==(5,1,2),"true paid NPS14 calls")
    # Exact basis action of the two permutations before any subsequent sign/writer.
    mats = [ne.gate_matrix(body,g,max_qubits=6,max_expanded_stages=8) for g in word[:2]]
    weights = [ne.P,ne.P**2]
    event = pointer = 0
    for E,B,R,T in product(range(2), repeat=4):
        w = weights[E]*weights[B]*weights[R]*weights[T]
        i = (E<<3)|(B<<2)|(R<<1)|T
        j = i ^ (B<<3)
        k = j ^ (((j>>3)&1)<<1)
        need(mats[0][j,i]==1 and mats[1][k,j]==1, "actual source-order permutation")
        event += w*((j>>3)&1)
        pointer += w*((k>>1)&1)
    field_zero = lambda z: ne.GOLDEN_FIELD.from_sympy(z)==ne.GOLDEN_FIELD.zero
    need(field_zero(event-2*ne.P**3) and field_zero(pointer-ne.P**2-2*ne.P**6),
         "original NPS15 Q and canonical pointer price")
    reader_obj = {"op":"CX","wires":[2,4]}
    literal = compact(reader_obj)
    # Actual H.1 padding slot type before the named G_r power. Its declared
    # stand-alone executions here test syntax, without claiming full H.1 admission.
    rows = []
    for n in (1,2,3,4,5,12):
        ex = make((reader,)*(2*n)+(ne.Gate("G",(r,)),))
        expanded = ne.canonical_json(ex).encode("utf-8")
        run = run_encode(expanded)
        restored = run_decode(run)
        need(restored==expanded and decode(restored)==ex, "all paid intermediate slots recovered")
        need(len(decode(restored).gates)==2*n+1, "the pair has not been cancelled")
        need(run_encode(restored)==run, "round-trip on canonical run descriptions")
        rows.append({"n_pairs":n,"flat_bytes":len(expanded),"run_description_bytes":len(run)})
    dflat=rows[2]["flat_bytes"]-rows[1]["flat_bytes"]
    drun=rows[2]["run_description_bytes"]-rows[1]["run_description_bytes"]
    need(dflat==2*(1+len(literal)) and drun==0, "different length increments for n=2 to 3")
    out = dict(status="PASS",native_owner_sha256=digest,actual_full_word="NPS14",
        six_wire_reader_descriptor=literal.decode(),reader_descriptor_bytes=len(literal),
        full_shortest_json_bytes=len(flat),longer_whitespace_synonym_bytes=len(flip_spaces(flat)),
        decoded_field_omission_checks=omission,native_instructions=8,native_square_columns=64,
        operated_pointer=dict(original_event="2p^3",original_report_one="p^2+2p^6",
                              added_mean_terminal_golden_units="2p^6"),
        physical_delta_scope="all tests factoring through decoded stages and fixed input; byte inspection can distinguish",
        padding_rows=rows,flat_increment_for_two_extra_CX=dflat,
        maximal_run_increment_for_two_extra_CX=drun,
        physical_traversal_price_identified=False)
    print(json.dumps(out,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()

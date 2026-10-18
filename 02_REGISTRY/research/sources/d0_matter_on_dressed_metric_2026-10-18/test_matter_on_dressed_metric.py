"""Replay the dressed-metric matter response and the Einstein-copy refusal."""

from check_matter_on_dressed_metric import StressRefusal, admit_stress, run


def require(condition, name):
    if condition is not True:
        raise RuntimeError(name)


def main():
    copied = [[1, 0], [0, -1]]
    try:
        admit_stress({"copy_einstein": True, "T": copied, "G": copied, "kind": "grade0_only"})
    except StressRefusal as refusal:
        require(str(refusal) == "stress_defined_as_einstein", "einstein copy message")
    else:
        raise RuntimeError("negative control did not raise")
    try:
        admit_stress({"kind": "grade0_only", "scalar_action_integral": "sqrt|g|(dpsi)^2"})
    except StressRefusal:
        pass
    else:
        raise RuntimeError("scalar action was admitted")
    try:
        admit_stress({"kind": "grade0_only", "measure": "chosen"})
    except StressRefusal:
        pass
    else:
        raise RuntimeError("measure was admitted")
    citation = admit_stress({"kind": "grade0_only", "stress_on_dressed_metric": False})
    require(citation["grade0_only"] is True, "grade0 citation")
    require(citation["scoped_nogo"] is True, "citation nogo")
    require(citation["stress_on_dressed_metric"] is False, "citation stress")
    require(citation["stress_defined_as_einstein"] is False, "citation einstein flag")
    require(citation["gr_derived"] is False, "citation gr")
    result = run()
    flags = result["flags"]
    require(result["status"] == "PASS", "status")
    require(flags["scoped_nogo"] is True, "scoped_nogo")
    require(flags["stress_on_dressed_metric"] is False, "stress_on_dressed_metric")
    require(flags["stress_defined_as_einstein"] is False, "stress_defined_as_einstein")
    require(flags["gr_derived"] is False, "gr_derived")
    require(flags["grade0_only"] is True, "grade0_only")
    require(flags["spin_in_owned_source"] is False, "spin absent")
    require(flags["scoped_nogo"] != flags["stress_on_dressed_metric"], "xor")
    require(result["chronology"]["joint_factor_jet"] == "0", "factor jet")
    require(result["chronology"]["owned_grade_scale"] == {"0": "16", "2": "1", "3": "1/4"}, "owned grade scale")
    require(result["chronology"]["density_scale"] == "2", "density scale")
    require(result["raw_defect"]["dressed_einstein"] == "0", "dressed einstein")
    require(result["raw_defect"]["raw_einstein_at_0"][0] == "-3/4", "raw residual")
    require(result["grade0_only"]["spin_arguments"] == 0, "grade0 spin count")
    require(result["check_count"] > 0, "checks ran")
    print("PASS %s %s" % (result["check_count"], result["verdict"]))


if __name__ == "__main__":
    main()

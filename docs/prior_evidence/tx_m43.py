"""TX-M43 — supplemental collector test (Addendum 7 to FAILFIRST V0.2, author 2026-10-24 11:49).
Pre-registered in RG6_M43_TEST_PROPOSAL.md (5ebb0fe3...22d6). S4d stays NOT_APPLICABLE; this is NOT S4d.
Target: private class `_Collector` of the verifier module given on the command line.
Expected values come only from spec §5.2 P-2 / P-3 (cap 32, FAILURES_TRUNCATED as entry 33, a deduped
emission does not count toward the cap) and the S4d expected cell. Never from candidate output.

Usage: python3 tx_m43.py <verifier.py> <expected_sha256> <out.json>
Any hash mismatch, import failure or missing attribute -> HARNESS_ERROR (never PASS).
"""
import hashlib
import importlib.util
import json
import sys

CAP = 32                      # spec §5.2 P-3
TRUNC = ("FAILURES_TRUNCATED", "failures")   # spec §5.2 P-3, §4.6


def pairs(n, start=0):
    return [("C", "d%02d" % i) for i in range(start, start + n)]


def main():
    path, want, out = sys.argv[1:4]
    res = {"target": path, "expected_sha256": want, "cases": {}, "row": "TX-M43"}
    try:
        b = open(path, "rb").read()
        got = hashlib.sha256(b).hexdigest()
        res["observed_sha256"] = got
        if got != want:
            raise RuntimeError("hash mismatch %s != %s" % (got, want))
        spec = importlib.util.spec_from_file_location("tx_m43_target", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        Col = getattr(mod, "_Collector")
    except Exception as e:  # harness error, never PASS
        res["outcome"] = "HARNESS_ERROR"
        res["error"] = "%s: %s" % (type(e).__name__, e)
        json.dump(res, open(out, "w"), indent=1)
        print(json.dumps(res, indent=1))
        return

    def run(name, stream, exp_entries, exp_trunc, exp_occ):
        c = Col()
        for p in stream:
            c.emit(*p)
        got = {"entries": [list(x) for x in c.entries], "truncated": c.truncated, "occurred": c.occurred}
        ok = (c.entries == exp_entries and c.truncated is exp_trunc and c.occurred == exp_occ)
        res["cases"][name] = {"outcome": "PASS" if ok else "FAIL",
                              "expected": {"n_entries": len(exp_entries), "truncated": exp_trunc,
                                           "occurred": exp_occ, "last": list(exp_entries[-1])},
                              "observed": {"n_entries": len(got["entries"]), "truncated": got["truncated"],
                                           "occurred": got["occurred"], "last": got["entries"][-1] if got["entries"] else None}}

    p32 = pairs(32)
    # a: 32 distinct + 2 repeats -> exactly 32 in first-occurrence order, no truncation (S4d expected cell)
    run("TX-M43-a", p32 + [p32[0], p32[17]], p32, False, 34)
    # b: 31 distinct, 1 repeat, 1 new -> 32 entries, no truncation (deduped emission does not count, P-3)
    p31 = pairs(31)
    run("TX-M43-b", p31 + [p31[5]] + pairs(1, 31), p31 + pairs(1, 31), False, 33)
    # c: 33 distinct -> 32 entries + FAILURES_TRUNCATED as entry 33 (P-3 control)
    run("TX-M43-c", pairs(33), p32 + [TRUNC], True, 33)
    # d: 2 identical -> 1 entry (P-2 control); occurred counts both
    run("TX-M43-d", [("C", "x"), ("C", "x")], [("C", "x")], False, 2)

    res["outcome"] = "PASS" if all(v["outcome"] == "PASS" for v in res["cases"].values()) else "FAIL"
    json.dump(res, open(out, "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()

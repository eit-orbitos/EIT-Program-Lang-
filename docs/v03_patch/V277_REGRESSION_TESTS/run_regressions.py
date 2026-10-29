"""Explicit synthetic-only round; no production oracle or gate approval implied.

Tasklet authoring status is NOT_RUN. External execution needs the author's
scoped synthetic-round authorization. No production owner root is invented.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import sys
import types
import unittest
import unicodedata


HISTORICAL_ONLY = frozenset({
    "test_m13_original_runtime_mutant_proposal_not_implemented",
    "test_m15_original_required_record_check_mutant_proposal_not_implemented",
})


def verify_trees(candidate, baseline):
    package = Path(__file__).resolve().parent.parent
    rows = json.loads((package / "BASELINE_INVENTORY.json").read_text())
    expected = {row["path"].removeprefix("successor_tree/"): row["sha256"] for row in rows}
    revised = dict(expected)
    delta = json.loads((package / "SOURCE_DELTA.json").read_text())["delta"]
    for row in delta:
        revised[row["path"].removeprefix("successor_tree/")] = row["candidate_sha256"]
    for label, root, pins in (("BASELINE", baseline, expected), ("CANDIDATE", candidate, revised)):
        actual = {f.relative_to(root).as_posix(): f for f in root.rglob("*") if f.is_file()}
        if set(actual) != set(pins):
            raise ValueError(label + " file inventory mismatch; no additions/deletions permitted")
        for name, pin in pins.items():
            if hashlib.sha256(actual[name].read_bytes()).hexdigest() != pin:
                raise ValueError(label + " SHA-256 mismatch: " + name)
        print(label + "_SOURCE_PINS_MATCH " + str(len(pins)), flush=True)


def leaf_tests(suite):
    for entry in suite:
        if isinstance(entry, unittest.TestSuite):
            yield from leaf_tests(entry)
        else:
            yield entry


class EvidenceResult(unittest.TextTestResult):
    def startTest(self, test):
        super().startTest(test)
        self._outcome = "ERROR"

    def addSuccess(self, test):
        self._outcome = "PASS"
        super().addSuccess(test)

    def addFailure(self, test, err):
        self._outcome = "FAIL"
        super().addFailure(test, err)

    def addError(self, test, err):
        self._outcome = "ERROR"
        super().addError(test, err)

    def addSkip(self, test, reason):
        self._outcome = "NOT_TESTED"
        super().addSkip(test, reason)

    def addSubTest(self, test, subtest, err):
        if err is not None:
            self._outcome = "FAIL"
        super().addSubTest(test, subtest, err)

    def stopTest(self, test):
        print("CASE_RESULT " + test.id() + " " + self._outcome, flush=True)
        super().stopTest(test)


def load_file(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError("explicit file loader unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module  # isolated test module namespace, not sys.path
    spec.loader.exec_module(module)
    return module


def load_candidate(root):
    source = root / "eit_program_lang"
    if not source.is_dir():
        raise ValueError("--candidate must name successor_tree, not a ZIP or parent")
    # A private package shell prevents executing the real __init__.py. Relative
    # runtime imports remain real files, not replacement integrity implementations.
    name = "_v277_regression_candidate"
    package = types.ModuleType(name)
    package.__path__ = [str(source)]
    package.__package__ = name
    sys.modules[name] = package
    core = load_file(name + ".s1_sp1_core", source / "s1_sp1_core.py")
    adapter = load_file(name + ".s1_sp1_adapter", source / "s1_sp1_adapter.py")
    builder = load_file(name + ".builder", source / "eit_v277_builder_candidate.py")
    runtime = load_file(name + ".frozen_translation_lookup", source / "frozen_translation_lookup.py")
    return types.SimpleNamespace(core=core, adapter=adapter, builder=builder,
                                 runtime=runtime, root=root)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", default=os.environ.get("V277_CANDIDATE_ROOT"))
    parser.add_argument("--baseline", help="immutable original successor_tree; optional baseline case otherwise skipped")
    parser.add_argument("--verbosity", type=int, default=2)
    parser.add_argument("--mode", required=True, choices=("synthetic-only",),
                        help="explicit scope; production/closure round is not supported")
    parser.add_argument("--execution-authorized", action="store_true",
                        help="acknowledge actual scoped author authorization for synthetic execution; not an IR04 approval")
    args = parser.parse_args(argv)
    # Fail CLOSED before any candidate/test import. No local-runtime fallback.
    if (platform.python_implementation() != "CPython"
            or sys.version_info[:3] != (3, 12, 15)
            or unicodedata.unidata_version != "15.0.0"):
        parser.error("BLOCKED: exact CPython 3.12.15 / Unicode 15.0.0 required; substitution prohibited")
    if not args.execution_authorized:
        parser.error("BLOCKED: scoped author synthetic-round authorization required; flag alone supplies none")
    if not args.candidate:
        parser.error("explicit --candidate or V277_CANDIDATE_ROOT required")
    if not args.baseline:
        parser.error("BLOCKED: immutable pinned Option-A baseline required for separate LIMITED empty-role case")
    print("MODE=SYNTHETIC_ONLY; PRODUCTION_ORACLE_APPROVAL=NOT_GRANTED; CLOSURE_ELIGIBLE=false", flush=True)
    print("ENVIRONMENT CPython=" + platform.python_version() + " Unicode=" + unicodedata.unidata_version, flush=True)
    candidate = Path(args.candidate).resolve(strict=True)
    baseline = Path(args.baseline).resolve(strict=True)
    if candidate == baseline:
        parser.error("BLOCKED: candidate and immutable baseline must be separate trees")
    try:
        verify_trees(candidate, baseline)
    except (OSError, ValueError, KeyError) as error:
        parser.error("BLOCKED_SOURCE_INTEGRITY: " + str(error))
    sys.dont_write_bytecode = True
    context = load_candidate(candidate)
    context.baseline = baseline
    if context.baseline is None:
        print("NOT_TESTED: pinned legacy baseline not supplied; full-suite claim prohibited", file=sys.stderr, flush=True)
    tests = load_file("_v277_authored_regressions", Path(__file__).with_name("test_s1_regressions.py"))
    tests.CONTEXT = context
    suite = unittest.defaultTestLoader.loadTestsFromModule(tests)
    selected = []
    for test in leaf_tests(suite):
        if test._testMethodName in HISTORICAL_ONLY:
            print("OUT_OF_SCOPE NOT_TESTED " + test.id() + " original historical mutant obligation remains OPEN", flush=True)
        else:
            selected.append(test)
    result = unittest.TextTestRunner(verbosity=args.verbosity, resultclass=EvidenceResult).run(unittest.TestSuite(selected))
    # Skips are incomplete evidence, not a full-suite success. Original mutant
    # proposals intentionally remain skipped until separately implemented.
    if not result.wasSuccessful():
        return 1
    if result.skipped or context.baseline is None:
        print("INCOMPLETE / NOT_TESTED: skipped obligations remain; no full-suite or gate claim", file=sys.stderr)
        return 3
    print("SYNTHETIC_ROUND_COMPLETE; HISTORICAL_MUTANTS_NOT_TESTED; F01_UNVERIFIED; NO_GATE_CLOSURE", flush=True)
    # Zero means selected synthetic round only; historical obligations stay open.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

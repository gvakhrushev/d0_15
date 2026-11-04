"""Small producer regressions for informative discovery and raw-query matching."""

import contextlib
import io
import json
import os
import pathlib
import random
import re
import subprocess
import tempfile
import unittest
from unittest import mock

try:
    from tools import proof_architecture as proof
except ModuleNotFoundError:
    import proof_architecture as proof


QUERY = (
    "native full source amberquartz violetcobalt indigomarble "
    "ochretopaz silvergranite bluegarnet"
)


class ProofSearchTermTests(unittest.TestCase):
    def make_research(self, root):
        research = root / "02_REGISTRY" / "research"
        research.mkdir(parents=True)
        return research

    def test_broad_terms_on_other_lines_still_match_raw_query(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            research = self.make_research(root)
            owner = research / "owner.md"
            owner.write_text("amberquartz\nnative full\n", encoding="utf-8")
            hits = proof.full_text_search_many(root, [QUERY, QUERY], limit=12)

        for result in hits:
            self.assertEqual(len(result), 1)
            hit = result[0]
            self.assertEqual(hit["query_terms"], len(proof._query_terms(QUERY)))
            self.assertEqual(hit["matched_term_names"], ["native", "full", "amberquartz"])
            self.assertEqual(hit["matched_terms"], 3)
            self.assertTrue(hit["direct_content"])
            self.assertEqual({row["line"] for row in hit["evidence_lines"]}, {1, 2})

    def test_raw_threshold_is_not_lowered_to_prefilter_term_count(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            research = self.make_research(root)
            (research / "owner.md").write_text("amberquartz violetcobalt\n", encoding="utf-8")
            hits = proof.full_text_search(root, QUERY, limit=12)
        # Nine raw groups require three hits; six informative groups alone
        # would require only two. The prefilter must not change that threshold.
        self.assertEqual(len(proof._query_terms(QUERY)), 9)
        self.assertEqual(hits, [])

    def test_fullstep_is_not_treated_as_the_broad_word_full(self):
        query = "fullStep native source amberquartz violetcobalt"
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            research = self.make_research(root)
            (research / "owner.md").write_text("fullStep\nnative\n", encoding="utf-8")
            hits = proof.full_text_search(root, query, limit=12)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["matched_term_names"], ["fullstep", "native"])
        self.assertEqual(hits[0]["query_terms"], 5)
        self.assertTrue(hits[0]["direct_content"])

    def test_unrelated_broad_only_corpus_document_and_title_are_not_discovered(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            research = self.make_research(root)
            (research / "owner.md").write_text("native full source\n", encoding="utf-8")
            (research / "native_full_source.md").write_text("Unrelated prose.\n", encoding="utf-8")
            hits = proof.full_text_search(root, QUERY, limit=12)
        self.assertEqual(hits, [])

    def test_broad_only_query_keeps_exhaustive_fallback(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            research = self.make_research(root)
            (research / "owner.md").write_text("native full source\n", encoding="utf-8")
            hits = proof.full_text_search(root, "native full source", limit=12)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["matched_term_names"], ["native", "full", "source"])
        self.assertEqual(hits[0]["query_terms"], 3)

    def test_exact_pin_uses_raw_terms_and_still_rejects_wrong_blob(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            research = self.make_research(root)
            source = research / "owner.md"
            source_rel = source.relative_to(root).as_posix()
            source.write_text("amberquartz\nnative full\n", encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "add", source_rel], cwd=root, check=True)
            subprocess.run(["git", "-c", "user.name=Proof Test", "-c",
                            "user.email=test@example.invalid", "commit", "-q", "-m", "fixture"],
                           cwd=root, check=True)
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root,
                                             text=True).strip()
            blob = subprocess.check_output(["git", "rev-parse", f"HEAD:{source_rel}"],
                                           cwd=root, text=True).strip()
            source.unlink()
            locator = research / "locator.md"
            for label, cited_blob in (("exact", blob), ("wrong_blob", "f" * 40)):
                with self.subTest(label=label):
                    locator.write_text(
                        f"{QUERY}: {source_rel}; commit {commit}; blob {cited_blob}.\n",
                        encoding="utf-8",
                    )
                    hits = proof.full_text_search(root, QUERY, limit=12)
                    owner_hits = [hit for hit in hits if hit["source"] == source_rel]
                    self.assertTrue(owner_hits)
                    if label == "exact":
                        hit = next(hit for hit in owner_hits if hit.get("pin_status") == "verified")
                        self.assertTrue(hit["direct_content"])
                        self.assertEqual(hit["source_commit"], commit)
                        self.assertEqual(hit["source_blob"], blob)
                        self.assertEqual(hit["query_terms"], 9)
                        self.assertEqual(hit["matched_term_names"], ["native", "full", "amberquartz"])
                    else:
                        self.assertFalse(any(hit["direct_content"] for hit in owner_hits))
                        self.assertFalse(any(hit.get("pin_status") == "verified" for hit in owner_hits))


class ProofSearchRegexEquivalenceTests(unittest.TestCase):
    @staticmethod
    def legacy_pattern(terms):
        """The named-group producer before the literal-prefix optimization."""
        alternatives = []
        for index, (_, variants) in enumerate(terms):
            values = sorted(set(variants), key=lambda value: (-len(value), value))
            alternatives.append(
                f"(?P<t{index}>" + "|".join(re.escape(value) for value in values) + ")"
            )
        return re.compile("|".join(alternatives)) if alternatives else re.compile(r"(?!)")

    @staticmethod
    def legacy_names(text, pattern, terms):
        group_names = {f"t{index}": name for index, (name, _) in enumerate(terms)}
        return {group_names[match.lastgroup] for match in pattern.finditer(text)
                if match.lastgroup in group_names}

    def assert_legacy_matches(self, text, terms):
        legacy = self.legacy_pattern(terms)
        actual = proof._term_pattern(terms)
        self.assertEqual(proof._matched_term_names(text, actual, terms),
                         self.legacy_names(text, legacy, terms))
        # Names alone would miss a change to regex overlap or consumption order.
        self.assertEqual([(match.span(), match.group(0)) for match in actual.finditer(text)],
                         [(match.span(), match.group(0)) for match in legacy.finditer(text)])

    def test_prefix_priority_unicode_literals_and_empty_terms_match_legacy(self):
        fixtures = [
            ("abab aba ab", [("first", ("ab",)), ("later", ("aba", "abab"))]),
            ("abab aba ab", [("first", ("ab", "abab")), ("later", ("aba",))]),
            ("ab a ab", [("first", ("ab", "a")), ("second", ("ab",))]),
            ("a+b a.b a*b (a)", [("punctuation", ("a+b", "a.b", "(a)")),
                                  ("other", ("a*b",))]),
            (proof._fold("ЁЖ ёж еЖ Straße STRASSE σ Σ ς fullStep"),
             [("russian", ("еж",)), ("german", ("strasse",)),
              ("greek", ("σ",)), ("full", ("fullstep",))]),
            ("abc", []),
            ("abc", [("empty", ())]),
            ("ab", [("empty", ("",)), ("a", ("a",))]),
            ("ab", [("a", ("a",)), ("empty", ("",))]),
        ]
        for text, terms in fixtures:
            with self.subTest(text=text, terms=terms):
                self.assert_legacy_matches(text, terms)

        # An overlapping later alternative must not become an additional hit.
        terms = [("earlier_prefix", ("ab",)), ("later_longer", ("abab",))]
        self.assertEqual(proof._matched_term_names("abab", proof._term_pattern(terms), terms),
                         {"earlier_prefix"})

    def test_deterministic_overlapping_variants_match_legacy(self):
        rng = random.Random(20261104)
        variants = ["a", "ab", "aba", "b", "ba", "еж", "ж", "σ", "strasse",
                    "a+b", ".", "", "full", "fullstep"]
        for case in range(600):
            terms = [(f"term{index}", tuple(rng.choices(variants, k=rng.randrange(5))))
                     for index in range(rng.randrange(8))]
            text = " ".join(rng.choices(variants, k=rng.randrange(20)))
            with self.subTest(case=case):
                self.assert_legacy_matches(text, terms)

    def test_same_compiled_literals_keep_distinct_semantic_owners(self):
        first = [("first_owner", ("shared", "sharedprefix"))]
        second = [("second_owner", ("shared", "sharedprefix"))]
        shared_pattern = proof._term_pattern(first)
        self.assertEqual(shared_pattern.pattern, proof._term_pattern(second).pattern)
        # Reuse the same pattern object across both term lists, then revisit the
        # first owner: a cache keyed solely by regex cannot retain both meanings.
        for terms, owner in ((first, "first_owner"), (second, "second_owner"),
                             (first, "first_owner")):
            self.assertEqual(proof._matched_term_names("sharedprefix shared", shared_pattern, terms),
                             {owner})

    def test_complete_ranked_line_evidence_matches_legacy(self):
        content = "\n".join([
            "No heading yet: fullStep native",
            "# First ЁЖ source",
            "  ab abab a+b Straße  ",
            "A long source line: " + "x" * (proof.MAX_SNIPPET + 20) + " native fullStep",
            "## Second σ source",
            "unrelated prose",
            *[f"  native fullStep source {index:02d}  " for index in range(30)],
        ])
        term_lists = [
            [("prefix", ("ab",)), ("later", ("abab",)), ("native", ("native",)),
             ("fullstep", ("fullstep",)), ("source", ("source",)),
             ("unicode", ("еж", "strasse", "σ")), ("punctuation", ("a+b",))],
            proof._query_terms("native fullStep source точное восстановление тетрады"),
            [],
            [("empty", ()), ("native", ("native",))],
        ]
        for terms in term_lists:
            with self.subTest(terms=terms):
                actual = proof._line_evidence(content, terms, proof._term_pattern(terms))
                with mock.patch.object(proof, "_matched_term_names", self.legacy_names):
                    expected = proof._line_evidence(content, terms, self.legacy_pattern(terms))
                # Compare every field and the full sequence, including top-20
                # truncation, headings, term order, line ties and snippet cuts.
                self.assertEqual(actual, expected)
                if terms:
                    self.assertEqual(len(actual), 20)

    def test_progress_is_optional_stderr_json_and_never_stdout(self):
        for setting in (None, "0", "1"):
            stdout, stderr = io.StringIO(), io.StringIO()
            with self.subTest(setting=setting), mock.patch.dict(os.environ):
                if setting is None:
                    os.environ.pop("D0_PROOF_SEARCH_PROGRESS", None)
                else:
                    os.environ["D0_PROOF_SEARCH_PROGRESS"] = setting
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    proof._search_progress("fixture", query_index=2, candidate_count=7)
            self.assertEqual(stdout.getvalue(), "")
            if setting == "1":
                self.assertEqual(json.loads(stderr.getvalue()), {
                    "proof_search_progress": "fixture", "query_index": 2, "candidate_count": 7,
                })
                self.assertEqual(len(stderr.getvalue().splitlines()), 1)
            else:
                self.assertEqual(stderr.getvalue(), "")


if __name__ == "__main__":
    unittest.main()

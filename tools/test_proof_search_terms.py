"""Small producer regressions for informative discovery and raw-query matching."""

import pathlib
import subprocess
import tempfile
import unittest

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


if __name__ == "__main__":
    unittest.main()

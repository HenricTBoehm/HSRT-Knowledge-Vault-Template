import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_vault import validate_concept, validate_decisions, validate_okf

class TestValidation(unittest.TestCase):
    def concept(self, directory, text):
        path = Path(directory) / "concept.md"
        path.write_text(text, encoding="utf-8")
        return validate_concept(path)

    def test_okf_without_concepts(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / "60-Knowledge-Pilot" / "OKF"
            base.mkdir(parents=True)
            (base / "index.md").write_text('---\nokf_version: "0.2"\n---\n\n# Empty\n', encoding="utf-8")
            self.assertEqual([], validate_okf(Path(directory)))

    def test_missing_type_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = self.concept(directory, "---\nstatus: draft\n---\n\n# Claim\n")
            self.assertTrue(any("type" in error for error in errors))

    def test_source_without_resource_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = self.concept(directory, "---\ntype: Concept\nsources:\n  - id: s1\n---\n")
            self.assertTrue(any("resource" in error for error in errors))

    def test_duplicate_yaml_keys_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = self.concept(directory, "---\ntype: Concept\ntype: Metric\n---\n")
            self.assertTrue(any("Duplicate" in error for error in errors))

    def test_generated_actor_convention_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = self.concept(directory, "---\ntype: Concept\ngenerated: {by: placeholder}\n---\n")
            self.assertTrue(any("actor convention" in error for error in errors))

    def test_verified_without_offset_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = self.concept(directory, "---\ntype: Concept\nverified: {by: human:test, at: \"2026-10-31T11:30:00\"}\n---\n")
            self.assertTrue(any("verified" in error for error in errors))

    def test_stale_after_without_offset_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = self.concept(directory, "---\ntype: Concept\nstale_after: 2026-11-01\n---\n")
            self.assertTrue(any("stale_after" in error for error in errors))

    def test_source_signals_and_usage_window_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = self.concept(directory, "---\ntype: Concept\nsources:\n  - id: source-1\n    resource: reference.md\n    author: process:importer\n    usage_count: 3\n    last_modified: \"2026-10-01T10:00:00Z\"\nusage_window:\n  from: \"2026-10-01T00:00:00Z\"\n  to: \"2026-10-31T00:00:00Z\"\n---\n\nClaim.[^source-1]\n\n[^source-1]: Source\n")
            self.assertEqual([], errors)

    def test_reversed_usage_window_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = self.concept(directory, "---\ntype: Concept\nusage_window:\n  from: \"2026-11-01T00:00:00Z\"\n  to: \"2026-10-01T00:00:00Z\"\n---\n")
            self.assertTrue(any("must not be after" in error for error in errors))

    def test_valid_inline_attested_computation(self):
        with tempfile.TemporaryDirectory() as directory:
            fence = chr(96) * 3
            errors = self.concept(directory, "---\ntype: Attested Computation\nruntime: python\nparameters:\n  - {name: value, type: integer, required: true}\nexecutor:\n  resource: references/run.md\n  receipt: [result]\nattester:\n  resource: references/check.py\n---\n\n# Computation\n\n" + fence + "python\nprint(value)\n" + fence + "\n")
            self.assertEqual([], errors)

    def test_valid_tilde_fenced_attested_computation(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = self.concept(directory, "---\ntype: Attested Computation\nruntime: python\n---\n\n# Computation\n\n~~~python\nprint(1)\n~~~\n")
            self.assertEqual([], errors)

    def test_attested_computation_requires_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            fence = chr(96) * 3
            errors = self.concept(directory, "---\ntype: Attested Computation\n---\n\n# Computation\n\n" + fence + "sql\nselect 1\n" + fence + "\n")
            self.assertTrue(any("runtime" in error for error in errors))

    def test_external_and_inline_computation_conflict(self):
        with tempfile.TemporaryDirectory() as directory:
            fence = chr(96) * 3
            errors = self.concept(directory, "---\ntype: Attested Computation\nruntime: python\ncomputation: references/code.py\n---\n\n# Computation\n\n" + fence + "python\nprint(1)\n" + fence + "\n")
            self.assertTrue(any("mutually exclusive" in error for error in errors))

    def test_nested_index_frontmatter_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / "60-Knowledge-Pilot" / "OKF"
            nested = base / "nested"
            nested.mkdir(parents=True)
            (base / "index.md").write_text('---\nokf_version: "0.2"\n---\n\n# Root\n', encoding="utf-8")
            (nested / "index.md").write_text("---\ntype: Index\n---\n\n# Nested\n", encoding="utf-8")
            self.assertTrue(any("frontmatter" in error for error in validate_okf(Path(directory))))

    def test_log_dates_must_be_newest_first(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / "60-Knowledge-Pilot" / "OKF"
            base.mkdir(parents=True)
            (base / "index.md").write_text('---\nokf_version: "0.2"\n---\n\n# Root\n', encoding="utf-8")
            (base / "log.md").write_text("# Log\n\n## 2026-01-01\n* Old\n\n## 2026-02-01\n* New\n", encoding="utf-8")
            self.assertTrue(any("newest first" in error for error in validate_okf(Path(directory))))

    def test_admission_requires_human_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / "60-Knowledge-Pilot" / "DECISIONS"
            folder.mkdir(parents=True)
            (folder / "claim.md").write_text("---\ntype: admission-record\ndisposition: ADMIT_TO_WIKI\nreviewer: null\nreviewed_at: null\nsource_ids: []\nauthorized_effect: none\n---\n", encoding="utf-8")
            self.assertGreaterEqual(len(validate_decisions(Path(directory))), 4)

    def test_negative_hold_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / "60-Knowledge-Pilot" / "DECISIONS"
            folder.mkdir(parents=True)
            (folder / "pending.md").write_text("---\ntype: admission-record\ndisposition: HOLD\nreviewer: null\nreviewed_at: null\n---\n", encoding="utf-8")
            self.assertEqual([], validate_decisions(Path(directory)))

if __name__ == "__main__":
    unittest.main()

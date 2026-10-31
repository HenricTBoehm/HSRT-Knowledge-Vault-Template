import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from validate_vault import validate_concept,validate_okf,validate_decisions

class TestValidation(unittest.TestCase):
    def test_okf_without_concepts(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d)/'60-Knowledge-Pilot'/'OKF';base.mkdir(parents=True)
            (base/'index.md').write_text('---\nokf_version: "0.2"\n---\n\n# Empty\n')
            self.assertEqual([],validate_okf(Path(d)))
    def test_missing_type_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.md';p.write_text('---\nstatus: draft\n---\n\n# Claim\n')
            self.assertTrue(any('type' in x for x in validate_concept(p)))
    def test_source_without_resource_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.md';p.write_text('---\ntype: Concept\nsources:\n  - id: s1\n---\n')
            self.assertTrue(any('resource' in x for x in validate_concept(p)))
    def test_duplicate_yaml_keys_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.md';p.write_text('---\ntype: Concept\ntype: Metric\n---\n')
            self.assertTrue(any('Duplicate' in x for x in validate_concept(p)))
    def test_verified_without_offset_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.md';p.write_text('---\ntype: Concept\nverified: {by: human:test, at: "2026-10-31T11:30:00"}\n---\n')
            self.assertTrue(any('verified' in x for x in validate_concept(p)))
    def test_admission_requires_human_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d)/'60-Knowledge-Pilot'/'DECISIONS';folder.mkdir(parents=True)
            (folder/'claim.md').write_text('---\ntype: admission-record\ndisposition: ADMIT_TO_WIKI\nreviewer: null\nreviewed_at: null\nsource_ids: []\nauthorized_effect: none\n---\n')
            self.assertTrue(len(validate_decisions(Path(d)))>=4)
    def test_negative_hold_allowed(self):
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d)/'60-Knowledge-Pilot'/'DECISIONS';folder.mkdir(parents=True)
            (folder/'pending.md').write_text('---\ntype: admission-record\ndisposition: HOLD\nreviewer: null\nreviewed_at: null\n---\n')
            self.assertEqual([],validate_decisions(Path(d)))

if __name__=='__main__':unittest.main()

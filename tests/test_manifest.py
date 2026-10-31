import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_manifest import validate_manifest

class TestManifest(unittest.TestCase):
    def write_manifest(self, root, files):
        (root / "template-manifest.json").write_text(
            json.dumps({
                "manifest_excludes": ["template-manifest.json"],
                "files": files,
            }),
            encoding="utf-8",
        )

    def test_exact_manifest_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("blank", encoding="utf-8")
            self.write_manifest(root, ["README.md"])
            self.assertEqual([], validate_manifest(root))

    def test_unlisted_file_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("blank", encoding="utf-8")
            (root / "unexpected.md").write_text("unexpected", encoding="utf-8")
            self.write_manifest(root, ["README.md"])
            self.assertTrue(any("unlisted" in item for item in validate_manifest(root)))

    def test_missing_listed_file_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_manifest(root, ["missing.md"])
            self.assertTrue(any("does not exist" in item for item in validate_manifest(root)))

    def test_duplicate_entry_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("blank", encoding="utf-8")
            self.write_manifest(root, ["README.md", "README.md"])
            self.assertTrue(any("duplicates" in item for item in validate_manifest(root)))

    def test_generated_cache_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("blank", encoding="utf-8")
            cache = root / "scripts" / "__pycache__"
            cache.mkdir(parents=True)
            (cache / "module.pyc").write_bytes(b"generated")
            self.write_manifest(root, ["README.md"])
            self.assertEqual([], validate_manifest(root))

if __name__ == "__main__":
    unittest.main()

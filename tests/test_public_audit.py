import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_public import scan

class TestPublicAudit(unittest.TestCase):
    def test_empty_template_safe(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "README.md").write_text("No source records.\n", encoding="utf-8")
            (Path(directory) / "LICENSE").write_text("Generic license.\n", encoding="utf-8")
            self.assertEqual([], scan(Path(directory)))

    def test_email_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "README.md").write_text("user" + "@" + "example.invalid", encoding="utf-8")
            self.assertTrue(any("Email" in item for item in scan(Path(directory))))

    def test_private_drive_pointer_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "README.md").write_text("https://" + "drive." + "google.com/file/d/FAKE/view", encoding="utf-8")
            self.assertTrue(any("Drive" in item for item in scan(Path(directory))))

    def test_pdf_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "paper.pdf").write_bytes(b"%PDF-1.7")
            self.assertTrue(any("unapproved file type" in item for item in scan(Path(directory))))

    def test_docx_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "notes.docx").write_bytes(b"PK")
            self.assertTrue(any("unapproved file type" in item for item in scan(Path(directory))))

    def test_zip_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "archive.zip").write_bytes(b"PK")
            self.assertTrue(any("unapproved file type" in item for item in scan(Path(directory))))

    def test_image_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "image.png").write_bytes(b"\x89PNG")
            self.assertTrue(any("unapproved file type" in item for item in scan(Path(directory))))

    def test_unknown_extensionless_file_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "research-data").write_text("unknown", encoding="utf-8")
            self.assertTrue(any("unapproved file type" in item for item in scan(Path(directory))))

    def test_non_utf8_allowed_extension_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "note.md").write_bytes(b"\xff\xfe")
            self.assertTrue(any("non-UTF8" in item for item in scan(Path(directory))))

    def test_generated_python_cache_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "scripts" / "__pycache__"
            cache.mkdir(parents=True)
            (cache / "module.cpython-312.pyc").write_bytes(b"generated")
            self.assertEqual([], scan(Path(directory)))


if __name__ == "__main__":
    unittest.main()

import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_public import scan

class TestPublicAudit(unittest.TestCase):
    def test_empty_template_safe(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'README.md').write_text('No source records.\n')
            self.assertEqual([],scan(Path(d)))
    def test_email_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            # Construct test string so this source contains no real email address.
            (Path(d)/'README.md').write_text('user'+'@'+'example.invalid')
            self.assertTrue(any('Email' in x for x in scan(Path(d))))
    def test_private_drive_pointer_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'README.md').write_text('https://'+'drive.'+'google.com/file/d/FAKE/view')
            self.assertTrue(any('Drive' in x for x in scan(Path(d))))

if __name__=='__main__': unittest.main()

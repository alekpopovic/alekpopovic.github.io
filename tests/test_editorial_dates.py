import contextlib
import datetime as dt
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('editorial_check', ROOT / 'scripts/check-content.py')
editorial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editorial)
Datetime = dt.datetime


class BeforeUTCMidnight(Datetime):
    @classmethod
    def now(cls, tz=None):
        return Datetime.fromisoformat('2026-10-12T23:30:00+00:00').astimezone(tz)


class EditorialDatesTests(unittest.TestCase):
    def check_date(self, date):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '_posts').mkdir()
            (root / '_data').mkdir()
            (root / '_config.yml').write_text('timezone: Europe/Belgrade\n')
            (root / '_data/projects.json').write_text('[]')
            (root / '_posts/guide.md').write_text(f'---\nsection: ai\nverified_at: {date}\nsources: []\n---\nA reviewed guide.\n')
            with patch.object(editorial, 'ROOT', root), patch.object(editorial.dt, 'datetime', BeforeUTCMidnight), patch('sys.argv', ['check-content.py']), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                editorial.main()
            return (root / 'reports/content-review.md').read_text()

    def test_current_belgrade_day_is_not_future_on_a_utc_runner(self):
        report = self.check_date('2026-10-13')
        self.assertIn('Checked 2026-10-13', report)
        self.assertIn('(0 days old)', report)

    def test_next_belgrade_day_is_still_rejected(self):
        with self.assertRaises(SystemExit) as error:
            self.check_date('2026-10-14')
        self.assertEqual(error.exception.code, 1)


if __name__ == '__main__':
    unittest.main()

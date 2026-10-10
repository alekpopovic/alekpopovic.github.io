import json
import tempfile
import unittest
from pathlib import Path

from normalize_logs import normalize
from render_nginx_config import render


class NormalizationTests(unittest.TestCase):
    def event(self):
        return {"schema_version":1,"request_id":"a"*32,"event_time":"2026-10-10T00:00:00+02:00",
                "site_id":"site-demo","client_ip":"198.51.100.23","method":"GET","path":"/a\"b",
                "status":"404","request_time_seconds":"0.002","bytes_sent":"64","enforcement":"allow"}
    def test_numeric_units_and_escaped_path(self):
        event=normalize(json.dumps(self.event()))
        self.assertEqual(event['request_time_ms'],2)
        self.assertEqual(event['path'],'/a"b')
        self.assertEqual(event['status'],404)
        self.assertEqual(event['event_time'],1791583200)
    def test_missing_timezone_rejected(self):
        e=self.event();e['event_time']='2026-10-10T00:00:00'
        with self.assertRaises(ValueError): normalize(json.dumps(e))
    def test_query_rejected(self):
        e=self.event();e['path']='/login?token=disposable'
        with self.assertRaises(ValueError):normalize(json.dumps(e))
    def test_render_paths_and_listener_match(self):
        with tempfile.TemporaryDirectory() as root:
            unix=render(root)
            tcp=render(root,tcp=True)
            self.assertIn(str(Path(root)/'auth.sock'),unix)
            self.assertIn('http://127.0.0.1:9101/v1/check',tcp)
            self.assertIn('listen 127.0.0.1:8080',tcp)
            self.assertIn('proxy_pass_request_headers off',tcp)
            self.assertNotIn('return 200',tcp)


if __name__=='__main__':unittest.main()

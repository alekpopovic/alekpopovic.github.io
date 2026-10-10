# SPDX-License-Identifier: MIT
import copy
import unittest
from audit_chain import build, verify, canonical

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.events = [{"action": "created", "id": 1}, {"action": "ended", "id": 1}]
        self.rows, self.head = build(self.events)
    def test_valid(self): self.assertTrue(verify(self.rows, self.head))
    def test_mutation(self):
        rows=copy.deepcopy(self.rows);rows[0]["event"]["id"]=2
        self.assertFalse(verify(rows,self.head))
    def test_truncation(self): self.assertFalse(verify(self.rows[:-1],self.head))
    def test_reorder(self): self.assertFalse(verify(list(reversed(self.rows)),self.head))
    def test_insertion(self): self.assertFalse(verify(self.rows+[self.rows[-1]],self.head))
    def test_external_checkpoint(self):
        altered=[{"action":"other","id":1},self.events[1]]
        rewritten,new_head=build(altered)
        self.assertTrue(verify(rewritten,new_head))
        self.assertFalse(verify(rewritten,self.head))
    def test_detached_input(self):
        self.events[0]["id"]=100
        self.assertTrue(verify(self.rows,self.head))
    def test_empty(self):
        rows,head=build([]);self.assertTrue(verify(rows,head))
    def test_restricted_json(self):
        with self.assertRaises(ValueError): canonical({"a":float("nan")})
        with self.assertRaises(ValueError): canonical({1:"key"})
    def test_canonical_order(self):
        self.assertEqual(canonical({"a":1,"b":2}),canonical({"b":2,"a":1}))
if __name__=="__main__": unittest.main()

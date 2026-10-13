import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from observe_database_recovery import validate_recovery_names
class RecoveryTargets(unittest.TestCase):
 def test_fresh_distinct_lab_names(self):self.assertTrue(validate_recovery_names('inside_orch_lab_source_test','inside_orch_lab_target_test'))
 def test_equal_names_rejected(self):
  with self.assertRaises(ValueError):validate_recovery_names('inside_orch_lab_same_test','inside_orch_lab_same_test')
 def test_empty_target_rejected(self):
  with self.assertRaises(ValueError):validate_recovery_names('inside_orch_lab_source_test','')
 def test_external_names_rejected(self):
  with self.assertRaises(ValueError):validate_recovery_names('inside_orch_lab_source_test','production')
if __name__=='__main__':unittest.main()

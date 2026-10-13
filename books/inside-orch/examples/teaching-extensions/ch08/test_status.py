#!/usr/bin/env python3
"""Exercise semantic failure boundaries without inventing real host observations."""
import importlib.util,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('atlas_status',Path(__file__).with_name('atlas_status.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class StatusContract(unittest.TestCase):
 def service(self,replicas=1):return dict(id='s1',spec=dict(name='atlas-api',replicas=replicas),deployment_version=2,status='active')
 def task(self,id='t1',version=2,actual='healthy',desired='running'):return dict(id=id,service_id='s1',version=version,actual_status=actual,desired_status=desired)
 def test_current_available(self):self.assertTrue(module.evaluate(self.service(),[self.task()])[0])
 def test_old_healthy_does_not_mask_current_assigned(self):self.assertFalse(module.evaluate(self.service(),[self.task('old',1),self.task('new',2,'assigned')])[0])
 def test_cleanup_history_excluded(self):self.assertTrue(module.evaluate(self.service(),[self.task(),self.task('old',1,'removed','removed')])[0])
 def test_zero_replicas(self):self.assertTrue(module.evaluate(self.service(0),[])[0])
 def test_duplicate_task_cannot_inflate_count(self):
  with self.assertRaises(ValueError):module.evaluate(self.service(2),[self.task(),self.task()])
 def test_missing_contract_fields(self):
  with self.assertRaises(ValueError):module.evaluate(self.service(),[{}])
 def test_wrong_service(self):
  task=self.task();task['service_id']='other'
  with self.assertRaises(ValueError):module.evaluate(self.service(),[task])
 def test_bool_is_not_replica_integer(self):
  with self.assertRaises(ValueError):module.evaluate(self.service(True),[])
if __name__=='__main__':unittest.main(verbosity=2)

import importlib.util,unittest,copy
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'scripts/run_database_tests.py';s=importlib.util.spec_from_file_location('guard',p);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
class IsolationGuardTests(unittest.TestCase):
 def setUp(self):
  self.url='postgres://lab:disposable@127.0.0.1:15432/inside_orch_lab_fixture_test'
  self.container={'Config':{'Labels':{'inside-orch.lab':'true','inside-orch.run':'fixture'},'Env':['POSTGRES_DB=inside_orch_lab_fixture_test']},'State':{'Running':True},'NetworkSettings':{'Ports':{'5432/tcp':[{'HostIp':'127.0.0.1','HostPort':'15432'}]}}}
 def test_accepts_exact_owned_loopback(self):self.assertEqual(g.validate_target(self.url,self.container),'inside_orch_lab_fixture_test')
 def test_rejects_remote(self):
  with self.assertRaises(ValueError):g.validate_target(self.url.replace('127.0.0.1','example.com'),self.container)
 def test_rejects_real_database(self):
  with self.assertRaises(ValueError):g.validate_target(self.url.replace('inside_orch_lab_fixture_test','production'),self.container)
 def test_rejects_missing_ownership(self):
  self.container['Config']['Labels']={}
  with self.assertRaises(ValueError):g.validate_target(self.url,self.container)
 def test_rejects_wrong_port(self):
  with self.assertRaises(ValueError):g.validate_target(self.url.replace('15432','25432'),self.container)
 def test_rejects_wildcard_binding(self):
  self.container['NetworkSettings']['Ports']['5432/tcp'][0]['HostIp']='0.0.0.0'
  with self.assertRaises(ValueError):g.validate_target(self.url,self.container)
 def test_rejects_database_mismatch(self):
  self.container['Config']['Env']=['POSTGRES_DB=another']
  with self.assertRaises(ValueError):g.validate_target(self.url,self.container)
 def test_rejects_stopped_container(self):
  self.container['State']['Running']=False
  with self.assertRaises(ValueError):g.validate_target(self.url,self.container)
if __name__=='__main__':unittest.main()

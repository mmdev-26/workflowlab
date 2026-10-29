import unittest,json
from pathlib import Path
from engine import analyze,simulate
class Tests(unittest.TestCase):
 def setUp(self):self.d=json.loads(Path(__file__).with_name('example.json').read_text())
 def test_repeatable(self):self.assertEqual(analyze(self.d),analyze(self.d))
 def test_exact_queue(self):
  x=simulate([0,1,2],[{'name':'one','servers':1,'serviceMean':2}],0);self.assertEqual([j['completed'] for j in x['jobs']],[2,4,6]);self.assertEqual(x['summary']['meanQueueWait'],1)
 def test_capacity(self):
  a=simulate([0,1,2],[{'name':'one','servers':2,'serviceMean':2}],0);self.assertEqual(a['summary']['meanQueueWait'],0)
 def test_monotonic_jobs(self):
  x=analyze(self.d)
  for j in x['jobs']:self.assertGreaterEqual(j['completed'],j['arrived']);self.assertGreaterEqual(j['queueWait'],0)
 def test_utilization(self):
  for stage in analyze(self.d)['stages']:self.assertLessEqual(stage['utilization'],1)
 def test_invalid_capacity(self):self.d['stages'][0]['servers']=0;self.assertRaises(ValueError,analyze,self.d)
 def test_invalid_size(self):self.d['jobs']=0;self.assertRaises(ValueError,analyze,self.d)
 def test_scenario_same_arrivals(self):
  x=analyze(self.d);self.assertEqual([j['arrived'] for j in x['jobs']],[j['arrived'] for j in x['scenario']['jobs']])
 def test_stage_completion_reorders(self):
  # A downstream FCFS queue must sort actual arrivals, not upstream job IDs.
  x=simulate([10,0],[{'name':'one','servers':1,'serviceMean':1}],0);self.assertEqual([j['completed'] for j in x['jobs']],[11,1])
if __name__=='__main__':unittest.main()

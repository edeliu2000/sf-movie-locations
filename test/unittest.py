'''
Created on Jul 21, 2014

@author: eni
'''

import unittest
from google.appengine.ext import testbed

from service.dataloader import ImportManager
from model.movie import SFMovieLocation

class CSVEntryTestCase(unittest.TestCase):

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_taskqueue_stub()
    self.testbed.init_datastore_v3_stub()
      
  def tearDown(self):
    self.testbed.deactivate()

  def testProcessCSVEntry(self):
    import_manager = ImportManager()
    
    entry = ['film name', '1998', 'Coit Tower ', 'facts', 'company', 'distributer', 'Ethan Hawke', 'whatever']
    import_manager.process_csv_entry(entry)
    
    #test storage in db and in task queue
    resultsFromDB = SFMovieLocation.all().fetch(2)
    self.assertEqual(1, len(resultsFromDB))
    self.assertEqual('film name', resultsFromDB[0].name)
    self.assertEqual('Coit Tower', resultsFromDB[0].location)
        
    
if __name__ == '__main__':
  unittest.main()

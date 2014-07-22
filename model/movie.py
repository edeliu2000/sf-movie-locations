'''
Created on Jul 20, 2014

@author: eni
'''

import logging
import math
import re

from google.appengine.ext import db
from google.appengine.api import taskqueue

class SFMovieLocation(db.Model):
  name = db.StringProperty(default="", required=False, indexed=False)
  director = db.StringProperty(default="", required=False)
  releaseYear = db.IntegerProperty(default=0, required=False)
  zipCode = db.StringProperty(default="", required=False)
  location = db.StringProperty(default="", required=False)
  geoLocation = db.GeoPtProperty(default=None, required=False, indexed=False)
  
  
  def add_to_index_queue(self):
    
    try:
      queue = taskqueue.Queue(name='locationindex-queue')
      task = taskqueue.Task(
        url='/worker/locationindex/add/',
        params={'key':str(self.key())})
      queue.add(task)
    
    except Exception:
      #fail silently but log
      logging.warn("Failed to add event to indexing queue")
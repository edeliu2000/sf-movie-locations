'''
Created on Jul 20, 2014

@author: eni
'''

import webapp2

from google.appengine.ext import db
from google.appengine.api import taskqueue

from model.movie import SFMovieLocation
from service.search import SearchManager


"""
  Internal worker to add locations to index. Gets its tasks from the taskqueue
""" 

class AddNewLocationToIndex(webapp2.RequestHandler):

  def post(self):
    key = self.request.get('key')
    #get the entry from DB
    movie_location = SFMovieLocation.get(key)
    
    if movie_location:
      search_manager = SearchManager()
      #index entry
      search_manager.index_movie_location(movie_location)
      
      
    
    





app = webapp2.WSGIApplication([('/worker/locationindex/add/', AddNewLocationToIndex)],
                                       debug=True)


  

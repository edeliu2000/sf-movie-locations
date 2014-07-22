'''
Created on Jul 20, 2014

@author: eni
'''

import webapp2
import os

from google.appengine.ext.webapp import template

from service.search import SearchManager

class SearchMovieLocations(webapp2.RequestHandler):

  def get(self):
    start = self.request.get('start')
    name = self.request.get('name')
    
    name = name.strip() if name else ''
    
    movie_locations = []
    if name:
      search_manager = SearchManager()
      movie_locations = search_manager.search_movie_location(name, start)
      
    
    template_values = {
        'movieLocations':movie_locations,
        'limit':20
      }

    path = os.path.join(os.path.dirname(__file__), '../view/json/location_search_result.json')
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
    self.response.out.write(template.render(path, template_values))      


app = webapp2.WSGIApplication([('/search/movie/locations/', SearchMovieLocations)],
                                       debug=True)
    
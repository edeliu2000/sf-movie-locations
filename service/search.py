'''
Created on Jul 20, 2014

@author: eni
'''

import logging

from google.appengine.api import search


class SearchManager():
  
  """
     Method for searching the movie location catalog
  """   
  def search_movie_location(self, name, start):
    # Specify the query string using the Search API's Query language.
    query_str = 'default:"{0}"'.format(name)
    sort_expr = search.SortExpression(expression='name', direction=search.SortExpression.ASCENDING, default_value='')
    returned_fields = ['name', 'director', 'year', 'location', 'geoLocation']
    
    #pick the index to search    
    index = search.Index(name='location-index')
    
    #get the cursor for paging
    cursor = search.Cursor(web_safe_string=start) if start else search.Cursor()
      
    results = index.search(search.Query(
      # Specify the query string using the Search API's Query language.
      query_string=query_str,
      options=search.QueryOptions(
        limit=20,
        cursor=cursor,
        sort_options=search.SortOptions(
          expressions=[sort_expr],
          limit=1000),
        returned_fields=returned_fields
    )))
    
    
    subject_list = []
    for subj in results.results:
      subject_list.append({"doc_id":subj.doc_id, "fields":subj.fields})
      
    return subject_list
  
  
  
  """
     Method for adding a movie location entry in the search engine index
  """   
  def index_movie_location(self, movie_location):
    # Get the index.
    index = search.Index(name='location-index')
    default_field = (movie_location.name + " : " + movie_location.location)
    
    fields = [search.TextField(name='default', value=default_field, language='en'),
              search.TextField(name='name', value=movie_location.name, language='en'),
              search.TextField(name='location', value=movie_location.location, language='en'),
              search.TextField(name='director', value=movie_location.director, language='en'),
              search.NumberField(name='year', value=movie_location.releaseYear)]
    
    if movie_location.geoLocation:
      fields.append(search.GeoField(name='geoLocation', 
                                    value=search.GeoPoint(movie_location.geoLocation.lat, 
                                                          movie_location.geoLocation.lon)))
                
    
    # Create a document.
    doc = search.Document(
        doc_id=str(movie_location.key()),
        fields=fields)

    # Index the document.
    try:
      index.put(doc)
    except search.PutError, e:
      result = e.results[0]
      if result.code == search.OperationResult.TRANSIENT_ERROR:
        # add retry logic at some point if there is time left
        pass

    except search.Error, e:
      # log the failure
      logging.error("Error indexing movie location document: " + str(movie_location.key()) + "  name: " + movie_location.name)

        
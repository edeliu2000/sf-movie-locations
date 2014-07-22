'''
Created on Jul 20, 2014

@author: eni
'''

import csv
import webapp2
import logging

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db

from model.movie import SFMovieLocation 

# helper method
def stripString(value, defaultValue):
  return value.strip() if value else defaultValue  
    

class ImportManager():
  
  """
  Stores each entry in the DB and starts the indexing process for that entry
  """
  def process_csv_entry(self, entry):
    try:  
      name, year, location, facts, company, distributor, director = entry[:7]
      
      #fill entity
      dbEntity = SFMovieLocation()
      dbEntity.name = stripString(name, "")
      dbEntity.location = stripString(location, "")
      dbEntity.director = stripString(director, "")
      dbEntity.releaseYear = int(stripString(year, 0))

      #store in DB
      dbEntity.put()
      
      #add to index queue
      dbEntity.add_to_index_queue()
      
    except Exception:
      logging.warn("failed to process row: " + str(entry))  
      
    

"""
Simple class to show a form where to upload a csv file

""" 
class UploadForm(webapp2.RequestHandler):
  
  def get(self):
    upload_url = blobstore.create_upload_url('/admin/upload')
 
    html_string = """
    <form action="%s" method="POST" enctype="multipart/form-data">
    Upload File:
    <input type="file" name="file"> <br>
    <input type="submit" name="submit" value="Submit">
    </form>""" % upload_url
 
    self.response.write(html_string)
 
 
"""
Processes the uploaded csv file.
CSV files should not contain more than 150-200 entries. Bigger files need to be chunked.

""" 
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):

  def process_csv(self, blob_info):
    
    blob_reader = blobstore.BlobReader(blob_info.key())
    reader = csv.reader(blob_reader, delimiter=',')
    
    import_manager = ImportManager()
    
    for row in reader:
      import_manager.process_csv_entry(row)
  
      
  def post(self):
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    self.process_csv(blob_info)
 
    blobstore.delete(blob_info.key())  # optional: delete file after import
    self.redirect("/admin/loaddata")
 
 
 
 
app = webapp2.WSGIApplication([
    ('/admin/loaddata', UploadForm),
    ('/admin/upload', UploadHandler)
], debug=True)

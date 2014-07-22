sf-movie-locations
==================

minimal app showing places where movies have been shot in sf

http://sfmovies-experiment.appspot.com/

Techincal Track: full stack 


Application Design:
--------------

The SF Movie app is a single page JS app that communicates with a Restful API hosted on Google App Engine. Users can search for movie locations in SF given a movie name or a location address/name. The application shows an autocomplete form that suggests movie names associated with the typed in location or locations associated with the typed in movie names as the users type in. If the user clicks on one of those suggestions the location associated with that entry is shown on the map. 

The reason for needing the user to type in movie names and showing them on the map only after clicking was that the data provided for the SF movie locations (about 1100 entries) only had unformated addresses (no geolocations) and I need geolocations to show points on a map. Using a geolocation REST API on the backend during the data import step was first considered. However, there are heavy limits in converting addresses to geolocations for the few geolocation API-s out there (google geolocation API has a limit of 100/day). What I opted for was to use the less restrictive JS geolocation API-s on the fly for the few suggestion results and only show those on the map.


- **Finding Suggestions for AutoComplete, Display on the Map**: 
The app consists of a single page html and JavaScript that queries the backend via a REST API for suggestions and displays the results in a list (autocomplete) as well as on a google map. The application needed to find street names or movie names existing in the data entries based on incomplete user input. This makes the case to use a search engine that can handle the ambiguity of incomplete user input as well as search fast accross multiple dimensions. I opted for Google App Engine primarily because it offers a search engine that needs little/no configuration compared to SOLR or ElasticSearch. Also being very familiar on Python/Django helps as AppEngine supports that stack. The data entries needed to be added to the search engine index as well as imported in a DB for persistence (in case I would need to reindex or whatever). Because of speed the REST API serves data directly from the search engine. Since the data is always the same caching API results on both backend (memcache, redis) or frontend would have been appropriate. Because of my time contraints (spending no more then a few hours on a single day) I didn't get to implement it.



- **Importing the Data**:
There were about 1100 entries that needed to be stored and indexed. A simple data importer uploads a csv file, stores its entries in DB and indexes the entries on the search engine. I chose to use a queue (AppEngine taskqueue) for the indexing to not flood the system with thousands of indexing tasks at once as well as to get retry logic for free if indexing failed for a few entries (AppEngine taskqueue retries until successful). The queue sends tasks to one or more workers at a configured rate per second and the workers do the real indexing. This approach allows for scalable near real-time index updates on entries without blocking the request thread.



- **Frontend**:
Because of time contraints and the minimal interface needed I opted not to use any of the major JS frameworks like Backbone or Angular. Instead I used my own JS code and a minimal library for cross browser DOM manipulation and xhr (XUI JS). I also could not spend much time in the UI so it's really minimal.




SF Movies REST API:

GET http(s)://sfmovies-experiment.appspot.com/search/movie/locations/?name=<movie name or street name in SF>

Returns a JSON object with a locations property. Example:

    {
        "locations":[{
            "key":"ahVzfnNmbW92aWVzLWV4cGVyaW1lbnRyHAsSD1NGTW92aWVMb2NhdGlvbhiAgICA2reXCgw", 
            "name":"Greed", 
            "location":"Hayes Street at Laguna", 
            "director":"Eric von Stroheim", 
            "year":"1924", 
        }]
        "limit":20
    }


Stack:
--------------

Backend (Python, Django, AppEngine DataStore, App Engine Search, App Engine Queue)

Frontend (JavaScript, Google Maps API 3, XUI JS used for a few cross browser dom operations and xhr calls, HTML5, CSS)

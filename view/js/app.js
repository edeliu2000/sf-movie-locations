var App = (function(){
  
  //helper function, creates xui dom elements
  var el = function(e, cls){
      var r = x$(document.createElement(e));
      for(var i=0;i<cls.length;i++){r.addClass(cls[i])}
      return r;
    },

    //App AutoComplete object
    autoCompleteObj, 

    //App Map object
    map; 
  
  
  
  //AutoComplete class
  function AutoComplete(minKeys, parentEl){
    this.parentEl = parentEl;
    this.oldText = "";
    this.newText = "";
    this.minNumChars = 3;
    this.minKeys = minKeys || 1;
    
    this.suggestions = [];
  }
  
  AutoComplete.prototype.canTriggerLoad = function(text){
    return text && text.length >= this.minNumChars
      && Math.abs(this.newText.length - text.length) >= this.minKeys;
  }	
  
  AutoComplete.prototype.onKeyStroke = function(text){
    if(this.canTriggerLoad(text)){
      this.oldText = this.newText;
      this.newText = text;
      this.loadSuggestions();
    }
  }
  
  
  
  AutoComplete.prototype.loadSuggestions = function(){
    var _this = this;
    this.parentEl.xhr('/search/movie/locations/?name=' + escape(_this.newText), {
      async:true,
      callback:function(){
      	var responseObj = JSON.parse(this.responseText),
      	  suggList = responseObj.locations || [],
      	  suggestion;
      	
      	_this.suggestions = [];
      	   
        for(var i = 0; i<suggList.length; i++){
          suggestion = new Suggestion(suggList[i]);
          _this.addSuggestion(suggestion);
        }
        
        _this.showAsList();
      }
    });
  }
  
  
  AutoComplete.prototype.addSuggestion = function(suggestion){
    this.suggestions.push(suggestion);  
  }
  
  
  AutoComplete.prototype.showAsList = function(){
    var docFragment = x$(document.createDocumentFragment()), 
      item,
      _this = this,

      //use closure to capture index when used in for loop
      itemClicked = function(index){
        return function(){
          _this.parentEl.removeClass('expanded')
          _this.suggestions[index].loadGeoLocation();
        };
      };

    
    for(var i = 0; i<this.suggestions.length; i++){
      item = el('div', ['suggestion']).html(this.suggestions[i].name + ' | ' + this.suggestions[i].location);
      item.click(itemClicked(i));
      docFragment.bottom(item[0]);
    }
    
    
    //add class to show in UI
    if(this.suggestions.length){
      this.parentEl.addClass('expanded');
    }else{
      this.parentEl.removeClass('expanded');
    }
    
    this.parentEl.html(docFragment[0]);
      
  }
  
  
  
  //Movie Location Suggestion class (item within the autocomplete list)
  function Suggestion(jsonObj){
    this.name = jsonObj.name;
    this.location = jsonObj.location;
    this.geoLocation = "";
  }	
  
  
  Suggestion.prototype.loadGeoLocation = function(){
    var loc = this.location + ', San Francisco, CA',
      movieName = this.name;
      
    map.geocoder.geocode({'address': loc}, function(results, status){
      if(status == google.maps.GeocoderStatus.OK){
        
        var latlng = results[0].geometry.location;
        map.googleMap.setCenter(latlng);
        map.googleMap.setZoom(14);
        
        if(map.marker){
          map.marker.setMap(null);
        }
        
        map.marker = new google.maps.Marker({
          position: latlng,
          map: map.googleMap,
          title:movieName
        });
        
      }
    });  
  }
  
  
  
  //Map class
  function Map(parentId){
    this.parentId = parentId;
    this.geocoder = new google.maps.Geocoder();
    this.googleMap = "";
    this.marker = "";
  }
  
  Map.prototype.load = function(){
    var mapOptions = {
      zoom: 11,
      center: new google.maps.LatLng(37.74724, -122.44791)
    };

    this.googleMap = new google.maps.Map(document.getElementById(this.parentId), mapOptions);
    
  }
  
  
  
  return  {
    start: function(){
      
      map = new Map('map-container');
      map.load();
      
      //add listener for keystrokes
      x$('#autoComplete').on("keyup", function(){
        if(!autoCompleteObj){
          autoCompleteObj = new AutoComplete(1, x$('#suggestionsParent'))
        }
        autoCompleteObj.onKeyStroke(x$('#autoComplete')[0].value)
      });
      
      //show autocomplete on focus
      x$('#autoComplete').on("focus", function(){
        var canShow = autoCompleteObj 
              && autoCompleteObj.suggestions
              && autoCompleteObj.suggestions.length 
              && x$('#autoComplete')[0].value;
        
        if(canShow){
          autoCompleteObj.parentEl.addClass('expanded');
        }
        
      });
      
      
    }
  };
  
  
})();

x$(window).on('load', function(){
  App.start();
});
        

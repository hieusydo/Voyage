// Reference: https://stackoverflow.com/a/35858424

// Bascically doing this: <script src="https://maps.googleapis.com/maps/api/..." async defer></script>
function loadScript(srcScript, myCallback) {
    var tmpHead = document.getElementsByTagName('HEAD')[0];
    var tmpScript = document.createElement('script');
    tmpScript.type = 'text/javascript';
    tmpScript.src = srcScript;
    tmpHead.appendChild(tmpScript);
    tmpScript.onload = myCallback;
}

function drawMap() {
  console.log('drawMap()');
  // Make AJAX call to get landmarks
  var req = new XMLHttpRequest();  
  var hostPart = location.hostname
  if (hostPart === 'localhost' || hostPart === '127.0.0.1') {
    hostPart += (':' + location.port)
  }

  var url = 'http://' +  hostPart + '/landmark/getAll/'
  req.open('GET', url, true) // true = async

  req.onreadystatechange = function () {
    if (req.readyState === 4 && req.status === 200) {
         console.log('Got back response');
        // console.log(req.responseText);
        // Jsonify response
        data = JSON.parse(req.responseText);
      console.log(data)
        allLms = data.landmarks

        // Calculate center of view
        pid = [];
        ratings = []
        comments = [];
        allCoords = [];
        visitDate = [];

        allLat = 0;
        allLng = 0;
        for (i = 0; i < allLms.length; i++ ) {
          l = allLms[i]
          var coord = { lat: l["lat"], lng: l["lng"] };  
          allCoords.push(coord)
          pid.push(l["place_id"])
          ratings.push(l["rating"])
          comments.push(l["comment"])
          visitDate.push(l["date_created"])

          // Book keeping to find center of view
          allLat += l["lat"]
          allLng += l["lng"]
        }
        centerCoord = { lat: allLat/allLms.length, lng: allLng/allLms.length }
        // console.log("center: ", centerCoord)

        // Start to draw map
        var styledMapType = new google.maps.StyledMapType([
          {
            "elementType": "geometry",
            "stylers": [
              {
                "color": "#ebe3cd"
              }
            ]
          },
          {
            "elementType": "labels.text.fill",
            "stylers": [
              {
                "color": "#523735"
              }
            ]
          },
          {
            "elementType": "labels.text.stroke",
            "stylers": [
              {
                "color": "#f5f1e6"
              }
            ]
          },
          {
            "featureType": "administrative",
            "elementType": "geometry.stroke",
            "stylers": [
              {
                "color": "#c9b2a6"
              }
            ]
          },
          {
            "featureType": "administrative.land_parcel",
            "elementType": "geometry.stroke",
            "stylers": [
              {
                "color": "#dcd2be"
              }
            ]
          },
          {
            "featureType": "administrative.land_parcel",
            "elementType": "labels.text.fill",
            "stylers": [
              {
                "color": "#ae9e90"
              }
            ]
          },
          {
            "featureType": "landscape.natural",
            "elementType": "geometry",
            "stylers": [
              {
                "color": "#dfd2ae"
              }
            ]
          },
          {
            "featureType": "poi",
            "elementType": "geometry",
            "stylers": [
              {
                "color": "#dfd2ae"
              }
            ]
          },
          {
            "featureType": "poi",
            "elementType": "labels.text.fill",
            "stylers": [
              {
                "color": "#93817c"
              }
            ]
          },
          {
            "featureType": "poi.park",
            "elementType": "geometry.fill",
            "stylers": [
              {
                "color": "#a5b076"
              }
            ]
          },
          {
            "featureType": "poi.park",
            "elementType": "labels.text.fill",
            "stylers": [
              {
                "color": "#447530"
              }
            ]
          },
          {
            "featureType": "road",
            "stylers": [
              {
                "visibility": "off"
              }
            ]
          },
          {
            "featureType": "road",
            "elementType": "geometry",
            "stylers": [
              {
                "color": "#f5f1e6"
              }
            ]
          },
          {
            "featureType": "road.arterial",
            "elementType": "geometry",
            "stylers": [
              {
                "color": "#fdfcf8"
              }
            ]
          },
          {
            "featureType": "road.highway",
            "elementType": "geometry",
            "stylers": [
              {
                "color": "#f8c967"
              }
            ]
          },
          {
            "featureType": "road.highway",
            "elementType": "geometry.stroke",
            "stylers": [
              {
                "color": "#e9bc62"
              }
            ]
          },
          {
            "featureType": "road.highway.controlled_access",
            "elementType": "geometry",
            "stylers": [
              {
                "color": "#e98d58"
              }
            ]
          },
          {
            "featureType": "road.highway.controlled_access",
            "elementType": "geometry.stroke",
            "stylers": [
              {
                "color": "#db8555"
              }
            ]
          },
          {
            "featureType": "road.local",
            "elementType": "labels.text.fill",
            "stylers": [
              {
                "color": "#806b63"
              }
            ]
          },
          {
            "featureType": "transit.line",
            "elementType": "geometry",
            "stylers": [
              {
                "color": "#dfd2ae"
              }
            ]
          },
          {
            "featureType": "transit.line",
            "elementType": "labels.text.fill",
            "stylers": [
              {
                "color": "#8f7d77"
              }
            ]
          },
          {
            "featureType": "transit.line",
            "elementType": "labels.text.stroke",
            "stylers": [
              {
                "color": "#ebe3cd"
              }
            ]
          },
          {
            "featureType": "transit.station",
            "elementType": "geometry",
            "stylers": [
              {
                "color": "#dfd2ae"
              }
            ]
          },
          {
            "featureType": "water",
            "elementType": "geometry.fill",
            "stylers": [
              {
                "color": "#b9d3c2"
              }
            ]
          },
          {
            "featureType": "water",
            "elementType": "labels.text.fill",
            "stylers": [
              {
                "color": "#92998d"
              }
            ]
          }
        ])
        var map = new google.maps.Map(document.getElementById('voyageMap'), {
          zoom: 5,
          center: centerCoord,
          mapTypeControlOptions: {
            mapTypeIds: ['styled_map']
          }        
        });

        //Associate the styled map with the MapTypeId and set it to display.
        map.mapTypes.set('styled_map', styledMapType);
        map.setMapTypeId('styled_map');

        //Associate the styled map with the MapTypeId and set it to display.

        var service = new google.maps.places.PlacesService(map);
        var infowindow = new google.maps.InfoWindow();
        for (c = 0; c < allLms.length; c++ ) {

          //Place marker
          var marker = new google.maps.Marker({
            position: allCoords[c],
            map: map
          });   
 
          var comment = String(comments[c]);
          var rating = String(ratings[c]);
          var date = String(visitDate[c]);
          if(comment === ""){
                 comment = "None"
          }

          //Set up clickable event
          service.getDetails({
            placeId: pid[c]
          }, function(place, status) {
              //Set up click event for marker
              google.maps.event.addListener(marker, 'click', function() {
                        infowindow.setContent('<div><strong>' + place.name + '</strong><br><br>' +
                        place.formatted_address + '<br><br><strong>' +
                        'Date Visited: ' + '</strong>' + visitDate + '<br><strong>' +
                        'Rating: ' + '</strong>' + rating + '<br><br><strong>' +
                        'Comment: ' + '</strong><br>' + comment +
                        '</div>');
                        infowindow.open(map, this);
          })});
          
        }
    }
  };

  req.send();
}


loadScript("https://maps.googleapis.com/maps/api/js?key=AIzaSyDwN4ya6pztrnG0S6wSpiFZfTcKRK-_50o&libraries=places", drawMap);

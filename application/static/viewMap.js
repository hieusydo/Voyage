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

function attachInfoToMarker(marker, lmDeets) {
  console.log(lmDeets)
  var infowindow = new google.maps.InfoWindow();
  infowindow.setContent('<div id="markerPopup">' +
    '<h6>' + lmDeets['name'] + '</h6>' +
    '<b>Date Visited: </b>' + lmDeets['date'] + '<br>' +
    '<b>Rating: </b>' + lmDeets['rating'] + '<br>' +
    '<b>Comment: </b>' + lmDeets['comment'] + '<br><br>' + 
    '<img src=' + lmDeets['photo_url'] + ' alt="Uploaded Image">' +
    '</div>'
  );

  marker.addListener('click', function() {
    infowindow.open(marker.get('map'), marker);
  });
}

function drawMap() {
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
        // Jsonify response
        data = JSON.parse(req.responseText);
        allLms = data.landmarks
        theme = data.theme

        // Calculate center of view
        var allCoords = [];
        allLat = 0;
        allLng = 0;
        for (i = 0; i < allLms.length; i++ ) {
          l = allLms[i]
          var coord = { lat: l["lat"], lng: l["lng"] };  
          allCoords.push(coord)
          // Book keeping to find center of view
          allLat += l["lat"]
          allLng += l["lng"]
        }
        centerCoord = { lat: allLat/allLms.length, lng: allLng/allLms.length }

        // Start to draw map
        var styledMapType = new google.maps.StyledMapType(theme)
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

        for (c = 0; c < allLms.length; c++ ) {
          //Place marker
          var marker = new google.maps.Marker({
            position: allCoords[c],
            map: map
          });   

          // Add details for each coordinate c
          var lmDeets = {
            'name' : allLms[c]['name'],
            'comment' : allLms[c]['comment'] === "" ? 'None' : allLms[c]['comment'], 
            'rating' : allLms[c]['rating'],
            'date' : allLms[c]['date_created'],
            'photo_url' : allLms[c]['photo_url'],
          }           
          attachInfoToMarker(marker, lmDeets)          
        }
    }
  };

  req.send();
}


loadScript("https://maps.googleapis.com/maps/api/js?key=AIzaSyDwN4ya6pztrnG0S6wSpiFZfTcKRK-_50o", drawMap);

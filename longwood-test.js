var map;
var markers = new Array();
var infowindows = new Array();

function makeMarkerAndInfobox(currentSpecimen) {
  var positionOnMap = new google.maps.LatLng(currentSpecimen.latlon[0], currentSpecimen.latlon[1]);

  var marker = new google.maps.Marker({
    position: positionOnMap,
    map: map,
    title: currentSpecimen.locality
  });

  var contentInfobox =  '<div class="content">'+
    '<div class="siteNotice">'+
    '</div>'+
    '<h1 class="firstHeading" class="firstHeading">'+currentSpecimen.species+'</h1>'+
    '<div class="bodyContent">'+
    '<img src="img/' + currentSpecimen.accession_number + '.jpg" />'+
    '<p>'+currentSpecimen.locality+'</p>'+
    '<p>Accession Number: '+currentSpecimen.accession_number+ '<br/>'+
    'Country: '+currentSpecimen.country+ '<br/>' +
    'Species: '+currentSpecimen.species+'</p>'+
    '</div>'+
    '</div>';

  var infowindow = new google.maps.InfoWindow({
      content: contentInfobox
  });

  marker.__infowindow = infowindow;

  return marker;
}

function addMarkersAndInfowindows () {
  for (var i = 0; i < boxwoodData.length; i++) {
    var mi = makeMarkerAndInfobox(boxwoodData[i]);
    markers.push(mi);
  }
}

function initialize() {
  var mapOptions = {
    zoom: 4,
    center: new google.maps.LatLng(39.9033765,32.767873)
  };

  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  addMarkersAndInfowindows();

  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
    google.maps.event.addListener(markers[i], 'click', function(e) {
      this.__infowindow.open(map, this);
    });
  }

  var markerCluster = new MarkerClusterer(map, markers);
}

google.maps.event.addDomListener(window, 'load', initialize);

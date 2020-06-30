function getCookie(name) { //csrf verification
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

var origin_pos = {} //represent the origin position, i.e. the value of input box with id "origin"
var destination_pos = {} //represent the destination position, i.e. the value of input box with id "origin"
var origin_value = "";

var infowindow = new google.maps.InfoWindow();

function initMap(){
    //Initialize the map when the page is loaded
    //get the users location when webpage is loaded
    //show the stop clusters

    //get user's location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        origin_pos = pos;
        map =new google.maps.Map(document.getElementById('googleMap'), {
                  center: {lat: pos.lat, lng: pos.lng},
                  zoom: 7
                });
        var loc_marker = new google.maps.Marker({
                              map: map,
                              position: pos,
              });

        var stopKeys = Object.keys(stopdata);

        // Add stop markers with onclick
        var marker;
        var markers = [];
        var stopKey;
        for (i=0;i<stopKeys.length;i++) {
            stopKey = stopKeys[i];
            if (stopdata[stopKey]['routes'] != "") {
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(
                        stopdata[stopKey]['latitude'],
                        stopdata[stopKey]['longitude']),
                    map: map
                });
                marker.setMap(map);
                markers.push(marker);
                marker.addListener('click', (function (marker, stopKey) {
                    return function () {getStopInfo(marker, stopKey);}
                })(marker, stopKey));
            }
        }
        // alert(markers.length);

        // create marker clusters using array of markers
        var markerCluster = new MarkerClusterer(map, markers, { maxZoom: 14, imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });

        //get address and weather information from backend and display them
        $.ajax({
            headers: {'X-CSRFToken': csrftoken},
            url: '/init',
            type: 'POST',
            data: pos,
            dataType: 'json',
            async:false,
            success: function (data) {
                // document.getElementById(elementid).value = data.address;
                loc_infoWindow = new google.maps.InfoWindow;
                loc_infoWindow.setPosition(pos);
                loc_infoWindow.setContent("you r here:"+data.address);
                origin_value = data.address;
                loc_infoWindow.open(map, loc_marker);
                document.getElementById("weather").innerHTML = data.weather;
            },
            error: function () {return "error";alert("error");},
        });
        map.setCenter(pos);
      }, function() {
        handleLocationError(true, loc_infoWindow, map.getCenter());
      });
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, loc_infoWindow, map.getCenter());
    }
    // document.getElementById('origin').value = 'Your current location';
}
function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    //supporting functions of initMap()
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
}

function getStopInfo(marker, stopKey) {
    //supporting functions of initMap()

    let content = "<div id='infowindow'><h5>Stop Number: " + stopdata[stopKey]["stopno"] + "</h5>";
    content += "Routes: " + stopdata[stopKey]['routes'];
    content += "</div>"

    // add content of get request to info window
    infowindow.setContent(content);
    infowindow.open(map, marker);
}

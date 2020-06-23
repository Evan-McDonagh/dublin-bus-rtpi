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

function initMap(){//Initialize the map when the page is loaded

    // get the users location when webpage is loaded
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        origin_pos = pos;
        map = new google.maps.Map(document.getElementById('map'), {
                  center: {lat: pos.lat, lng: pos.lng},
                  zoom: 13
                });
        var marker = new google.maps.Marker({
                              map: map,
                              position: pos,
              });
        $.ajax({
            headers: {'X-CSRFToken': csrftoken},
            url: 'init',
            type: 'POST',
            data: pos,
            dataType: 'json',
            async:false,
            success: function (data) {
                // document.getElementById(elementid).value = data.address;
                infoWindow = new google.maps.InfoWindow;
                infoWindow.setPosition(pos);
                infoWindow.setContent("you r here:"+data.address);
                origin_value = data.address;
                infoWindow.open(map, marker);
                document.getElementById("weather").innerHTML = data.weather;
            },
            error: function () {return "error";alert("error");},
        });
        map.setCenter(pos);
      }, function() {
        handleLocationError(true, infoWindow, map.getCenter());
      });
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
    // document.getElementById('origin').value = 'Your current location';
}
function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
}

function search() {//trigger relevant functions to generate directions
    //query the place according to the input boxes.
    if (document.getElementById('origin').value == 'Your current location' || document.getElementById('origin').value ==""){
        var s_origin = origin_value;
    }
    else{var s_origin = document.getElementById('origin').value}
    var s_dest = document.getElementById('destination').value;
    alert('searchstart' + s_origin);
    // alert('searchend' + s_dest);

    var map2 = new google.maps.Map(document.getElementById('map'), {
        center: origin_pos,
        zoom: 13
    });
    var service = new google.maps.places.PlacesService(map2);
    var s_origin_request = {
        query: s_origin,
        fields: ['name', 'geometry'],
    };
    service.findPlaceFromQuery(s_origin_request, function (results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            // alert(results[0].geometry.location);
            map2.setCenter(results[0].geometry.location);
            var infowindow = new google.maps.InfoWindow({
                content: s_origin,
            });
            var marker = new google.maps.Marker({
                map: map2,
                position: results[0].geometry.location,
            });
            marker.addListener("mouseover", function () {
                infowindow.open(map, marker);
            });
            origin_pos = results[0].geometry.location;
            origin_pos = {'lat': results[0].geometry.location.lat(), 'lng': results[0].geometry.location.lng()}
        }
    });
    var s_dest_request = {
        query: s_dest,
        fields: ['name', 'geometry'],
    };
    service.findPlaceFromQuery(s_dest_request, function(results, status) {
          if (status === google.maps.places.PlacesServiceStatus.OK) {
              // alert(results[0].geometry.location);
              map2.setCenter(results[0].geometry.location);
              var infowindow = new google.maps.InfoWindow({
                content: s_dest,
                });
              var marker = new google.maps.Marker({
                              map: map2,
                              position: results[0].geometry.location,
                              // icon:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
              });
              marker.addListener("mouseover", function () {
                    infowindow.open(map, marker);
                });
              destination_pos = {'lat':results[0].geometry.location.lat(), 'lng':results[0].geometry.location.lng()}
      }
    });
}

function calcRoute() {
    // alert("clacroute");
  var start = document.getElementById('origin').value;
  var end = document.getElementById('destination').value;
  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer();
  var request = {
    origin: {query: document.getElementById('origin').value},
    destination: {query: document.getElementById('destination').value},
    travelMode: 'TRANSIT',
    provideRouteAlternatives: true,
  };
    var map3 = new google.maps.Map(document.getElementById('map'),{
        center: origin_pos,
        zoom:13,
    });
    directionsRenderer.setMap(map3);
    directionsService.route(request, function(result, status) {
    if (status == 'OK') {
      directionsRenderer.setDirections(result);
    }
  });
   directionsRenderer.setPanel(document.getElementById('figure1'));
}
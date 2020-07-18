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
// var destination_pos = {} //represent the destination position, i.e. the value of input box with id "origin"
var origin_value = "";

var infowindow = new google.maps.InfoWindow();
var map;

function initMap(){
    //Initialize the map when the page is loaded
    //get the users location when webpage is loaded
    //show the stop clusters

    //Initializing vars 
    var marker;
    var markers = [];
    var stopKey;
    var lngT = 0.005;
    var latT = 0.003;
    var stopKeys = Object.keys(stopdata);

    var pos = {lat:53.350140, lng:-6.266155};
    map =new google.maps.Map(document.getElementById('googleMap'), {
                  // center: {lat: pos.lat, lng: pos.lng},
        center:{lat:53.350140, lng:-6.266155},
                  zoom: 10
                });
    loc_infoWindow = new google.maps.InfoWindow;

    //get user's location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            // pos.lat = position.coords.latitude;
            // pos.lng = position.coords.longitude;
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        // alert(pos.lat)
        origin_pos = pos;
        map.setCenter(pos);
        map.setZoom(14);
        // loc_infoWindow.setPosition(pos);
        pos['status'] = 'OK';
        sendlocation({'lat':pos.lat, 'lng':pos.lng}, loc_infoWindow, map);
        realtimeweather({'lat':pos.lat, 'lng':pos.lng});

        //Add only the stop makers near user if geolocation enabled:
        for (i=0;i<stopKeys.length;i++){
            stopKey = stopKeys[i];
            if (stopdata[stopKey]['routes'] != "" && stopdata[stopKey]['latitude'] < (pos.lat+latT) && stopdata[stopKey]['latitude'] > (pos.lat-latT) && stopdata[stopKey]['longitude'] < (pos.lng+lngT) && stopdata[stopKey]['longitude'] > (pos.lng-lngT)){
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(
                        stopdata[stopKey]['latitude'],
                        stopdata[stopKey]['longitude']),
                    map: map
                });
            }
        }

      }, function() {
        pos['status'] = "wrong";
        sendlocation({'lat':pos.lat, 'lng':pos.lng}, loc_infoWindow, map);
        realtimeweather({'lat':pos.lat, 'lng':pos.lng});
        handleLocationError(true, loc_infoWindow, map.getCenter(), map);

        // Add all stop markers with onclick if geolocation is not enabled
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
                    return function () {getStopInfo(marker, stopKey, map);}
                })(marker, stopKey));
            }
        
        }
        // create marker clusters using array of markers
        var markerCluster = new MarkerClusterer(map, markers, { maxZoom: 14, imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });
      });
    } else {
      // Browser doesn't support Geolocation
      pos['status'] = 'wrong';
      sendlocation({'lat':pos.lat, 'lng':pos.lng}, loc_infoWindow, map);
      realtimeweather({'lat':pos.lat, 'lng':pos.lng});
      handleLocationError(false, loc_infoWindow, map.getCenter(), map);

      // Add all stop markers if geolocation is not supported
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
                return function () {getStopInfo(marker, stopKey, map);}
            })(marker, stopKey));
        }
    
    }
    // create marker clusters using array of markers
    var markerCluster = new MarkerClusterer(map, markers, { maxZoom: 14, imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });
    }
}
    
google.maps.event.addDomListener(window, 'load', initMap);


function sendlocation(pos, loc_infoWindow, map){
    $.ajax({
        headers: {'X-CSRFToken': csrftoken},
        url: '/init',
        type: 'POST',
        data: pos,
        dataType: 'json',
        // async:false,
        success: function (data) {
            // document.getElementById(elementid).value = data.address;
            // alert(pos.lat);
            var loc_marker = new google.maps.Marker({
                          map: map,
                          position: {'lat':pos.lat, 'lng':pos.lng},
          });
            loc_infoWindow.setPosition({'lat':pos.lat, 'lng':pos.lng});
            loc_infoWindow.setContent("you r here:"+data.address);
            origin_value = data.address;
            loc_infoWindow.open(map, loc_marker);
        },
        error: function () {return "error";alert("error");},
    });
}

function realtimeweather(pos) {
    // alert('realtimeweather')
    $.ajax({
        headers: {'X-CSRFToken': csrftoken},
        url: '/weather',
        type: 'POST',
        data:pos,
        dataType: 'json',
        success: function (data) {
            // alert(data.weather);
            var icon = data['iconUrl']
            var weather_show ="<img src='" + icon  + "'>" +data['descp'] +" "+ data['temp'];
            // console.log(weather_show);
            document.getElementById("weather").innerHTML = weather_show;
        }
    })
}

function handleLocationError(browserHasGeolocation, infoWindow, pos, map) {
    //supporting functions of initMap()
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
}

function getStopInfo(marker, stopKey, map) {
    //supporting functions of initMap()
    var infowindow = new google.maps.InfoWindow;
    let content = "<div id='infowindow'><h5>Stop Number: " + stopdata[stopKey]["stopno"] + "</h5>";
    content += "Routes: " + stopdata[stopKey]['routes'];
    content += "</div>"

    // add content of get request to info window
    infowindow.setContent(content);
    infowindow.open(map, marker);
}

function search() {
    //trigger relevant functions to generate directions
    //query the place according to the input boxes.

    if (document.getElementById('origin').value ==""){var s_origin = origin_value;}
    else{var s_origin = document.getElementById('origin').value}
    var s_dest = document.getElementById('destination').value;

    var map2 = new google.maps.Map(document.getElementById('googleMap'), {
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
            map2.setCenter(results[0].geometry.location);
            var infowindow_ori = new google.maps.InfoWindow({
                content: s_origin,
            });
            var marker_ori = new google.maps.Marker({
                map: map2,
                position: results[0].geometry.location,
                icon:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',

            });
            marker_ori.addListener("mouseover", function () {
                infowindow_ori.open(map2, marker_ori);
            });
            origin_pos = results[0].geometry.location;
            // origin_pos = {'lat': results[0].geometry.location.lat(), 'lng': results[0].geometry.location.lng()}
        }
    });
    var s_dest_request = {
        query: s_dest,
        fields: ['name', 'geometry'],
    };
    service.findPlaceFromQuery(s_dest_request, function(results, status) {
          if (status === google.maps.places.PlacesServiceStatus.OK) {
              map2.setCenter(results[0].geometry.location);
              var infowindow_dest = new google.maps.InfoWindow({
                content: s_dest,
                });
              var marker_dest = new google.maps.Marker({
                              map: map2,
                              position: results[0].geometry.location,
                              icon:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
              });
              marker_dest.addListener("mouseover", function () {
                    infowindow_dest.open(map, marker_dest);
                });
              destination_pos = {'lat':results[0].geometry.location.lat(), 'lng':results[0].geometry.location.lng()}
      }
    });
}

function calcRoute() {
  // var start = document.getElementById('origin').value;
  // var end = document.getElementById('destination').value;
  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer();
  var request = {
    origin: {query: document.getElementById('origin').value},
    destination: {query: document.getElementById('destination').value},
    travelMode: 'TRANSIT',
    transitOptions:{departureTime: new Date(document.getElementById("datetimepicker1").value)},
    provideRouteAlternatives: false,
  };
    var map3 = new google.maps.Map(document.getElementById('googleMap'),{
        center: origin_pos,
        zoom:13,
    });
    directionsRenderer.setMap(map3);
    directionsService.route(request, function(result, status) {
    if (status == 'OK') {
        var routes_dict = {}
        var route_choices = {}
        for (i in result['routes']){
            legs = result['routes'][i]['legs'];
            for (j in legs){
                var walking_dur = 0;
                var bus_dur = 0;
                var bus_name = [];
                var bus_name_str = '';
                steps = legs[j]['steps']
                // alert(result['routes'][i]['bounds'])
                for (k in steps){
                    if (steps[k].travel_mode == 'WALKING'){walking_dur += steps[k]['duration'].value}
                    else if (steps[k].travel_mode == 'TRANSIT'){bus_dur += steps[k]['duration'].value; bus_name.push(steps[k]['transit']['line'].short_name)}
                }
                // alert(bus_name[0])
                if (bus_name.length > 1){for (i in bus_name){bus_name_str += bus_name[i] + "->"}}
                else{bus_name_str = bus_name[0]};
                routes_dict[bus_name_str] = result['routes'][i];
                document.getElementById('routes').innerHTML = "<button id="+bus_name_str + ">"+bus_name_str+"</button>" + "walk:" + walking_dur +"s, on bus:"+ bus_dur+"s<br>";
                // loadstops(bus_name, result['routes'][i]['bounds'])
                document.getElementById(bus_name_str).addEventListener('click', function(){loadstops(bus_name, result['routes'][i]['bounds'], map3);});

            }
        }
        function showinfowindow(marker, id, map){
            $.ajax({
                headers: {'X-CSRFToken': csrftoken},
                url:'/rtmarkerinfo',
                data:{'id':id},
                type:'POST',
                dataType:'json',
                async:true,
                success: function (data) {
                    // alert(data.allinfo)
                    var infowindow = new google.maps.InfoWindow({
                        content:data.allinfo
                    });
                    marker.addListener('click', function(){infowindow.open(map,marker)})
                    // marker.addListener('mouseover', function(){infowindow.open(map,marker)})
                    // marker.addListener('mouseout', function(){infowindow.close(map,marker)})
                }
            })
        }
        function loadstops(bus_name, bounds, map){
            post_data = {'bus':bus_name, 'bounds':bounds}
            $.ajax({
                headers: {'X-CSRFToken': csrftoken},
                url: '/printresult',
                data: JSON.stringify(post_data),
                type:'POST',
                dataType:'json',
                success: function (data) {
                    for (var i=0; i < data.stop_locations.length; i++) {
                        marker = new google.maps.Marker({map:map, position:new google.maps.LatLng(data.stop_locations[i].lat, data.stop_locations[i].lng)});
                        showinfowindow(marker, data.stop_locations[i].id, map);
                    }
                }, error: function () {
                    alert('error');
                },
        });
        }
      directionsRenderer.setDirections(result);
    }
  });
   directionsRenderer.setPanel(document.getElementById('h51'));
}
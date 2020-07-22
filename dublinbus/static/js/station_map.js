// a function to get cookie msg for the csrf verification, has nothing to do with logic stuff
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
var csrftoken = getCookie('csrftoken'); //store the cookie msg in "csrftoken"

var origin_pos = {} //represent the origin position, lat, lng
// var origin_value = ""; //the text in the input box with id "origin"

var map;
var nearMeList = [];
var allstopmarkers = [];
var nearmemarkers = [];
var alongroutemarkers = []

function initMap(){
    //Initialize the map when the page is loaded
    //get the users location when webpage is loaded
    //show the stop clusters

    var pos = {lat:53.350140, lng:-6.266155}; //used to initialize the map, if geolocation enabled, the pos will be changed
    map =new google.maps.Map(document.getElementById('googleMap'), {
        center:pos,
        zoom: 10
    });

    //get user's location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            delete pos.lat;
            delete pos.lng;
            pos['lat'] = position.coords.latitude;
            pos['lng'] = position.coords.longitude;
            // "pos" is changed to be the real location of the user.
        origin_pos = pos;
        map.setCenter(pos);
        map.setZoom(15);
        pos['status'] = 'OK';
        sendlocation(pos, map);
        realtimeweather(pos);
        addallmarkers(map);
        clearmarkers(allstopmarkers);
        addnearmemarkers(map, pos);
      }, function() {
        pos['status'] = "ERROR";
        sendlocation(pos, map);
        realtimeweather(pos);
        handleLocationError(true, map.getCenter(), map);
        addallmarkers(map);
        clearmarkers(allstopmarkers);
        addnearmemarkers(map, pos);
      });
    } else {
      // Browser doesn't support Geolocation
      pos['status'] = 'ERROR';
      sendlocation(pos, map);
      realtimeweather(pos);
      handleLocationError(false, map.getCenter(), map);
      addallmarkers(map);
      clearmarkers(allstopmarkers);
      addnearmemarkers(map, pos);
    }
    // create marker clusters using array of markers
    // var markerCluster = new MarkerClusterer(map, markers, { maxZoom: 14, imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });

}

    
// google.maps.event.addDomListener(window, 'load', initMap);


//send the users location "pos" to backend function to get the address info at this location and display it on map
function sendlocation(pos, map){
    $.ajax({
        headers: {'X-CSRFToken': csrftoken},
        url: '/init',
        type: 'POST',
        data: pos,
        dataType: 'json',
        // async:false,
        success: function (data) {
                // loc_infoWindow = new google.maps.InfoWindow; //display user's location msg
            var loc_infoWindow = new google.maps.InfoWindow({
                    // position:{'lat':pos.lat, 'lng':pos.lng}
                });
            var loc_marker = new google.maps.Marker({
                    map: map,
                    position: {'lat':pos.lat, 'lng':pos.lng},
                });
            loc_infoWindow.setContent((pos.status == 'OK'? "Your position:":"(Unlocated)Map center:")+data.address)
            loc_infoWindow.open(map, loc_marker);
        },
        error: function () {return "error";alert("error");},
    });
}

//send location to backend and get weather msg from weather(request) function
function realtimeweather(pos) {
    $.ajax({
        headers: {'X-CSRFToken': csrftoken},
        url: '/weather',
        type: 'POST',
        data:pos,
        dataType: 'json',
        success: function (data) {
            var icon = data['iconUrl']
            var weather_show ="<img src='" + icon  + "'>" +data['descp'] +" "+ data['temp'];
            document.getElementById("weather").innerHTML = weather_show;
        }
    })
}

function handleLocationError(browserHasGeolocation, pos, map) {
    //supporting functions of initMap()
    alert(browserHasGeolocation ?
        'Error: The Geolocation service failed. location not accessible' :
        'Error: Your browser doesn\'t support geolocation.')
    // infoWindow = new google.maps.InfoWindow();
    // infoWindow.setPosition(pos);
    // infoWindow.setContent(browserHasGeolocation ?
    //                       'Error: The Geolocation service failed.' :
    //                       'Error: Your browser doesn\'t support geolocation.');
    // infoWindow.open(map);
}

function search() {
    //trigger relevant functions to generate directions
    //query the place according to the input boxes.
    clearmarkers(allstopmarkers);
    clearmarkers(nearmemarkers);
    if (document.getElementById('origin').value ==""){var s_origin = origin_value;}
    else{var s_origin = document.getElementById('origin').value}
    var s_dest = document.getElementById('destination').value;

    // var map2 = new google.maps.Map(document.getElementById('googleMap'), {
    //     center: origin_pos,
    //     zoom: 13
    // });
    var service = new google.maps.places.PlacesService(map);
    var s_origin_request = {
        query: s_origin,
        fields: ['name', 'geometry'],
    };
    service.findPlaceFromQuery(s_origin_request, function (results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            map.setCenter(results[0].geometry.location);
            var infowindow_ori = new google.maps.InfoWindow({
                content: s_origin,
            });
            var marker_ori = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location,
                // icon:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',

            });
            marker_ori.addListener("mouseover", function () {
                infowindow_ori.open(map, marker_ori);
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
              map.setCenter(results[0].geometry.location);
              var infowindow_dest = new google.maps.InfoWindow({
                content: s_dest,
                });
              var marker_dest = new google.maps.Marker({
                              map: map,
                              position: results[0].geometry.location,
                              // icon:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
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
    // var map3 = new google.maps.Map(document.getElementById('googleMap'),{
    //     center: origin_pos,
    //     zoom:13,
    // });
    directionsRenderer.setMap(map);
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
                document.getElementById(bus_name_str).addEventListener('click', function(){loadstops(bus_name, result['routes'][i]['bounds'], map);});

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
                        var marker = new google.maps.Marker({map:map, position:new google.maps.LatLng(data.stop_locations[i].lat, data.stop_locations[i].lng)});
                        showinfowindow(marker, data.stop_locations[i].id, map);
                        alongroutemarkers.push(marker)
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

function nearMe(ls){
    // var size = Object.keys(ls).length;
    var size = ls.length;
    var routes = new Set();
    if (size > 0){
        var msg ="<p>There are " + size + " bus stops within 5 minutes walk of your location. </p><p>Serving routes: ";
        for (var i=0; i < size; i++) {
            var buses = ls[i];
            for (var j=0; j < buses.length; j++){
                routes.add(buses[j]);
            }
        }
        routes = Array.from(routes);
        for (var k=0; k < routes.length; k++){
            msg += routes[k] + " ";
        }
        msg += "</p>"
        document.getElementById("nearme").innerHTML = msg;
    } 
}

function clearmarkers(markerlist){
    for (var i=0; i < markerlist.length; i++){
        markerlist[i].setMap(null);
    }
}
function showmarkers(markerlist, map) {
    for (var i=0; i < markerlist.length; i++){
        // alert(i)
        markerlist[i].setMap(map);
        // markerlist[i].addListener('click', (function (marker, stopKey) {
        //         return function () {getStopInfo(marker, stopKey, map);}
        //     })(marker, stopKey));
    }
}
function getStopInfo(marker, stopKey) {
    infowindow = new google.maps.InfoWindow();
    let content = "<div id='infowindow'><h5>Stop Number: " + stopdata[stopKey]["stopno"] + "</h5>";
    content += "Routes: " + stopdata[stopKey]['routes'];
    content += "</div>"

    // add content of get request to info window
    infowindow.setContent(content);
    infowindow.open(map, marker);
}

function addallmarkers(map) {
    var stopKeys = Object.keys(stopdata);
    for (var i=0;i<stopKeys.length;i++) {
        var stopKey = stopKeys[i];
        if (stopdata[stopKey]['routes'] != "") {
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(
                    stopdata[stopKey]['latitude'],
                    stopdata[stopKey]['longitude']),
            });
            marker.addListener('click', (function (marker, stopKey) {
                return function () {getStopInfo(marker, stopKey, map);}
            })(marker, stopKey));
            allstopmarkers.push(marker);
        }
    }
    showmarkers(allstopmarkers, map);
}

function addnearmemarkers(map, pos){
    var stopKeys = Object.keys(stopdata);
    var lngT = 0.005;
    var latT = 0.005;
    for (var i=0;i<stopKeys.length;i++){
        var stopKey = stopKeys[i];
        if (stopdata[stopKey]['routes'] != "" && stopdata[stopKey]['latitude'] < (pos.lat+latT) && stopdata[stopKey]['latitude'] > (pos.lat-latT) && stopdata[stopKey]['longitude'] < (pos.lng+lngT) && stopdata[stopKey]['longitude'] > (pos.lng-lngT)){
           nearMeList.push(stopdata[stopKey]['routes']);
           var marker = new google.maps.Marker({
                position: new google.maps.LatLng(
                    stopdata[stopKey]['latitude'],
                    stopdata[stopKey]['longitude']),
            });
            marker.addListener('click', (function (marker, stopKey) {
                return function () {getStopInfo(marker, stopKey, map);}
            })(marker, stopKey));
            nearmemarkers.push(marker);
        }
    }
    nearMe(nearMeList);
    showmarkers(nearmemarkers, map);
}
function stopsearch() {
    info = {csrfmiddlewaretoken: '{{ csrf_token }}', stop_id :  $('#stop_id').val()};
        // console.log(info);

        $.ajax({
            headers: {'X-CSRFToken': csrftoken},
            type:"POST",
            url: "http://127.0.0.1:8000/stop/",
            cache: false,
            dataType: "html",
            // headers:{'Content-Type':"application/json"} ,
            data:JSON.stringify($('#stop_id').val()),
            success: function(result, statues, xml){
                result = JSON.parse(result);
                console.log(result['results']);
                var real_info = "Time Table" +"<br>";
                for (var i =0; i< result["results"].length; i++){
                real_info += result["results"][i]["route"]+"        "+result["results"][i]["arrivaldatetime"] +"<br>";
                    }
                    // console.log(real_info);
                $("#stoparea").html(real_info);
            },
            error: function(){
                alert("false");
            }
        });

    var stop_id = $('#stop_id').val();
    stopKeys = Object.keys(stopdata);
    clearmarkers(alongroutemarkers);
    var marker;
    var markers = [];
    var stopKey;
    var stop_idd; //在for循环里相匹配的
    // var stopmap = new google.maps.map(document.getElementById('stopMap'));
    for (i=0;i<stopKeys.length;i++){
        stopKey = stopKeys[i]
        stop_idd = stopdata[stopKey]["stopno"];
        // console.log(stop_idd);

        if (stop_idd == stop_id){
            var stationsInfo =  "Stop_number:<h5>"+stop_idd+"<h5>";
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(
                        stopdata[stopKey]['latitude'],
                        stopdata[stopKey]['longitude']),
                    map: map,
                });

                // marker.setVisible(false);
                map.setZoom(15);
                map.panTo(marker.position);
                marker.setMap(map);

                var infowindow  = new google.maps.InfoWindow({
                        content: ""
                    });
                var pre = false;

                document.getElementById("stopbtn").addEventListener("click", function(){
                    pre.close();
                });

                google.maps.event.addListener(marker,'click', (function(marker,stationsInfo,infowindow){
                    pre = infowindow;
                    pre.setContent(stationsInfo);
                    pre.open(map, marker);

                    }) (marker,stationsInfo,infowindow));
                }
            }
    return false;
}
initMap();
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
var destination_pos = {}//represent the destination position, lat, lng
// var origin_value = ""; //the text in the input box with id "origin"

var map;
var nearMeList = [];
var allstopmarkers = [];
var nearmemarkers = [];
var alongroutemarkers = [];
var originmarkers = [];
var destinationmarkers = [];
var directionsService = new google.maps.DirectionsService();
var directionsRenderer = new google.maps.DirectionsRenderer();
var singlestopmarker = [];
var directionresults = [];

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
        error: function () {alert("error"+" failed js function:sendlocation"+" involved views.py function:init(request)");},
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

//deal with the geolocation error
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

//trigger relevant functions to generate directions
// function search() {
//     clearmarkers(allstopmarkers);
//     clearmarkers(nearmemarkers);
//     //query the place according to the input boxes.
//     if ($("#origin").val() == "" || $("#destination").val() == "") {alert('The "from" or "to" box cannot be empty')}
//     else {
//         var s_origin = document.getElementById('origin').value
//         var s_dest = document.getElementById('destination').value;
//
//         var service = new google.maps.places.PlacesService(map);
//
//         //search the location of origin input
//         var s_origin_request = {
//             query: s_origin,
//             fields: ['name', 'geometry'],
//         };
//         service.findPlaceFromQuery(s_origin_request, function (results, status) {
//             if (status === google.maps.places.PlacesServiceStatus.OK) {
//                 map.setCenter(results[0].geometry.location);
//                 var infowindow_ori = new google.maps.InfoWindow({
//                     content: s_origin,
//                 });
//                 var marker_ori = new google.maps.Marker({
//                     map: map,
//                     position: results[0].geometry.location,
//                     icon:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
//
//                 });
//                 marker_ori.addListener("mouseover", function () {infowindow_ori.open(map, marker_ori);});
//                 marker_ori.addListener("mouseout", function () {infowindow_ori.close(map, marker_ori);});
//                 origin_pos = results[0].geometry.location;
//                 ori_dest_markers.push(marker_ori);
//                 // origin_pos = {'lat': results[0].geometry.location.lat(), 'lng': results[0].geometry.location.lng()}
//             }
//         });
//
//         //search the location of destination input
//         var s_dest_request = {
//             query: s_dest,
//             fields: ['name', 'geometry'],
//         };
//         service.findPlaceFromQuery(s_dest_request, function (results, status) {
//             if (status === google.maps.places.PlacesServiceStatus.OK) {
//                 // map.setCenter(results[0].geometry.location);
//                 var infowindow_dest = new google.maps.InfoWindow({
//                     content: s_dest,
//                 });
//                 var marker_dest = new google.maps.Marker({
//                     map: map,
//                     position: results[0].geometry.location,
//                     icon:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
//                 });
//                 marker_dest.addListener("mouseover", function () {infowindow_dest.open(map, marker_dest);});
//                 marker_dest.addListener("mouseout", function () {infowindow_dest.close(map, marker_dest);});
//                 destination_pos = {'lat': results[0].geometry.location.lat(), 'lng': results[0].geometry.location.lng()};
//                 ori_dest_markers.push(marker_dest);
//             }
//         });
//     }
// }

function calcRoute() {
    directionsRenderer.setMap(null);
    clearmarkers(alongroutemarkers);
    alongroutemarkers = [];
    clearmarkers(nearmemarkers);
      var request = {
        origin: {query: document.getElementById('origin').value},
        destination: {query: document.getElementById('destination').value},
        travelMode: 'TRANSIT',
        transitOptions:{departureTime: new Date(document.getElementById("datetimepicker1").value)},
        provideRouteAlternatives: false,
      };
    directionsRenderer.setMap(map);
    directionsService.route(request, function(result, status) {
    if (status == 'OK') {
        directionresults = [result];
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
                for (k in steps){
                    if (steps[k].travel_mode == 'WALKING'){walking_dur += steps[k]['duration'].value}
                    else if (steps[k].travel_mode == 'TRANSIT'){bus_dur += steps[k]['duration'].value; bus_name.push(steps[k]['transit']['line'].short_name)}
                }
                if (bus_name.length > 1){for (var i in bus_name){bus_name_str += bus_name[i] + "->"}}
                else{bus_name_str = bus_name[0]};
                routes_dict[bus_name_str] = result['routes'][i];
                document.getElementById('routes').innerHTML = "<button id="+"showalongroutemarker>"+bus_name_str+"</button>" + "walk:" + walking_dur + "s, on bus:"+ bus_dur+"s<br>";
                loadstops(bus_name, result['routes'][i]['bounds'], map);
                document.getElementById("showalongroutemarker").addEventListener('click', function(){changemarkerstatus(alongroutemarkers, map)});

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
        function loadstops(bus_name, bounds, map) {
            if (alongroutemarkers.length !== 0) {
                showmarkers(alongroutemarkers, map)
            } else {
                post_data = {'bus': bus_name, 'bounds': bounds}
                $.ajax({
                    headers: {'X-CSRFToken': csrftoken},
                    url: '/printresult',
                    data: JSON.stringify(post_data),
                    type: 'POST',
                    dataType: 'json',
                    success: function (data) {
                        // alongroutemarkers = [];
                        for (var i = 0; i < data.stop_locations.length; i++) {
                            var marker = new google.maps.Marker({
                                // map: map,
                                position: new google.maps.LatLng(data.stop_locations[i].lat, data.stop_locations[i].lng)
                            });
                            showinfowindow(marker, data.stop_locations[i].id, map);
                            alongroutemarkers.push(marker);
                            // showmarkers(alongroutemarkers, map);
                        }
                    }, error: function () {
                        alert('error'+" involved js function loadstops(bus_name, bounds, map) serving function calcRoute()"+" involved views.py function printresult(request)");
                    },
                });
            }
        }
      directionsRenderer.setDirections(result);
    }
  });
   directionsRenderer.setPanel(document.getElementById('h51'));
}

//Find the nearme stops and generate a msg to describe them.
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

//To make the markers in a list invisible.
function clearmarkers(markerlist){
    for (var i=0; i < markerlist.length; i++){
        markerlist[i].setMap(null);
    }
}

//To make the markers in a list visible.
function showmarkers(markerlist, map) {
    for (var i=0; i < markerlist.length; i++){
        markerlist[i].setMap(map);
    }
}

//triggered by clicking the markers to show stop info.
function getStopInfo(marker, stopKey) {
    infowindow = new google.maps.InfoWindow();
    let content = "<div id='infowindow'><h5>Stop Number: " + stopdata[stopKey]["stopno"] + "</h5>";
    content += "Routes: " + stopdata[stopKey]['routes'];
    content += "</div>"

    // add content of get request to info window
    infowindow.setContent(content);
    infowindow.open(map, marker);
}

//Add all stops markers on the map.
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

//Add the markers of nearme stops and display them on map
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

// The function to search a single stopid in the map and display the time info.
function stopsearch() {
    directionsRenderer.setMap(null);
    clearmarkers(alongroutemarkers);
    clearmarkers(nearmemarkers);
    clearmarkers(singlestopmarker);
        $.ajax({
            headers: {'X-CSRFToken': csrftoken},
            type:"POST",
            url: "/stop/",
            cache: false,
            dataType: "json",
            data:{'stop_id':$('#stop_id').val()},
            success: function(result, statues, xml){
                var real_info = "Time Table" +"<br>";
                for (var i =0; i< result["results"].length; i++){
                    real_info += result["results"][i]["route"]+"        "+result["results"][i]["arrivaldatetime"] +"<br>";
                }
                $("#stoparea").html(real_info);
            },
            error: function(){
                alert("false"+" involved js function stopsearch() involved views.py function stop(request)");
            }
        });
    var stop_id = $('#stop_id').val();
    stopKeys = Object.keys(stopdata);

    var stopKey;
    var stop_idd; //在for循环里相匹配的
    // var stopmap = new google.maps.map(document.getElementById('stopMap'));
    for (i=0;i<stopKeys.length;i++){
        stopKey = stopKeys[i]
        stop_idd = stopdata[stopKey]["stopno"];
        // console.log(stop_idd);

        if (stop_idd == stop_id){
            var stationsInfo =  "Stop_number:<h5>"+stop_idd+"<h5>";
                var marker = new google.maps.Marker({
                    position: new google.maps.LatLng(
                        stopdata[stopKey]['latitude'],
                        stopdata[stopKey]['longitude']),
                    map: map,
                });

                // marker.setVisible(false);
                map.setZoom(15);
                map.panTo(marker.position);
                // marker.setMap(map);
                singlestopmarker = [marker];
                // singlestopmarker.push(marker);
                showmarkers(singlestopmarker, map);

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

//triggered by clicking "Search" button to show current searching result if it is made invisible.
function showsearchcontent(){
    directionsRenderer.setDirections(directionresults[0]);
    directionsRenderer.setMap(map);
    directionsRenderer.setPanel(document.getElementById('h51'));
}

//triggered by clicking "Stop" button to show current searching result if it is made invisible.
function showstopsearchcontent(){
    showmarkers(singlestopmarker, map);
}

//change the markers to be visible from being invisible or reversely.
function changemarkerstatus(markerlist, map){
    for (var i=0; i<markerlist.length; i++){
        if (markerlist[i].map){markerlist[i].setMap(null);}
        else{markerlist[i].setMap(map)}
    }
}

//get the clicking point location on map
function select_ori_dest(id){
    if (id == "origin"){
        $("#origin").val(null); //clear the input box
        clearmarkers(originmarkers); //clear previous marker
    }
    else{
        $("#destination").val(null);
        clearmarkers(destinationmarkers);
        // destinationmarkers=[];
    }
    google.maps.event.addListener(map, 'click', function(event) {
        if (originmarkers.length > 1) {
            clearmarkers(originmarkers);
            originmarkers = [];
        }// do not allow multiple origin markers appear
        if (destinationmarkers.length > 1) {
            clearmarkers(destinationmarkers);
            destinationmarkers = [];
        }

        getclicklocation(event.latLng);
    })
}
//supportinh function to get event location for function select_ori_dest(id)
function getclicklocation(latLng){
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({'location': latLng}, function(responses, status) {
        if (status === 'OK') {
            var address = responses[0].formatted_address;
            var loc_infoWindow = new google.maps.InfoWindow({});
            var loc_marker = new google.maps.Marker({
                // map: map,
                position: latLng,
                draggable: true,
                animation: google.maps.Animation.DROP,
            });
            loc_infoWindow.setContent(
                "<h5 id='address'>" + address + "</h5>" + "<br>" +
                "<button id='ori-sel'>" + "As Origin" + "</button>" +
                "<button id='dest-sel'>" + "As Destination" + "</button>"
            )
            loc_infoWindow.open(map, loc_marker);
            showmarkers([loc_marker], map);

            //enable user to chose this address as origin or destination
            $(document).on('click', "#ori-sel", function () {
                clearmarkers(originmarkers);
                loc_marker.setMap(null);
                var ori_infowindow = new google.maps.InfoWindow();
                ori_infowindow.setContent("<h5 id='ori-address'>" + "Origin:" + address + "</h5>");
                var orimarker = new google.maps.Marker({
                    position: latLng,
                    draggable: true,
                    animation: google.maps.Animation.DROP,
                });
                ori_infowindow.open(map, orimarker);
                google.maps.event.addListener(orimarker, 'dragend', function (event) {
                    geocoder.geocode({'location': event.latLng}, function (Resp, status) {
                        orimarker.setPosition(event.latLng);
                        address = Resp[0].formatted_address;
                        ori_infowindow.setContent("<h5 id='ori-address'>" + "Origin:" + address + "</h5>");
                        originmarkers = [];
                        originmarkers.push(orimarker);
                        showmarkers(originmarkers, map);
                        $("#origin").val(address);
                    })
                })
                originmarkers = [];
                originmarkers.push(orimarker);
                showmarkers(originmarkers, map);
                $("#origin").val(address);
                // $("#dest-sel").hide();
            });
            $(document).on("click", "#dest-sel", function () {
                clearmarkers(destinationmarkers);
                loc_marker.setMap(null);
                var dest_infowindow = new google.maps.InfoWindow();
                dest_infowindow.setContent("<h5 id='dest-address'>" + "Destination:" + address + "</h5>");
                var destmarker = new google.maps.Marker({
                    position: latLng,
                    draggable: true,
                    animation: google.maps.Animation.DROP,
                });
                dest_infowindow.open(map, destmarker);
                google.maps.event.addListener(destmarker, 'dragend', function (event) {
                    geocoder.geocode({'location': event.latLng}, function (Resp, status) {
                        destmarker.setPosition(event.latLng);
                        address = Resp[0].formatted_address;
                        dest_infowindow.setContent("<h5 id='dest-address'>" + "Destination:" + address + "</h5>");
                        destinationmarkers = [];
                        destinationmarkers.push(destmarker);
                        showmarkers(destinationmarkers, map);
                        $("#destination").val(address);
                    })
                })
                destinationmarkers = [];
                destinationmarkers.push(destmarker);
                showmarkers(destinationmarkers, map)
                $("#destination").val(address);
            });
        }
    })
}

<<<<<<< Updated upstream


    //     $.ajax({
    //     headers: {'X-CSRFToken': csrftoken},
    //     url: '/init',
    //     type: 'POST',
    //     data: {'lat':Latitude, 'lng':Longitude},
    //     dataType: 'json',
    //     // async:false,
    //     success: function (data) {
    //         //get the address msg of clicking location
    //         var loc_infoWindow = new google.maps.InfoWindow({});
    //         var loc_marker = new google.maps.Marker({
    //                 // map: map,
    //                 position: {'lat':Latitude, 'lng':Longitude},
    //                 draggable:true,
    //                 animation: google.maps.Animation.DROP,
    //             });
    //         loc_infoWindow.setContent(
    //             "<h5 id='address'>"+data.address+"</h5>"+"<br>"+
    //             "<button id='ori-sel'>"+"As Origin"+"</button>"+
    //             "<button id='dest-sel'>"+"As Destination"+"</button>"
    //         )
    //         loc_infoWindow.open(map, loc_marker);
    //         showmarkers([loc_marker], map);
    //
    //         //enable user to chose this address as origin or destination
    //         $(document).on('click', "#ori-sel", function () {
    //             clearmarkers(originmarkers);
    //             loc_marker.setMap(null);
    //             var ori_infowindow = new google.maps.InfoWindow();
    //             ori_infowindow.setContent("<h5 id='ori-address'>"+"Origin:"+data.address+"</h5>");
    //             var orimarker = new google.maps.Marker({
    //                     position: {'lat':Latitude, 'lng':Longitude},
    //                     draggable:true,
    //                     animation: google.maps.Animation.DROP,
    //                 });
    //             ori_infowindow.open(map, orimarker);
    //             google.maps.event.addListener(orimarker, 'dragend', function (event) {
    //                 orimarker.setPosition(event.latLng);
    //                 var address =
    //                 ori_infowindow.setContent("<h5 id='ori-address'>"+"Origin:"+data.address+"</h5>");
    //             })
    //             originmarkers = [];
    //             originmarkers.push(orimarker);
    //             showmarkers(originmarkers, map);
    //             $("#origin").val(data.address);
    //             // $("#dest-sel").hide();
    //         });
    //         $(document).on("click", "#dest-sel", function () {
    //             clearmarkers(destinationmarkers);
    //             loc_marker.setMap(null);
    //             var dest_infowindow = new google.maps.InfoWindow();
    //             dest_infowindow.setContent("<h5 id='dest-address'>"+"Destination:"+data.address+"</h5>");
    //             var destmarker = new google.maps.Marker({
    //                     position: {'lat':Latitude, 'lng':Longitude},
    //                     draggable:true,
    //                     animation: google.maps.Animation.DROP,
    //                 });
    //             dest_infowindow.open(map, destmarker);
    //             destinationmarkers = [];
    //             destinationmarkers.push(destmarker);
    //             showmarkers(destinationmarkers, map)
    //             $("#destination").val(data.address);
    //         });
    //     },
    //     error: function () {return "error";alert("error");},
    // });
// initMap();
=======
//To calculate the estimated fare of the journey 
function calcFare(fareRoutes){
    var leapFare = 0;
    var cashFare = 0;
    for (var i=0; i < fareRoutes.length; i++){
        if (fareRoutes[i] > 1 && fareRoutes[i] < 4){
            leapFare += 1.55;
            cashFare += 2.15;
        } else if (fareRoutes[i] > 3 && fareRoutes[i] < 14){
            leapFare += 2.25;
            cashFare += 3.00;
        } else if (fareRoutes[i] > 13){
            leapFare += 2.50;
            cashFare += 3.30;
        }
            
    }
    if (leapFare > 7){
        // Accounting for leap card capping 
        leapFare = 7;
    }

    //Makes sure price is rounded to 2 decimal places
    leapFare = leapFare.toFixed(2);
    cashFare = cashFare.toFixed(2);

    var fares = "<p><b>Estimated Adult Fares:</b><br>Leap: €" + leapFare + "<br>Cash: €" + cashFare + "</p>";
    document.getElementById("fares").innerHTML = fares;
}
>>>>>>> Stashed changes

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
var segmentsinfo = [];
var fareRoutes = [];

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

function calcRoute() {
    directionsRenderer.setMap(null);
    clearmarkers(alongroutemarkers);
    alongroutemarkers = [];
    clearmarkers(nearmemarkers);
    segmentsinfo = [];
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
        // var route_choices = {}
        var routes_list = result['routes'];
        for (var i in routes_list){
            var bounds = result['routes'][0]['bounds']
            var ROUTE = routes_list[i];
            var legs = ROUTE['legs'];
            for (j in legs){
                var LEG = legs[j];
                var walking_dur = 0;
                var bus_dur = 0;
                var bus_name = [];
                var bus_name_str = '';
                var steps = LEG['steps'];
                var fareStops = [];
                for (k in steps){
                    if (steps[k].travel_mode == 'WALKING'){walking_dur += steps[k]['duration'].value}
                    else if (steps[k].travel_mode == 'TRANSIT'){
                        bus_dur += steps[k]['duration'].value;
                        // alert(steps[k]['transit'])
                        bus_name.push(steps[k]['transit']['line'].short_name);
                        var seg = {
                            'travelmode':steps[k].travel_mode,
                            'busname':steps[k]['transit']['line'].short_name,
                            'startstopname':steps[k]['transit']['departure_stop'].name,
                            'startstoplocation': steps[k]['transit']['departure_stop']['location'],
                            'endstopname':steps[k]['transit']['arrival_stop'].name,
                            'endstoplocation': steps[k]['transit']['arrival_stop']['location'],
                            'headsign': steps[k]['transit']['headsign'],
                            'numstops':steps[k]['transit'].num_stops,
                            'agency':steps[k]['transit']['line']['agencies'][0]['name'],
                            'traveltime':steps[k]['duration'].value,
                            'instructions':steps[k]['instructions']
                        }
                        segmentsinfo.push(seg)

                        //adding number of stops on route(s) to array for calcFare function
                        fareStops.push(steps[k]['transit']['num_stops']);
                    }
                }
                showPrediction(segmentsinfo);
                
                // if entered route requires transit, call calcFare function 
                if (fareStops.length > 0){
                    //adding array to array to calc individual routes 
                    fareRoutes.push(fareStops);
                    calcFare(fareRoutes);
                }

                for (var p in bus_name){bus_name_str += (p == 0? bus_name[p]:"->"+bus_name[p])}
                routes_dict[bus_name_str] = {'route':ROUTE, "busnames":bus_name};

                //convert to mins for readability 
                walk_time = Math.round(walking_dur/60);
                bus_time = Math.round(bus_dur/60);

                document.getElementById('routes').innerHTML = "<button id="+"showalongroutemarker>"+bus_name_str+"</button>" + "<p style='color: white;'><b>Estimated Travel Time: </b><br>Walking: " + walk_time + " minutes<br>Transit: "+ bus_time +" minutes</p>";
                loadstops(segmentsinfo, bounds, map);
                // $(document).on('click', "#showalongroutemarker", function () {showmarkers(alongroutemarkers, map)});
                document.getElementById("showalongroutemarker").addEventListener('click', function(){showmarkers(alongroutemarkers, map)});
            }
        }
        function showinfowindow(marker, map){
            var id = marker.getTitle();
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
                    // infowindow.open(marker, map)
                    marker.addListener('click', function(){infowindow.open(map,marker)})
                    // marker.addListener('mouseover', function(){infowindow.open(map,marker)})
                    // marker.addListener('mouseout', function(){infowindow.close(map,marker)})
                }
            })
        }
        function loadstops(segmentsinfo,  bounds, map) {
            if (alongroutemarkers.length !== 0) {
                showmarkers(alongroutemarkers, map)
            } else {
                // var post_data = {'segmentsinfo': segmentsinfo, 'bounds': bounds}
                $.ajax({
                    headers: {'X-CSRFToken': csrftoken},
                    url: '/printresult',
                    // data: post_data,
                    data: JSON.stringify([segmentsinfo, bounds]),
                    type: 'POST',
                    dataType: 'json',
                    success: function (data) {
                        for (key in data){
                            var stops = data[key];
                            for (var i=0; i<stops.length; i++) {
                                var stop = stops[i];
                                var id = stop.id;
                                var lat = stop.lat;
                                var lng = stop.lng;
                                var Marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(lat, lng),
                                    title: id,
                                    icon:"https://img.icons8.com/android/24/000000/bus.png"
                                });
                                // Marker.addListener('click', showinfowindow(Marker, map));
                                // google.maps.event.addListener(Marker, 'click', showinfowindow(Marker, map));
                                showinfowindow(Marker, map);
                                alongroutemarkers.push(Marker);
                            }
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
                title: stopdata[stopKey]['stopno'],
                label: stopKey,
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

//supporting function to get event location for function select_ori_dest(id)
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
// initMap();

//To calculate the estimated fare of the journey 
function calcFare(fareRoutes){
    var leapFare = 0;
    var cashFare = 0;
    var journey = fareRoutes[fareRoutes.length - 1];
    for (var i=0; i < journey.length; i++){
        if (journey[i] > 1 && journey[i] < 4){
            leapFare += 1.55;
            cashFare += 2.15;
        } else if (journey[i] > 3 && journey[i] < 14){
            leapFare += 2.25;
            cashFare += 3.00;
        } else if (journey[i] > 13){
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

    var fares = "<p style='color: white;'><b>Estimated Adult Fares:</b><br>Leap: €" + leapFare + "<br>Cash: €" + cashFare + "</p>";
    document.getElementById("fares").innerHTML = fares;
}

//send starts, ends in different segments to backend
function showPrediction(segmentsinfo){
    // Add nearest stopmarkers to segmentsinfo
    for (var i=0; i<segmentsinfo.length; i++) {
        if (segmentsinfo[i].travelmode == 'TRANSIT') {
            segmentsinfo[i]['startstopno'] = find_closest_stopmarker(segmentsinfo[i]["startstoplocation"],segmentsinfo[i]['busname']);
            segmentsinfo[i]['endstopno'] = find_closest_stopmarker(segmentsinfo[i]["endstoplocation"],segmentsinfo[i]['busname']);
        }
    }



    // "segmentsinfo" variable is a list declared at the line 34 of this script. and it is fed in the function "calcRoute()" just following the a dictionary variable "seg"
    $.ajax({
        headers: {'X-CSRFToken': csrftoken}, //just for security issue
        url: '/showprediction', //correspond to a route in urls.py and the function "showprediction(request)" in views.py will be triggered
        data: JSON.stringify(segmentsinfo), // the data that will be post to backend. if the data is not a dictionary, should use JSON.stringfy(segs)
        type: 'POST', // could be 'POST' or 'GET'
        dataType: 'json',// declare the type of sent data
        success: function (data) {
            // if the correspond function in backend given response successfully, this function is triggered and parameter "data" is the responded data.
            var no_predictions = 0;
            for (i in segmentsinfo) {
                if (segmentsinfo[i].travelmode == 'TRANSIT') {
                    segmentsinfo[i]['traveltime'] = data.prediction[no_predictions];
                    np_predictions = 0;
                }
            }
            displayDirections(segmentsinfo,data);
        }, error: function () {
            // if the correspond function in backend geives response successfully, this function is triggered and parameter "data" is the responded data.
            alert('error'+" involved js function showPrediction(segs) "+" involved views.py function showprediction(request)");
        },
    });
}
function find_closest_stopmarker(location,route) {
    // Finds nearest stopmarker to a given LatLng which  a given route in its route array
    var distances = [];
    var closest = -1;
    for (i = 0; i < allstopmarkers.length; i++) {
        var d = google.maps.geometry.spherical.computeDistanceBetween(allstopmarkers[i].position, location);
        distances[i] = d;
        if (closest == -1 || d < distances[closest] && stopdata[allstopmarkers[i].getLabel()].routes.includes(route)) {
            closest = i;
        }
    }
    return allstopmarkers[closest].getTitle();
  }

function displayDirections(segmentsinfo,data) {
    var number_buses = 0;
    for (i in segmentsinfo) {
        if (segmentsinfo[i].agency == "Dublin Bus" || segmentsinfo[i].agency == "Go-Ahead"){
            // alert(segmentsinfo[i].predictedtraveltime)
        }
        else {
            // alert(segmentsinfo[i].traveltime);
        }
    }
    renderTravelPlan(segmentsinfo);
}

function renderTravelPlan(segmentsinfo) {
    var totaltraveltime = 0;
    document.getElementById('directions-body').innerHTML = '';
    for (i in segmentsinfo) {
        renderLegCard(segmentsinfo[i]);
        totaltraveltime += segmentsinfo[i].traveltime;
    }
    document.getElementById('directions-body').innerHTML = '<span style="font-variant: small-caps;">Arrival in: </span><span style="font-size:large; font-weight:bold;">' + Math.round(totaltraveltime/60) + ' minutes</span>' +  document.getElementById('directions-body').innerHTML;
}

function renderLegCard(seg) {
    var time = Math.round(seg.traveltime/60);
    var busname = '';

    var html_out = '<div class="card flex-row flex-wrap" style="margin-bottom:5px; margin-top:5px; "><table style="border-spacing: 10px;border-collapse: separate;"><tr>';
    if (seg.travelmode == 'WALKING') {
        html_out += '<td><img src="../static/images/icon-WALKING.png" alt="" style="width: 50px;"></td>';
    } else if (seg.agency == "Dublin Bus" || seg.agency == "Go-Ahead"){
        html_out += '<td><img src="../static/images/icon-BUS.png" alt="" style="width: 50px;"></td>';
        busname = '(' + seg.busname + ')';
    } else {
        html_out += '<td><img src="../static/images/icon-TRAIN.png" alt="" style="width: 50px;"></td>';
    }
    html_out += '<td><h4 class="card-title" style="color: black;">' + time + ' minutes ' + '</h4>';
    html_out += '<p class="card-text">' + seg.instructions  + busname + '</p></td>';
    html_out += '</tr></table>';
    document.getElementById('directions-body').innerHTML += html_out;
}
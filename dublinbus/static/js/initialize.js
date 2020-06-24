// var myCenter=new google.maps.LatLng(53.350140, -6.266155);
//     var map;
//     var mapProp;
// function initialize() {
//     mapProp = {
//         center: new google.maps.LatLng(53.350140, -6.266155),
//         zoom: 13,
//         mapTypeId: google.maps.MapTypeId.ROADMAP
//     };
//     map=new google.maps.Map(document.getElementById("googleMap"), mapProp);
// }
// google.maps.event.addDomListener(window, 'load', initialize);


    // map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

var infowindow;
var map;

function initialize() {
        var mapProp = {
            center: new google.maps.LatLng(53.350140, -6.266155),
            zoom: 13,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        
        map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

        infowindow = new google.maps.InfoWindow();

        stopKeys = Object.keys(stopdata);

        // Add stop markers with onclick
        var marker;
        var markers = [];
        var stopKey;
        for (i=0;i<stopKeys.length;i++) {
            stopKey = stopKeys[i]
            if (stopdata[stopKey]['routes'] != "") {
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(
                        stopdata[stopKey]['latitude'], 
                        stopdata[stopKey]['longitude']),
                    map: map
                });
                markers.push(marker);
                marker.addListener('click', (function (marker, stopKey) {
                    return function () {
                        getStopInfo(marker, stopKey)
                                    }
                })(marker, stopKey));
            }
        }

        marker.setMap(map);
        // create marker clusters using array of markers
        var markerCluster = new MarkerClusterer(map, markers, { maxZoom: 14, imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });
    };
    google.maps.event.addDomListener(window, 'load', initialize);

function getStopInfo(marker, stopKey) {
    let content = "<div id='infowindow'><h5>Stop ID: " + stopdata[stopKey]["id"] + "</h5>";
    content += "Routes: " + stopdata[stopKey]['routes'];
    content += "</div>"

    // add content of get request to info window
    infowindow.setContent(content);
    infowindow.open(map, marker);
}
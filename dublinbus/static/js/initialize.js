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



function initialize() {
        var mapProp = {
            center: new google.maps.LatLng(53.350140, -6.266155),
            zoom: 13,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        
        var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

        stopKeys = Object.keys(stopdata);
        console.log(stopdata);

        var marker;
        for (i=0;i<stopKeys.length;i++) {
            marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(
                                        stopdata[stopKeys[i]]['latitude'], 
                                        stopdata[stopKeys[i]]['longitude']),
                                    map: map
                                });
        }
        
        marker.setMap(map);
    };
    google.maps.event.addDomListener(window, 'load', initialize);
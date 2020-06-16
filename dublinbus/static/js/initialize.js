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
    }
    google.maps.event.addDomListener(window, 'load', initialize);
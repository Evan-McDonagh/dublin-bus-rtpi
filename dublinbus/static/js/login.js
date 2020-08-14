$(document).ready(function () {
    // $("#alertinfo").hide();
    // alert($("#alertinfo").val());
    if ($("#alertinfo").val() != "") {
        window.confirm("Registered Successfully!\nNow please login your own account")
    }
    if ($("#loginerrmsg").val() != "") {
        window.confirm($("#loginerrmsg").val())
    }
    // else if ($("#alertinfo").val() == null){alert(null)}
})
// $("#loginerrmsg").change(function () {
//     alert('asdf')
//     if ($("#loginerrmsg").val() == "username does not match password") {
//         window.confirm($("#loginerrmsg").val())
//     }
//     else {$("#loginerrmsg").show()}
// })
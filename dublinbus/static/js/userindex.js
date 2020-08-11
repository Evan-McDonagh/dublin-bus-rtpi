function clicktoaddfav() {
    // when user click the star, and stop they input will be added to the favorite
    $('.star').click(function (e) {
        e.preventDefault;
        if (document.getElementById("stop_id").value === "") {
            alert('please input stop')
        } else {
            addfav('stop', $("#userindexun").val(), $("#stop_id").val());
        }
    })

    // add favorite route
    $('.route').click(function (e) {
        e.preventDefault;
        if (document.getElementById("route_id").value === "") {
            alert('please input route')
        } else {
            addfav('route', $("#userindexun").val(), $("#route_id").val())
        }
    });

    // add favorite place
    $('.place').click(function (e) {
        e.preventDefault;
        if ($('#origin').val() === "") {
            alert('please input place')
        } else {
            addfav('place', $("#userindexun").val(), $('#origin').val());
        }
    });

    //show favorite stop and remove favorite stop
    $("#mystop").click(function(e){
        $("#favoritearea").html("");
        var tableContent = document.createElement("div");
        var stopArr = getfav('stop', $("#userindexun").val());
        document.body.appendChild(tableContent);

        for (let i = 0; i<stopArr.length; i++){
            let stop = stopArr[i];

            var wrapper = document.createElement("div");
            wrapper.className = "favs-wrapper";

            var stop_elem = document.createElement("span");
            var t = document.createTextNode(stop);
            stop_elem.appendChild(t);

            var iconstar = document.createElement("a");
            iconstar.innerHTML = "&times;";
            iconstar.className = 'rmicon-stop';
            iconstar.id = stopArr[i]

            wrapper.appendChild(stop_elem);
            wrapper.appendChild(iconstar);

            tableContent.appendChild(wrapper);

            document.getElementById("favorite").appendChild(tableContent);

        };
        $("#favoritearea").html(tableContent);
        var rmicons = $(".rmicon-stop");
        for (var i=0; i<rmicons.length; i++){
            rmicons[i].onclick=function () {
                delfav('stop', $("#userindexun").val(), $(this).attr('id'));
                $(this).parent('div').remove();
            }
        }
    });

    //show favorite place and remove favorite place
    $("#myplace").click(function(e){
        $("#favoritearea").html("");
        var tableContent = document.createElement("div");
        var placeArr = getfav('place', $("#userindexun").val());;
        document.body.appendChild(tableContent);

        for (let i = 0; i<placeArr.length; i++){
            let place = placeArr[i];

            //Creating wrapper div for each fav
            var wrapper = document.createElement("div");
            wrapper.className = "favs-wrapper";

            var place_elem = document.createElement("span");
            var t = document.createTextNode(place);
            place_elem.appendChild(t);

            var iconstar = document.createElement("a");
            iconstar.innerHTML = "&times;";
            iconstar.className = 'rmicon-place';
            iconstar.id = placeArr[i]

            wrapper.appendChild(place_elem);
            wrapper.appendChild(iconstar);

            tableContent.appendChild(wrapper);
            document.getElementById("favorite").appendChild(tableContent);
        }
        $("#favoritearea").html(tableContent);
            var rmicons = $(".rmicon-place");
            for (var i=0; i<rmicons.length; i++){
                rmicons[i].onclick=function () {
                    delfav('place', $("#userindexun").val(), $(this).attr('id'));
                    $(this).parent('div').remove();
                }
            }
        });

    //show favorite route and remove favorite route
    $("#myroute").click(function(e){
            $("#favoritearea").html("");
            var tableContent = document.createElement("div");
            var routeArr = getfav('route', $("#userindexun").val());
            document.body.appendChild(tableContent);

            for (let i = 0; i<routeArr.length; i++){
                let route = routeArr[i];

                var wrapper = document.createElement("div");
                wrapper.className = "favs-wrapper";

                var route_elem = document.createElement("span");
                var t = document.createTextNode(route);
                route_elem.appendChild(t);

                var iconstar = document.createElement("a");
                iconstar.innerHTML = "&times;";
                iconstar.className = 'rmicon-route';
                iconstar.id = routeArr[i]

                wrapper.appendChild(route_elem);
                wrapper.appendChild(iconstar);

                tableContent.appendChild(wrapper);

                document.getElementById("favorite").appendChild(tableContent);
            }

            $("#favoritearea").html(tableContent);
            var rmicons = $(".rmicon-route");
            for (var i=0; i<rmicons.length; i++){
                rmicons[i].onclick=function () {
                    delfav('route', $("#userindexun").val(), $(this).attr('id'));
                    $(this).parent('div').remove();
                }
            }
            });



}
window.addEventListener('load', function (){clicktoaddfav()}, false)


function showuserinfowindow() {
    var username = $("#userindexun").val();
    // alert(username);
    $.ajax({
        headers: {'X-CSRFToken': csrftoken},
        url:'/user_manage/showuserinfowindow/',
        type:"POST",
        dataType: 'json',
        data:{'username':username},
        async:false,
        success: function (data) {
            if (data.hasOwnProperty('msg')){alert(data['msg'])}
            else{
                const burger = document.querySelector('.burger');
                const modal = document.querySelector('.modal');

                //Toggle nav
                modal.classList.toggle('modal-active');
                //Animation for burger
                burger.classList.toggle('toggle');

                var places = data['places'];
                var placecontent = makecontent(places, 'search');
                document.getElementById("placecontent").innerHTML='';
                document.getElementById("placecontent").appendChild(placecontent);
                bindclick('search', 'origin');

                var stops = data["stops"];
                var stopcontent = makecontent(stops, 'stop');
                document.getElementById("stopcontent").innerHTML='';
                document.getElementById("stopcontent").appendChild(stopcontent);
                bindclick('stop', 'stop_id');

                var routes = data["routes"];
                var routecontent = makecontent(routes, 'route');
                document.getElementById('routecontent').innerHTML='';
                document.getElementById('routecontent').appendChild(routecontent);
                bindclick('route', 'route_id')
            }
        },
        // {#error: function () {alert('failed')}#}
    })
    if ($("#userinfowindow").is(":hidden")) {$("#userinfowindow").show();}
    else{$("#userinfowindow").hide();}
}

function makecontent(elementlist, clickele) {
    var ul = document.createElement('ul')
    for (var i in elementlist) {
        var ele = elementlist[i];
        var li = document.createElement('li');
        var input = document.createElement('input');
            input.type = 'button';
            input.id = ele;
            input.value = ele;
            input.className = 'content' + clickele;
        li.appendChild(input);

        var button = document.createElement('button');
            button.id = ele + "rm";
        var img = document.createElement('img');
            img.src = 'https://img.icons8.com/material/24/000000/delete-forever--v2.png'
        button.appendChild(img);

        li.appendChild(button);
        ul.appendChild(li)
    }
    alert(ul.innerHTML)
    return ul;
}

function bindclick(clickele, fillinele){
    var contents = document.getElementsByClassName('content'+clickele);
    var length = document.getElementsByClassName('content'+clickele).length;
    // alert(contents)
    // alert(length)
    for (var i=0; i<length; i++){
        contents[i].onclick=function () {
            // alert($(this).val());
            $("#"+clickele).click();
            $('#'+fillinele).val($(this).val());
        }
    }
}

function addfav(choice, username, content) {
    $.ajax({
        headers: {'X-CSRFToken': csrftoken},
        url:'/user_manage/addfav/',
        type:"POST",
        dataType: 'json',
        data:{'choice':choice, 'username':username, 'content': content},
        async:false,
        success: function (data) {alert(data.msg)},
        error: function () {alert('add favorite'+choice+'failed')}
    })
}

function getfav(choice, username){
    var gainedcontent = []
    $.ajax({
        headers: {'X-CSRFToken': csrftoken},
        url:'/user_manage/getfav/',
        type:"POST",
        dataType: 'json',
        data:{'choice':choice, 'username':username},
        async:false,
        success: function (data) {
            if (data.hasOwnProperty('msg')){alert(data['msg'])}
            else{gainedcontent=data['content'];}
            },
        error: function () {alert('get favorite'+choice+'failed')}
    })
    alert(gainedcontent)
    return gainedcontent;
}


function delfav(choice, username, content){
    $.ajax({
        headers: {'X-CSRFToken': csrftoken},
        url:'/user_manage/delfav/',
        type:"POST",
        dataType: 'json',
        data:{'choice':choice, 'username':username, 'content':content},
        async:false,
        success: function (data) {alert(data['msg'])},
        error: function () {alert('delete favorite'+choice+'failed')}
    })
}

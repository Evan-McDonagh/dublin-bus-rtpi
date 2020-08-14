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
// $("#register_submit").click(function () {
//     var fn = $("#username").val();
//     if ($("#username").val() == ""){alert('Please fill in your First Name *');return;}
//     else if ($("#lastname").val() == ""){alert('Please fill in your Last Name *');return;}
//     else if ($("#pwd").val() == ""){alert('Please fill the password');return;}
//     else if ($("#pwdcfm").val() == ""){alert('Please confirm the password');return;}
//     else if ($("#email").val() == ""){alert('Please fill in your email');return;}
//     else if ($("#answer").val() == ""){alert('Please answer your question');return;}
//     else{
//         var fn = $("#username").val();
//         var ln = $("#lastname").val();
//         var pwd = $("#pwd").val();
//         var pwdcfm = $("#pwdcfm").val();
//         var email = $("#email").val();
//         var phone = $("#phone").val();
//         var qst = $("#question").val();
//         var answer = $("#answer").val();
//         var gender = $('input[name=age]:checked').val();
//     }
// })
var error_username = false;
var error_last_name = false;
var error_password = false;
var error_check_password = false;
var error_email = false;
var error_answer = false;
var error_question = false;
var error_check = false;

$(document).ready(function () {
    $('#username').blur(function () {
        check_username();
    });

    $('#lastname').blur(function () {
        check_last_name();
    });

    $('#pwd').blur(function () {
        check_pwd();
    });

    $('#pwdcfm').blur(function () {
        check_pwdcfm();
    });

    $('#email').blur(function () {
        check_email();
    });

    $('#answer').blur(function () {
        check_answer();
    });

    $('#question').change(function () {
        check_question();
    });

    $('#allow').click(function () {
        if ($(this).is(':checked')) {
            error_check = false;
            $(this).siblings('span').hide();
        } else {
            error_check = true;
            $(this).siblings('span').html('请勾选同意');
            $(this).siblings('span').show();
        }
    });
})

function check_username(){
    var len = $('#username').val().length;
    if(len<1)
    {
        $('#username').next().html('please input your first name')
        $('#username').next().show();
        error_username = true;
    }
    else
    {
        $('#username').next().hide();
        error_username = false;
    }
}
// function check_last_name(){
//     var len = $('#lastname').val().length;
//     if(len<1)
//     {
//         $('#lastname').next().html('please input your first name')
//         $('#lastname').next().show();
//         error_last_name = true;
//     }
//     else
//     {
//         $('#lastname').next().hide();
//         error_last_name = false;
//     }
// }

function check_pwd(){
    var len = $('#pwd').val().length;
    if(len<8||len>20)
    {
        $('#pwd').next().html('at least 8-20 characters')
        $('#pwd').next().show();
        error_password = true;
    }
    else
    {
        $('#pwd').next().hide();
        error_password = false;
    }
}


function check_pwdcfm(){
    var pass = $('#pwd').val();
    var cpass = $('#pwdcfm').val();

    if(pass!=cpass)
    {
        $('#pwdcfm').next().html('password varies')
        $('#pwdcfm').next().show();
        error_check_password = true;
    }
    else
    {
        $('#pwdcfm').next().hide();
        error_check_password = false;
    }

}

function check_email(){
    var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

    if(re.test($('#email').val()))
    {
        $('#email').next().hide();
        error_email = false;
    }
    else
    {
        $('#email').next().html('wrong email formatter')
        $('#email').next().show();
        error_check_password = true;
    }

}

function check_answer(){
    var len = $('#answer').val().length;
    if(len<1)
    {
        $('#answer').next().html('please answer the question')
        $('#answer').next().show();
        error_answer = true;
    }
    else
    {
        $('#answer').next().hide();
        error_answer = false;
    }
}

function check_question(){
    var qust = $('#question option:selected').val();
    if(qust == "Please select your Sequrity Question")
    {
        $('#question').next().html('please select a question')
        $('#question').next().show();
        error_question = true;
    }
    else
    {
        $('#question').next().hide();
        error_question = false;
    }
}


function validate() {
    check_username();
    // check_last_name();
    check_pwd();
    check_pwdcfm();
    check_email();
    check_answer();
    check_question();

    if (error_username == false && error_password == false && error_check_password == false && error_email == false && error_answer == false && error_question == false && error_check == false) {
        return true;
    } else {
        return false;
    }
}










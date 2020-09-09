const roomName = JSON.parse(document.getElementById('room-name').textContent);
var username = JSON.parse(document.getElementById('username').textContent);

function getCookie(name) {
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
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$("#delete-chat").click(function(e) {
    e.preventDefault();
    $.ajax({
        header: { "X-CSRFToken": getCookie("csrftoken") },
        type: "POST",
        url: "/chat/action/" ,
        data: { 
            room_name: roomName, 
            action: 'delete', 
        },
        success: function(result) {
            window.location.pathname = '/explore/'; 
        },
        error: function(result) {
            alert('Chat could not be deleted');

        }
    });
});
// $("#add-chat").click(function(e) {
//     e.preventDefault();

//     $.ajax({
//         header: { "X-CSRFToken": getCookie("csrftoken") },
//         type: "POST",
//         url: "/chat/action/" ,
//         data: { 
//             room_name: roomName, 
           
//             action: 'add', 
//         },
//         success: function(result) {
//             console.log('success');
//         },
//         error: function(result) {
//             alert('Chat could not be deleted');

//         }
//     });
// });
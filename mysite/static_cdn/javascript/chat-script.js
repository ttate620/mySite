

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

function friends_selected() {
    console.log("friends selected")
    var friendList = document.getElementById("friendList");
    var opts = [];
    for (var i=0, len=friendList.options.length; i<len; i++) {
        var opt = friendList.options[i];
        if ( opt.selected ) {
            console.log(opt.value)
            opts.push(opt.value);
        }
    }
    
    return opts;
}
$('#create-chat-button').on('click',function(e){
    console.log("buttin click")
    var roomName = document.querySelector('#room-name-input').value;
    var friends_sel = friends_selected();
    
    if (friends_sel.length == 0) {
        alert("Must select at least one friend")
        return
    }
    
    $.ajax({
        data: {'friends_in_chat': friends_sel},

        headers: { "X-CSRFToken": getCookie("csrftoken") },
        url : '/chat/sendChatNotifications/'+ roomName + '/',
        dataType:'json',
        traditional: true,
        type: "POST",
        success: function(data) {
            console.log(data)
            window.location.pathname = '/chat/' + roomName + '/'; 
               
        }, error: function(error) {
            console.log('error');
            alert('Chat name unavailable')
        }
    })
   
    
})


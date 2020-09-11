
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






$(document).ready(function() {
    $(".comment-form").hide();
    $(".reply-form").hide();


    $(".reply-button").click(function(event) {
        var comment_id = event.target.id
        $(this).hide()
        console.log("form-"+comment_id)
        var reply_form = document.getElementById("form-"+comment_id)
        $("#form-"+comment_id).show()
    });

    $(".comment-button").click(function(event){
        var post_id = event.target.id
        $(this).hide()
        console.log(this)
        var comment_form = document.getElementById("form-"+post_id)
        $("#form-"+post_id).show()
    })
    
});



   


    
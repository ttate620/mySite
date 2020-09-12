
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



$(document).ready(function () {
    $("#bio").focus(function() {
      
    }).blur(function() {
       
        var bio = $('#bio').val()
        var myData = {
            'profile_field': 'bio',
            'updated_info': bio,
        }
        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            url : "update/bio/",
            global: false,
            type: "POST"
        });
        $.ajax({ data : myData}) 
    });

});


function saveClicked(){
    var editableText = $(this).parent().prev();
    var editedText = editableText.html();
    $(this).hide();
    $(this).prev().show();
    // editableText.focus();
    editableText.blur(editableTextBlurred);
    var ID = editableText.attr('id');
    var myData = {
        'profile_field': ID,
        'updated_info': editedText,
    }
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        url : "update/" + ID +"/",
        global: false,
        type: "POST"
    });
    $.ajax({ data : myData}) 
}
function editClicked(){
    $(this).hide();
    $(this).next().show();
    var divHtml = $(this).parent().prev('div').html();
    var divClass = $(this).parent().prev('div').attr('class');
    var divID = $(this).parent().prev('div').attr('id');
    var editableText = $("<textarea />");
    editableText.val(divHtml);
    editableText.addClass(divClass);
    editableText.attr('id', divID);
    $(this).parent().prev('div').replaceWith(editableText);
    editableText.focus();
    editableText.blur(editableTextBlurred); 
      
}

function editableTextBlurred() {
    var html = $(this).val();
    var viewableText = $("<div>");
    viewableText.html(html);
    viewableText.addClass($(this).attr('class'))
    viewableText.attr('id', $(this).attr('id'))
    $(this).replaceWith(viewableText);
    viewableText.click(editClicked);
    
}


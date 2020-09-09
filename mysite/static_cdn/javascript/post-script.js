


$(document).ready(function() {

    $("#comment-form").hide();
    $(".reply-form").hide();
    $("#comment-btn").click(function(){
        $("#comment-form").show();
    })
    $(".reply-btn").click(function(){
        var id = $(this).attr('id');
        var formId = '#reply-form-' + id.toString();
        $(formId).show();
    })
})



    
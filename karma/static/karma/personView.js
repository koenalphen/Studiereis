$(document).ready(function(){
    var dt = new Date();
    var dattime = dt.toISOString().slice(0,10);
    $(".date").val(dattime);



    $(".Anders").hide();

    $("#taskselect").change(function(){
        if ($("#taskselect").val() == "nieuw_task") {
            $(".Anders").show();
        }
        else{
            $(".Anders").hide();
        };
    });

    $("#taskNew").focus(function(){
        if ($(this).val() == "Omschrijving"){
            $(this).val("");
        }
    });

    $("#taskNew").focusout(function(){
        if($(this).val() == ""){
            $(this).val("Omschrijving");
        }
    });

    $("#commentField").focus(function(){
        if($(this).val() == "comment"){
            $(this).val("");
        }
    });

    $("#commentField").focusout(function(){
        if($(this).val() == ""){
            $(this).val("comment");
        }
    });

    // Code to make sure Ajax requests work in Django
    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
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

    $("button").click(function(){
        taskToRemove_id = $(this).attr("id");
        $.post("/karma/removelog/", {taskToRemove_id: taskToRemove_id});
        $(this).closest('tr').remove();

    });
});

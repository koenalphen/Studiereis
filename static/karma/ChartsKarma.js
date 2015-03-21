$(document).ready(function(){
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


// for the time graph
    // Get context with jQuery - using jQuery's .get() method.
    var over_time = $("#over_time").get(0).getContext("2d");
    // This will get the first returned node in the jQuery collection.
    var time_graph = new Chart(over_time).Line(lineData);


// for the category graph
    // Get context with jQuery - using jQuery's .get() method.
    var per_category = $("#per_category").get(0).getContext("2d");
    // This will get the first returned node in the jQuery collection.
    var perTask = new Chart(per_category).Bar(perTaskData);


// for the committee graph
    // Get context with jQuery - using jQuery's .get() method.
    var per_committee = $("#per_committee").get(0).getContext("2d");
    // This will get the first returned node in the jQuery collection.
    var perCommittee = new Chart(per_committee).Bar(perCommitteeData);


});

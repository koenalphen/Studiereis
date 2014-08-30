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


});
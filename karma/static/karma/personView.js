$(document).ready(function(){
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
});
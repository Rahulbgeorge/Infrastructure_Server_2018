var currentScreen="#newStock";

$(document).ready(function(){

    $("#newStock").click(function(){
        $.get("newstock",function(data, status){
            $("#contentScreen").html(data);
        });
    });

     $("#statistics").click(function(){
        $.get("statistics",function(data, status){
            $("#contentScreen").html(data);
        });
    });


});
$(document).ready(function(){

    $("#itemname").focus(function(){
        $(this).keypress(function(e){
            if(e.which == 13) {
                $("#qty").focus();
            }
        });
    });

})
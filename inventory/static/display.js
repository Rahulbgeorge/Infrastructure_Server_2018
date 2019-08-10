color=['#039be5','#0097a7','#827717','#ef6c00','#dd2c00','#e91e63','#9c27b0','#f44336','#673ab7','#2196f3']
data=['apple','pomogranate','tiger','balm','cheetha','nani','pomogranate','tiger','balm','cheetha','nani','pomogranate','tiger','balm','cheetha','nani']
ip=window.location.origin;
var dataSet = [];

$(document).ready(function(){
    console.log("Started processing")
    //loadData();
    $.get(ip+"/stocks/",function(data,status){
        console.log("processing data");
        console.log(data);
        dataSet=[];
        data.forEach(function(row){
        console.log("data")
        console.log(row)
        if(row['product']['measurement_type']=='n')
        {
        product_name=row['product']['name'];}
        else
        {
        product_name=row['product']['name']+"("+row['product']['qty']+row['product']['measurement_type']+")"
        }
        dataSet.push([product_name,row['qty'],row['product']['category_type']]);



        });
            loadListView();

    });
    $("#cardView").click(function(){
        console.log('card view triggered');
        //basic initialization
        $search_bar=$("<input/>")
            .addClass("searchBar")
            .attr("name","search")
            .attr("placeholder",'Search ...')
            .attr("type",'text');

        $data_row=$("<div/>")
                .addClass("row")
                .attr("id","datarow");



        $(".container").html("").append($search_bar).append($data_row);
        loadData();
    });


    $("#listView").click(function(){
    console.log("card view triggered");
        $(".container").html("");

        $table_data=$("<table/>")
            .attr("id",'mytable')
            .addClass("display");

         $(".container").html($table_data);

           $('#mytable').DataTable( {
        data: dataSet,
        columns: [
            { title: "Name" },
            { title: "Quantity" },
            { title: "Category" },

        ]
         } );



    });


    }
);



function loadListView()
{
 console.log("card view triggered");
        $(".container").html("");

        $table_data=$("<table/>")
            .attr("id",'mytable')
            .addClass("display");

         $(".container").html($table_data);

           $('#mytable').DataTable( {
        data: dataSet,
        columns: [
            { title: "Name" },
            { title: "Quantity" },
            { title: "Category" },

        ]});
        }

//LOADING DATA FOR CARD VIEW IN DISPLAY LIST
var random=0;
function loadData()
{

    data.forEach(function(content){



        $table=$('<table/>')
        .addClass("tabledata")
        .append(
            $('<center/>')
           .append( $('<tr/>')
            .append($("<td/>").text("Qty"))
            .append($("<td/>").text("22"))
            ));

            
            do{
            localrandom=parseInt(Math.random()*data.length)
            }while(random==localrandom);
            random=localrandom;
         $("#datarow").append(
            $('<div/>')
                .addClass('card col-2 mx-4')
                .css("background-color",color[random])
                //appending the top text with the caps
                .append(
                    $('<div/>')
                    .addClass('alphabet')
                    .text(content[0].toUpperCase())
                        )
                 //appending a center text i.e name of the item
                 .append($('<center/>').text(content).css("color","white"))
                 .append($table)
                 
                 );

    });
  
}
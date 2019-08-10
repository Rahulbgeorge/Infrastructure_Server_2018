var selectedItemId=0;
var ip=location.origin+"/";
var data=[];
var selectedItemStack=[];//This stack consists of data that ais pushed
var selectedItemCount=0;//Total number of items that was pushed into the selectedItem stack
var currentItem=""
var currentItemId;
var value;//REPRESENTS THE CURRENT VALUE OF THE ELEMENT

function fetchDataAndPopulateAutocompleteList()
{    
  //DEFAULT FETCHING OF DATA FOR AUTOCOMPLETE PURPOSE
  //INCLUDES DATA RELATED TO EACH PRODUCT AND ITS CURRENT QTY IN THE INVENTORY
  $.get(ip+"displayAllItems/",function(responseData,status){
             
          var temp=JSON.parse(responseData);
          console.log(temp['description']);
          data=temp['description'];
          console.log(data);
  });
  console.log("data fetch completed");
}



$(document).ready(function(){



    //Trying to fetch data and prepopulate the autocomplete list
 $.get(ip+"displayAllItems/",function(responseData,status){
           
          var temp=JSON.parse(responseData);
          console.log(temp['description']);
          data=temp['description'];
          console.log(data);
  });

   // fetchDataAndPopulateAutocompleteList();




    //For each key press in the item input field,
    // the data related to the query is populated here
  $("#itemname").keypress(function(event){
    console.log(event);  
    if(event.keyCode==13)
      {
          //on hit enter focus is changed to the prepopulated list automatically
          selectedItemId=0;
          $("#"+selectedItemId).css({background:'#3F51B5'});
      }
      else{
          //prepopulation of the data based on the data inputted by user
          populateData($("#itemname").val())
      }
  });  

  $("#saveProduct").click(saveProduct());

 
 
      




});//end of document ready



//list of preexisting data is shown over here
function populateData(input)
{
    $("#data").html("");
    var iteration=0;
    var i=0;
    this.data.forEach(element => {
        if(element.name.toLowerCase().indexOf(input)>-1)
        {
            $suggestionItem=$("<div>",{id:iteration,class:'dataItem'});
            $("#data").append($suggestionItem);
            $("#"+iteration).text(element.name+"( "+element.mass+" "+element.type+" )");
            $("#"+iteration).data("value", i+"");
            item=i+"";
            $("#"+iteration).click(function(){
                
                selectItem($(this));
            });
            console.log(element);
            iteration=iteration+1;
        }
        i=i+1;
    });
}


//On click of a prepoulated list this fucntion is triggered
function selectItem(th)
{
    //TH REPRESENTS THE CURRENT ITEM IN THE LIST

    console.log(th);
    console.log(th.data("value"));
    value=data[th.data('value')];
    //pushing the data items to the stack
    selectedItemStack.push(value);
    selectedItemCount++;
    console.log(value);
    
        console.log("row pushing triggered in else side");
        pushDataToTable(value);
        // $("#newProductTable tr:last").append("<tr><td>iteration</td><td>new item</td><td>4</td></tr>");
        //PUS
        // $("#itemname").val(value.name+"( "+value.mass+value.type+" )");
        // $("#qty").focus();

    
   
} 

function saveProduct()
{
    var itemname=$("#newItemName").val();
    var itemmass=$("#newItemMass").val();
    var itemtype=$("#itemType").val();
    var category=$("#itemcategory").val();
    var inventoryqty=$("#newInventoryQty").val();

    console.log(itemmass);
    console.log(itemtype);
    console.log(inventoryqty);
    console.log(category);
    param={};
    param['itemtype']=itemtype;
    param['itemname']=itemname;
    param['itemcategory']=itemcategory;


    if(itemmass!="")
    {    
        param['itemmass']=itemmass;
        if(inventoryqty=="")
        {
            param['inventoryqty']=inventoryqty;
            $.post(ip+"/newItemEntry/",{itemname:itemname,itemmass:itemmass,itemtype:itemtype,itemcategory:category},function(data,status){
                out=JSON.parse(data);
                if(out['result']=="fail")
                {alert(out['description']);}
                else{
                console.log("new item entry");
                console.log(out['description'])
                    alert(out['description']);
                    window.location=ip+"/qrcode/?id="+out['description'];
                    fetchDataAndPopulateAutocompleteList();
                    $("#modalCloseButton").click();
                }
               

            });

        }
        else{
        $.post(ip+"newItemEntry/",{itemname:itemname,itemmass:itemmass,itemtype:itemtype,itemcategory:category,inventoryqty:inventoryqty},function(data,status){
            out=JSON.parse(data);
            if(out['result']=="fail")
            {alert(out['description']);}
            else{
                alert(out['description']);
                console.log("new item added");
                console.log(out['description']);
                window.location=ip+"/qrcode_page/?id="+out['description'];
                fetchDataAndPopulateAutocompleteList();
                $("#modalCloseButton").click();
            }
        

        });
        }
    }
    else
    console.log("item mass not available");
}





//THIS FUNCTION IS INVOKED WHEN
  function pushDataToTable(item)
  {
    // $("#qty").remove();
    var itemName=item.name+"( "+item.mass+item.type+" )";
    $("#itemname").replaceWith(itemName);
    // var rowMarkup="<tr><td>"+(selectedItemCount)+"</td><td>"+value.name+"</td><td><input type='number' id='qty'></td></tr>";
    // var rowCount = $('#stockTable > tbody >tr').length;
    // console.log("row count is"+rowCount);
    // // $('#stockTable  > tbody > tr').eq(rowCount-1).after(rowMarkup);
    //  $('#stockTable  > tbody').append(rowMarkup);

    $("#qty").focus();
    $("#qty").keypress(function(event){
        console.log("hey");
            if(event.keyCode==13)
            {
                pushNewAddOption();
            }
            });
  }

  function pushNewAddOption()
  {

    //pushing the inputted value to existing stack
    var quantity=$("#qty").val();
    selectedItemStack[selectedItemCount-1].qty=quantity;
    console.log(selectedItemStack);
      $("#qty").replaceWith($("#qty").val());
    var rowCount = $('#stockTable > tbody >tr').length;
    console.log("row count is"+rowCount);
    var rowMarkup="<tr><td>"+(selectedItemCount+1)+"</td><td><input type='text' id='itemname'></td><td><input type='number' id='qty'></td></tr>"
    $('#stockTable  > tbody ').append(rowMarkup);
    //For each key press in the item input field,
    // the data related to the query is populated here
    $("#itemname").focus();

  $("#itemname").keypress(function(event){
    console.log(event);  
    if(event.keyCode==13)
      {
          //on hit enter focus is changed to the prepopulated list automatically
          selectedItemId=0;
          $("#"+selectedItemId).css({background:'#3F51B5'});
      }
      else{
          //prepopulation of the data based on the data inputted by user
          populateData($("#itemname").val())
      }

  }); 
  }


  //The entire bills data is saved over here
  function saveBillData()
  {
    var gst=$("#gst").val();
    var date=$("#billDate").val();
    var cost=$("#billCost").val();
    var category=$("#billCategory").val();
    var data=JSON.stringify(selectedItemStack);

    $.post(ip+"newBill/",{items:data,gst:gst,date:date,cost:cost,category:category},function(data,status){
        out=JSON.parse(data);
        if(out['result']=="fail")
        {alert(out['description']);}
        else{
            console.log("bill added successfully");
            window.location=ip+"qrcode_page?id="+out['description'];
            alert("Successfully added product");
            fetchDataAndPopulateAutocompleteList();
            $("#modalCloseButton").click();
        }
       

    });
  }
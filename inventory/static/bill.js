var billdata=[];
var billProducts={};
var dataSet={};
var table;
var first_time=true;
ip=window.location.origin+"/";
$(document).ready(function(){
        //console.log(ip)
        $.get(ip+"bills/",function(data,status){
            console.log("data is printing")
            console.log(data);
            data.forEach(element => {
                //store bill data for database purpose
                billdata.push([element['id'],element['date'],element['gstid'],element['price']]);
                billProducts[element['date']+element['gstid']]=[];

                //store product data is billproducts 
                element['bill'].forEach(productInfo=>{
                        productData=productInfo['product'];
                        productData['stock']=productInfo['qty'];
                        //key value of product stored is a combination of 
                       billProducts[element['date']+element['gstid']].push(productData);
                });
            });

            loadTable();
        });


        $("#print").click(function(){
            window.location=ip+"qrcode_page?id="+currentinfo[0];
        });



     

});

function loadTable()
{
    table=$('#mytable').DataTable( {
        data: billdata,
        columns: [
            { title: "id"},
            { title: "Date" },
            { title: "Gstid" },
            { title: "Price" },

        ]
         } );

         $('#mytable').on('click', 'tr', function () {

            var data = table.row( this ).data();
            //this info is used during printing operation trigger
            currentinfo=data;
            console.log("table data prining")
            console.log(table.row(this));
            console.log(data)
            //console.log(data[0]+data[1]);
            localProducts=[]
            billProducts[data[1]+data[2]].forEach(product=>{
                //console.log("product is pushed");
                //console.log(product);
                localProducts.push([product['name'],product['stock']])
            });


            if(first_time)
            {
                
            producttable=$("#productTable").DataTable({
                data:localProducts,
                columns: [
                    { title: "Product name" },
                    { title: "Qty" },
        
                ]
            });
                $('#myModal').modal(); 
                first_time=false;
            }
            else{
                producttable.clear();
                producttable.rows.add(localProducts);
                producttable.draw();
            $('#myModal').modal('toggle'); 
            }

        } );
}
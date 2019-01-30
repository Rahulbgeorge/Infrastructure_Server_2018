from django.shortcuts import render
from django.shortcuts import  HttpResponse
from .models import Bill,Product,Stock
import json

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request,"index.html")

def newstock(request):
    return render(request,"newstock.html")

def statistics(request):
    return render(request,"statistics.html")

def data(request):
    return HttpResponse('{"hey:"inga"}')


#NEW BILL ENTRY IS DONE OVER HERE
@csrf_exempt
def newBillEntry(request):
    if request.method=="POST":
        print(request.POST)
        data = request.POST['data']
        data=json.loads(data)
        print(data)
        bill_category=data.get("bill_category",None)
        bill_cost=data.get("bill_cost",None)
        bill_date=data.get("bill_date",None)
        bill_gst=data.get("bill_gst",None)
        items=data.get("items",None)
        print("before if")
        if(bill_gst==None or bill_category==None ):
            return HttpResponse("fail")
        else:
            bill=Bill(category_type=bill_category,gstid=bill_gst,date=bill_date,price=bill_cost)
            bill.save()
            print("ID GENERATED FOR THE BILL IS")
            print(bill.id)
            for item in items:
                product=Product().findProduct(item['item'],item['mass'],item['qtyType'],bill_category)
                stock=Stock(bid=bill.id,pid=product.id,qty=item['qty'])
                stock.save()
            currentItem=request.POST['items']
            print(currentItem)





        return HttpResponse("successfully recieved data")
    return HttpResponse("fail")

@csrf_exempt
def newItemEntry(request):
    if(request.method=="POST"):
        itemname=request.POST.get("itemname",None)
        itemmass=request.POST.get("itemmass",None)
        itemtype=request.POST.get("itemtype",None)
        itemcategory=request.POST.get("itemcategory",None)
        inventoryqty=request.POST.get("inventoryqty",None)
        print(request.POST)
        if(itemname==None or itemmass==None or itemtype==None or itemcategory==None):
            print("data missing")
            return fail("Invalid input")
        else:
            product,alreadyExists = Product().findProduct(itemname, itemmass, itemtype, itemcategory)
            if(not alreadyExists):
                if(inventoryqty is not None):
                    if(int(inventoryqty)>0):
                        stock=Stock(product=product,qty=int(inventoryqty))
                        stock.save()
                        return success("new product item added with quantity")
                else:
                    stock = Stock(product=product, qty=0)
                    stock.save()
                    return success("new Product added without quantity")
            else:
                return fail("product already exists")
    print("post request not found")
    return fail("Try a post request")

def displayAllItems(request):
    products=Stock.objects.all()
    out=[]
    for product in products:
        data={}
        data['name']=product.product.name
        data['mass']=product.product.qty
        data['type']=product.product.measurement_type
        data['qty']=product.qty
        out.append(data)
    return success(out)





def success(message):
    out={}
    out['result']='success'
    out['description']=message
    return HttpResponse(json.dumps(out))

def fail(message):
    out={}
    out['result']='fail'
    out['description']=message
    return HttpResponse(json.dumps(out))

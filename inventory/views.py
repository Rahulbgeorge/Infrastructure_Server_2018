from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Bill, Product, Stock, BillData, Outgoing_stock_log
import json
from django.conf import settings
from rest_framework import generics, serializers
from rest_framework.views import APIView
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import django_filters.rest_framework
from .Serializers import *


#latest updated complete, only navigation bar needs to be setup
def bill_page(request):
    return render(request,"bill_page.html")


#latest updated complete, only navigation bar needs to be stup
def newstock(request):
    return render(request, "new_stock.html")


def homepage(request):
    return render(request,"index.html")

def inventory_log(request):
    return render(request,"display_items.html")

def qrCode(request):

    return render(request,"qrcode_gen.html",{'bill_id':request.GET['id']})

# NEW BILL ENTRY IS DONE OVER HERE
@csrf_exempt
def newBillEntry(request):
    if request.method == "POST":
        print(request.POST)

        data = request.POST['items']
        data = json.loads(data)
        print(data)
        bill_category = request.POST.get("category", None)
        bill_cost = request.POST.get("cost", None)
        bill_date = request.POST.get("date", None)
        bill_gst = request.POST.get("gst", None)

        bill, isExists = Bill().findOrSave(bill_gst, bill_date, bill_cost, bill_category)
        if (isExists):
            return fail("Bill already exists")
        else:
            for item in data:
                product, status = Product().findProduct(item['name'], item['mass'], item['type'])
                stock = Stock.saveStockData(product=product, qty=item['qty'])
                billStock = BillData(bill=bill, product=product, qty=item['qty'])
                billStock.save()
            return success(bill.id)

        # if(bill_gst==None or bill_category==None ):
        #     return HttpResponse("fail")
        # else:
        #     bill=Bill(category_type=bill_category,gstid=bill_gst,date=bill_date,price=bill_cost)
        #     bill.save()
        #     print("ID GENERATED FOR THE BILL IS")
        #     print(bill.id)
        #     for item in items:
        #         product=Product().findProduct(item['item'],item['mass'],item['qtyType'],bill_category)
        #         stock=Stock(bid=bill.id,pid=product.id,qty=item['qty'])
        #         stock.save()
        #     currentItem=request.POST['items']
        #     print(currentItem)


@csrf_exempt
def newItemEntry(request):
    if (request.method == "POST"):
        itemname = request.POST.get("itemname", None)
        itemmass = request.POST.get("itemmass", None)
        itemtype = request.POST.get("itemtype", None)
        itemcategory = request.POST.get("itemcategory", None)
        inventoryqty = request.POST.get("inventoryqty", None)
        print(request.POST)
        if (itemname == None or itemmass == None or itemtype == None or itemcategory == None):
            print("data missing")
            return fail("Invalid input")
        else:
            product, alreadyExists = Product().findOrCreateProduct(name=itemname, qty=itemmass,
                                                                   measurementType=itemtype, categoryType=itemcategory)
            if (not alreadyExists):
                if (inventoryqty is not None):
                    if (int(inventoryqty) > 0):
                        stock = Stock(product=product, qty=int(inventoryqty))
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
    products = Stock.objects.all()
    out = []
    for product in products:
        data = {}
        data['name'] = product.product.name
        data['mass'] = product.product.qty
        data['type'] = product.product.measurement_type
        data['qty'] = product.qty
        out.append(data)
    return success(out)



class Products(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()





class Stocks(generics.ListAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class StockData(generics.RetrieveAPIView,
                generics.UpdateAPIView):
    """
        Patch operation -- take out stock
    """
    lookup_field = "pk"
    serializer_class = StockSerializer

    def get_object(self):
        print("stock data printing")
        pk=self.kwargs.get('pk')
        return Stock.objects.get(id=pk)

    def perform_update(self, serializer):
        print(dir(serializer))
        print(serializer.validated_data['qty'])


class BillView(generics.ListAPIView):
    serializer_class = BillSerializer
    queryset = Bill.objects.all().order_by("-date")

class SingleBill(generics.RetrieveAPIView):
    serializer_class = SingleBillSerializer
    lookup_field = "id"
    def get_object(self):
        id=self.kwargs.get("id",None)
        if id is not None:
            return Bill.objects.get(id=id)


class Withdraw_histor_Serializer(serializers.ModelSerializer):
    person=serializers.SerializerMethodField()
    product=serializers.SerializerMethodField()
    date=serializers.SerializerMethodField()
    class Meta:
        model=Outgoing_stock_log
        fields=("person","product","date","qty")

    def get_person(self,instance):
        return instance.taken_by.name

    def get_product(self,instance):
        return instance.product.name

    def get_date(self,instance):
        return instance.date


class Withdraw_history(generics.ListAPIView):
    serializer_class = Withdraw_histor_Serializer
    queryset = Outgoing_stock_log.objects.all()

def success(message):
    out = {}
    out['result'] = 'success'
    out['description'] = message
    return HttpResponse(json.dumps(out))


def fail(message):
    out = {}
    out['result'] = 'fail'
    out['description'] = message
    return HttpResponse(json.dumps(out))

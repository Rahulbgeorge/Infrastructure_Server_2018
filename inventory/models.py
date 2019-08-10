from django.db import models
from rest_framework.views import APIView
# Create your models here.

class Product(models.Model):
    '''
        USE: THIS TABLE IS INTENTED ONLY FOR THE IDENTIFICATION OF THE PRODUCTS
            DESCRIPTION:
            <qty> : DESCRIBES THE MASS OR WEIGHT OF THE PARTICULAR ITEMS, FOR INSTANCE '1L HARPIC'  HERE 1 IS THE QUANTITY
            <measurement_type> : LITRE(l), GRAMS(g), KILOGRAMS(kg) ETC..
            <category_type>: HOUSE_KEEPING(h), ELECTRICAL(e), PLUMBING(p)
    '''
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=40 )
    qty=models.FloatField()
    measurement_type=models.CharField(max_length=5, default="None")
    category_type=models.CharField(max_length=2, default="None")
    cost=models.FloatField(default=0)

    def findOrCreateProduct(self,name,qty,measurementType,categoryType):
        try:
            print(categoryType)
            product=Product.objects.get(name=name,qty=qty,measurement_type=measurementType,category_type=categoryType)
            print("Product Already Exists")
            return [product,True]
        except Product.DoesNotExist:
            product=Product(name=name,qty=qty,measurement_type=measurementType,category_type=categoryType)
            product.save()
            product=Product.objects.get(name=name,qty=qty,measurement_type=measurementType,category_type=categoryType)
            print("New produt created")
            return [product,False]

    def findProduct( self,name, qty, measurementType):
        try:
            product = Product.objects.get(name=name, qty=qty, measurement_type=measurementType)
            print("Product Already Exists")
            return [product, True]
        except Product.DoesNotExist:
            product = Product(name=name, qty=qty, measurement_type=measurementType)
            product.save()
            product = Product.objects.get(name=name, qty=qty, measurement_type=measurementType)
            print("New produt created")
            return [product, False]



class Bill(models.Model):
    '''
        USE: THIS TABLE IS USED TO STORE THE BILL DETAILS ONLY
    '''
    category_type=models.CharField(max_length=5, default="a")
    gstid=models.CharField(default=None, max_length=15)
    date=models.CharField(max_length=20)
    price=models.FloatField()
    pic=models.CharField(max_length=30)

    def findOrSave(self,gst,date,price,category):
        try:
            bill=Bill.objects.get(gstid=gst,date=date,price=price,category_type=category)
            return [bill,True]
        except:
            print(price)
            print(type(price))
            bill=Bill(gstid=gst,date=date,price=float(price),category_type=category)
            bill.save()
            bill=Bill.objects.get(gstid=gst,date=date,price=price)
            return [bill,False]

class BillData(models.Model):
    id=models.AutoField(primary_key=True)
    bill=models.ForeignKey(Bill,on_delete=models.CASCADE,related_name="bill")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.IntegerField()

class Stock(models.Model):
    '''
        EACH PRODUCT GROUP IS STORED OVER HERE
        THIS ID WILL BE USED FOR THE PURPOSE OF  GENERATION OF BARCODES/QR CODES
    '''
    id=models.AutoField(primary_key=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.IntegerField()
    expirity_date=models.CharField(default=None,max_length=20,null=True)

    @staticmethod
    def saveStockData(product,qty):
        try:
            stock=Stock.objects.get(product=product)
            stock.qty=stock.qty+int(qty)
            stock.save()
            stock=Stock.objects.get(product=product)
            return stock
        except:
            stock=Stock(product=product,qty=qty)
            stock.save()
            stock=Stock.objects.get(product=product)
            return stock

class People(models.Model):
    OTHER_STAFF="OS"
    TEACHING_STAFF="TS"
    ADMINISTRATION="AD"
    designation_choices=[(OTHER_STAFF,"Other Staff"),
                         (TEACHING_STAFF,"Teaching Staff"),
                         (ADMINISTRATION,"Administration Staff")]

    class Meta:
        unique_together=(("designation","name"))
    id=models.AutoField(primary_key=True)
    designation=models.CharField(max_length=3,choices=designation_choices)
    name=models.CharField(max_length=30)

    @staticmethod
    def addPerson(name,designation=OTHER_STAFF):
        if not(len(name)<2):
            try:
                person=People(name=name,designation=designation)
                person.save()
                return person,"Success"
            except Exception as e:
                return None,str(e)
        else:
            return None,"Invalid name"

    @staticmethod
    def listAll():
        return People.objects.all()

    @staticmethod
    def listAdministrators():
        return People.objects.filter(designation=People.ADMINISTRATION)

    @staticmethod
    def listOtherStaff():
        return People.objects.filter(designation=People.OTHER_STAFF)


class Outgoing_stock_log(models.Model):
    id=models.AutoField(primary_key=True)
    taken_by=models.ForeignKey(People,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    qty=models.IntegerField()

    def withdraw_stocks(self,stocks,withdrawn_person):
        for stock in stocks:
            #decrease from existing stock
            myproduct=Product.objects.get(id=stock['id'])
            myStock=Stock.objects.get(product=myproduct)
            if(myStock.qty>=stock['qty']):
                myStock.qty=myStock.qty-int(stock['qty'])
                myStock.save()
                people=People.objects.get(id=withdrawn_person)
                #add data to withdrawn stock
                log=Outgoing_stock_log(product=myproduct,qty=stock['qty'],taken_by=people)
                log.save()

        return True











from django.db import models

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

    def findProduct(self,name,qty,measurementType,categoryType):
        try:
            product=Product.objects.get(name=name,qty=qty,measurement_type=measurementType,category_type=categoryType)
            print("Product Already Exists")
            return [product,True]
        except Product.DoesNotExist:
            product=Product(name=name,qty=qty,measurement_type=measurementType,category_type=categoryType)
            product.save()
            product=Product.objects.get(name=name,qty=qty,measurement_type=measurementType,category_type=categoryType)
            print("New produt created")
            return [product,False]



class Bill(models.Model):
    '''
        USE: THIS TABLE IS USED TO STORE THE BILL DETAILS ONLY
    '''
    category_type=models.CharField(max_length=5, default="a")
    gstid=models.CharField(default=None, max_length=15)
    date=models.CharField(max_length=20)
    price=models.FloatField()
    pic=models.CharField(max_length=30)


class Stock(models.Model):
    '''
        EACH PRODUCT GROUP IS STORED OVER HERE
        THIS ID WILL BE USED FOR THE PURPOSE OF  GENERATION OF BARCODES/QR CODES
    '''
    product=models.OneToOneField(Product,on_delete=models.CASCADE)
    id=models.IntegerField(primary_key=True)
    bill=models.ForeignKey(Bill,on_delete=models.SET_NULL, null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.IntegerField()
    expirity_date=models.CharField(default=None,max_length=20,null=True)









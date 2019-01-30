from django.test import TestCase
from .models import Stock,Bill,Product
# Create your tests here.

def cleanDatabase():
    Product.objects.all().delete()
    Bill.objects.all().delete()
    Stock.objects.all().delete()
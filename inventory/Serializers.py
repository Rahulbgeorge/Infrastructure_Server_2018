from .models import Product,Stock,Bill,BillData,People
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    category_type = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'qty', 'category_type', 'measurement_type']

    def get_category_type(self, obj):
        convert = {"h": "House Keeping", "e": "Electricals", "p": "Plumbing"}
        return convert[obj.category_type]


class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'product', 'qty', ]
        read_only_fields=("id","product")
        write_only_fields=("qty",)


class BillDataSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    class Meta:
        model=BillData
        fields=('product','qty')

class BillSerializer(serializers.ModelSerializer):
    bill=BillDataSerializer(many=True,read_only=True)
    class Meta:
        model=Bill
        fields=('id','date','category_type','gstid','price','bill')


class SingleBillDataSerializer(serializers.ModelSerializer):
    id=serializers.SerializerMethodField()
    name=serializers.SerializerMethodField()

    class Meta:
        model=BillData
        fields=('id','name','qty')

    def get_id(self,instance):
        return instance.product.id
    def get_name(self,instance):
        return instance.product.name
    def get_qty(self,instance):
        return instance.product.qty

class SingleBillSerializer(serializers.ModelSerializer):
    bill=SingleBillDataSerializer(many=True,read_only=True)
    class Meta:
        model=Bill
        fields=('id','bill')


class PeopleWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model=People
        fields=('id','name','designation')

class PeopleReadSerializer(serializers.ModelSerializer):
    designation = serializers.SerializerMethodField()

    class Meta:
        model = People
        fields = ('id', 'name', 'designation')


    def get_designation(self,value):
        if value == People.OTHER_STAFF:
            return "Other staff"
        elif value== People.ADMINISTRATION:
            return "Administration"
        else:
            return "Teaching staff"


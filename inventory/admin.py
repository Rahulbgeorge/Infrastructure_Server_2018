from django.contrib import admin

# # Register your models here.
from .models import Stock ,BillData,Bill,Outgoing_stock_log

admin.site.site_header="Christ Infrastructure Admin"



@admin.register(Bill)
class Bill(admin.ModelAdmin):
    list_display=('category_type','gstid','date','price')


@admin.register(Stock)
class Stock(admin.ModelAdmin):
    list_display=('id','Name','qty','expirity_date','category_type')

    def Name(self,obj):
        return obj.product.name+" ("+str(obj.product.qty)+obj.product.measurement_type+")"

    def category_type(self,obj):
        data={"h":"House Keeping",'e':"Electrical",'p':"Plumbing"}
        return data[obj.product.category_type]

@admin.register(Outgoing_stock_log)
class outgoing_stock(admin.ModelAdmin):
    list_display=("id","taken_by","product","date","qty")

    def taken_by(self,obj):
        return obj.taken_by.name

    def product(self,obj):
        return obj.product.name
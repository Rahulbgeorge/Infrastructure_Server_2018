import json
from .models import People
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import  generics
from .Serializers import PeopleReadSerializer,PeopleWriteSerializer
from .models import Outgoing_stock_log







class WithDrawStock(APIView):
    """
           Post operation can be used for withdrawing stock

           <B>Input Format</b>
           >> 'data' : {
                   'items':[
                       {'id':'2',
                        'qty':19},
                       {'id':'3',
                        'qty':21}
                        ]
                   'withdrawee_id':'21'
                   }
           """
    def post(self,request):
        data=request.POST.get("data",None)
        if data is not None:
            data=json.loads(data)
            withdraw_person=data['withdrawee_id']
            itemList=data['items']
            Outgoing_stock_log().withdraw_stocks(stocks=itemList,withdrawn_person=withdraw_person)
            return HttpResponse("success")



        return HttpResponse("Data responded")


class PeopleView(generics.ListCreateAPIView):
    queryset = People.listAll()

    def get_serializer_class(self):
        if self.request.method=="POST":
            return PeopleWriteSerializer
        else:
            return PeopleReadSerializer

class PersonView(generics.DestroyAPIView,
                 generics.RetrieveAPIView):
    lookup_field = "pk"
    queryset = People.listAll()

    def get_serializer_class(self):
        if self.request.method=="POST":
            return PeopleWriteSerializer
        else:
            return PeopleReadSerializer


from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ang/',include("angtest.urls")),
    url(r'^inventory/',include("inventory.urls"))
    #url(r'^',include("inventory.urls")),

]

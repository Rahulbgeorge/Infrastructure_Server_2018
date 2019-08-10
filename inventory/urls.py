"""infrastructureServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import Path
from django.contrib import admin
from .views import BillView, Stocks, StockData, Products, newstock, newBillEntry, newItemEntry, \
    displayAllItems,Withdraw_history, bill_page, SingleBill, qrCode,homepage ,inventory_log
from .mobile_view import WithDrawStock, PeopleView, PersonView
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^docs/', include_docs_urls(title='My API title')),
    url("^newBill/$", newBillEntry),
    url("^newItemEntry/$", newItemEntry),
    url("^displayAllItems/$", displayAllItems),
    url("^products/", Products.as_view()),
    url("^stocks/$", Stocks.as_view()),
    url("^bills/", BillView.as_view()),
    url("^bill/(?P<id>\d+)/", SingleBill.as_view()),
    url("^history/",Withdraw_history.as_view()),

    # ------------- PHONE RELATED APIS ---------------------------
    url("^withDrawStock/", WithDrawStock.as_view()),
    url("^stocks/(?P<pk>\d+)/", StockData.as_view()),
    url("^people/$", PeopleView.as_view()),
    url("^people/(?P<pk>\d+)/", PersonView.as_view()),

    # ---------------- Page Rendering ------------------
    url("^bill_page/", bill_page),
    url("^newstock$", newstock),
    url("^qrcode_page$", qrCode),
    url("^$",inventory_log),
]

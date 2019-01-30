from django.shortcuts import render

# Create your views here.

def home(request):
    print("i did reach this file with a lot of difficulty")
    return render(request,"angular/index.html")
from django.shortcuts import render

from django.http import HttpResponse as HP
def home(request):
    return render(request,"home.html")

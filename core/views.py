from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def about(request):
    context={
        'active_class':'aboutus'
    }
    return render(request,"core/about.html",context)

def contact(request):
    context={
        'active_class':'contactus'
    }
    return render(request,"core/contact.html",context)

def login(request):
    return render(request,"core/login.html")

def signup(request):
    return render(request,"core/signup.html")
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def about(request):
    return render(request,"core/about.html")

def contact(request):
    return render(request,"core/contact.html")

def login(request):
    return render(request,"core/login.html")

def signup(request):
    return render(request,"core/signup.html")
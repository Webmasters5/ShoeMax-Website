from django.shortcuts import render,redirect
from django.contrib.auth import aauthenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from django.http import HttpResponse



# Create your views here.
def about(request):
    return render(request,"core/about.html")

def contact(request):
    return render(request,"core/contact.html")

def log_in(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = aauthenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('homepage/home.html')
        else:
            messages.success(request,"There was an error logging in.") 
            return redirect('core/login.html')
    else:
        return render(request,"core/login.html")

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core/login.html')  # or your dashboard
    else:
        form = RegisterForm()

    return render(request,"core/signup.html")
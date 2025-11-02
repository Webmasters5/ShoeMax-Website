from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import signupform , loginform
from django.http import HttpResponse



# Create your views here.
###       about page
def about(request):
    context={
        'active_class':'aboutus'
    }
    return render(request,"core/about.html",context)


###       contact page
def contact(request):
    context={
        'active_class':'contactus'
    }
    return render(request,"core/contact.html",context)


###      login 
def log_in(request):

    if request.method == "POST":
        form = loginform(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                messages.success(request,'You have successfully logged in.')
                print('asfvs')
                return redirect('signup')
            else:
                messages.error(request,'Error. User does not exist.')
                print('pna')
                
        
        else:
            messages.success(request,"There was an error logging in.") 
            # return redirect('core/login.html')
    else:
        form = loginform()

    # print("Form valid:", form.is_valid())
    # print("Form errors:", form.errors)
    # print("User:", user)
    # print("Authenticated:", request.user.is_authenticated)

    return render(request,"core/login.html", {"loginform" : form})
    

###           logout
def logOut(request):
    logout(request)
    messages.success(request,"You have successfully logged out.")
    return redirect('home')


#######   sign up
def signup(request):
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has successfully been created.')
            return redirect('home')  # or your dashboard
    else:
        form = signupform()

    return render(request,"core/signup.html", {'form' : form})
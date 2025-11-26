from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import signupform , loginform,forgotPassword
from django.http import HttpResponse

#for email sending
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.
###       about page
def about(request):
    context={
        'active_class':'aboutus'
    }
    return render(request,"core/about.html",context)


###       contact page
def contact(request):

    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('telnum')
        message = request.POST.get('message')

        # Build email content
        subject = f"New Contact Us Message from {fname} {lname}"
        body = f"""
        You have received a new message from the Contact Us form:

        Name: {fname} {lname}
        Email: {email}
        Phone Number: {phone}
        Message:
        {message}
        """

        # Send email
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,        # sender (your account)
            ['shoemaxtest@gmail.com'],       # recipient (your inbox)
            fail_silently=False,
        )

        # … process form and send email …
        messages.success(request, f"Thank you {fname}, your message has been sent!", extra_tags='contactSuccess')
        return redirect('core:contact')
    return render(request, 'core/contact.html')


###      login 
def log_in(request):

    if request.method == "POST":
        form = loginform(request,data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                messages.success(request,'You have successfully logged in.')
                return redirect('homepage:home')
            else:
                messages.error(request,'Error. User does not exist.')
                
        
        else:
            messages.success(request,"There was an error logging in.") 
            # return redirect('core:login')
    else:
        form = loginform()

    return render(request,"core/login.html", {"loginform" : form})
    

###           logout
def logOut(request):
    logout(request)
    messages.success(request,"You have successfully logged out.")
    return redirect('homepage:home')


#######   sign up
def signup(request):
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has successfully been created.')
            return redirect('core:login')  # or your dashboard
    else:
        form = signupform()

    return render(request,"core/signup.html", {'form' : form})



############# FORGOT PASSWORD ##########################

def forgot_password_view(request):
    if request.method == 'POST':
        form = forgotPassword(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='core/password_reset_email.html',
                subject_template_name='core/passwordResetSubject.txt',
                from_email=None,  # Or set a custom sender
            )
            messages.success(request, "Password reset link sent to your email.")
            return redirect('core:login')  # Create this view or template
    else:
        form = forgotPassword()

    return render(request, 'core/forgotPassword.html', {'form': form})




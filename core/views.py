from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import signupform , loginform
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings

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


###       contact page    ###
def contact(request):

    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('telnum')
        message = request.POST.get('message')

        #Email validation using built-in email validation
        try:
            validate_email(email)
        except ValidationError:
            messages.success(request, "Invalid email address.",extra_tags='contactSuccess')
            #re-render with existing data

            return render(request, 'core/contact.html', {
                'fname': fname,
                'lname': lname,
                'email': email,
                'phone': phone,
                'message': message,
            })
        
        #### email validation using regex for email domains ###
        common_email_pattern = re.compile(r'^[A-Za-z0-9._%+-]+@(?:gmail\.com|yahoo\.com|outlook\.com|hotmail\.com|icloud\.com|protonmail\.com)$')
        if not common_email_pattern.match(email):
            messages.success(request, "Invalid email domain. Please use Gmail, Yahoo, Outlook, Hotmail, iCloud, or ProtonMail.", extra_tags='contactSuccess')
            return render(request, 'core/contact.html', {
                'fname': fname,
                'lname': lname,
                'email': email,
                'phone': phone,
                'message': message,
            })


        #Phone validation with regex
        phone_pattern = re.compile(r'^\+230\d{8}$')
        if not phone_pattern.match(phone):
            messages.success(request, "Invalid phone number. Use format +23012345678 (up to 8 digits after +230).", extra_tags='contactSuccess')
            #re-render with existing data
            return render(request, 'core/contact.html', {
                'fname': fname,
                'lname': lname,
                'email': email,
                'phone': phone,
                'message': message,
            })


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

    next_param = request.GET.get('next') or request.POST.get('next') or ''
    if request.method == "POST":
        form = loginform(request,data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get("remember_me")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                messages.success(request,'You have successfully logged in.')
                # Validate next; fallback to LOGIN_REDIRECT_URL
                if next_param:
                    return redirect(next_param)
                return redirect(settings.LOGIN_REDIRECT_URL or 'homepage:home')
            else:
                messages.error(request,'Error. User does not exist.')

            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)
        else:
            messages.success(request,"There was an error logging in.") 
    else:
        form = loginform()

    return render(request,"core/login.html", {"loginform" : form, "next": next_param})
    

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


class forgot_password_view(PasswordResetView):
    template_name = "registration/password_reset_form.html"
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "domain": "localhost:8000",  # change in prod (e.g., myapp.com)
            "protocol": "http",          # use "https" in production
        })
        return ctx


def toggle_theme(request):
    """Toggle the site theme between 'light' and 'dark' using a cookie."""
    from django.views.decorators.http import require_POST
    from django.http import HttpResponseRedirect

    @require_POST
    def _inner(req):
        next_url = req.META.get('HTTP_REFERER') or '/'
        current = req.COOKIES.get('theme', 'light')
        new = 'dark' if current == 'light' else 'light'
        response = HttpResponseRedirect(next_url)
        # persist for 1 year
        response.set_cookie('theme', new, max_age=60 * 60 * 24 * 365, httponly=False)
        return response

    return _inner(request)
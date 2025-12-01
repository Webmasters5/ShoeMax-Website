from django.shortcuts import render, redirect
from django.contrib import messages
from models_app.models import Shoe
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
#for email sending
from django.core.mail import send_mail
from django.conf import settings
###       home page
def home(request):
    context={
        'active_class':'home'
    }
    return render(request,'storefront/home.html',context)

###       about page
def about(request):
    context={
        'active_class':'aboutus'
    }
    return render(request,"storefront/about.html",context)

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

            return render(request, 'storefront/contact.html', {
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
            return render(request, 'storefront/contact.html', {
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
            return render(request, 'storefront/contact.html', {
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
        return redirect('storefront:contact')
    return render(request, 'storefront/contact.html')


def categories(request):
    #Lists a few samples from each category
    categories = Shoe.CATEGORY_CHOICES
    categories_list = []
    for code, label in categories.items():
        samples = list(Shoe.objects.filter(category=code)[:4])
        categories_list.append({
            'code': code,
            'label': label,
            'shoes': samples,
        })

    context = {
        'categories_list': categories_list,
        'active_class': 'categories',
    }
    return render(request, 'storefront/categories.html', context)
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm
from django.contrib.auth.models import User



class loginform(AuthenticationForm):

    ## to apply custom css to input fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ##custom css for username
        self.fields['username'].widget.attrs.update({
            'class' : 'username-input',
            'placeholder' : 'Username'
        })

        ##custom css for password
        self.fields['password'].widget.attrs.update({
            'class' : 'password-input',
            'placeholder' : 'Password'
        })


class signupform(UserCreationForm):

    ## to apply custom css to input fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ##custom css for username
        self.fields['username'].widget.attrs.update({
            'class' : 'username-input',
            'placeholder' : 'Username'
        })

        ##custom css for email
        self.fields['email'].widget.attrs.update({
            'class' : 'email-input',
            'placeholder' : 'Email'
        })

        ##custom css for password
        self.fields['password1'].widget.attrs.update({
            'class' : 'password-input',
            'placeholder' : 'Password'
        })

        ##custom css for password (confirmation)
        self.fields['password2'].widget.attrs.update({
            'class' : 'confirm-password-input',
            'placeholder' : 'Password'
        })

    # ## the metadata for the class
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


############ forgot form #####################

# core/forms.py
from django.contrib.auth.forms import PasswordResetForm

class forgotPassword(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'email-input', 
            'placeholder': 'Enter your email'
        })



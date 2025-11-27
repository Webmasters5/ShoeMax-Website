from django import forms
from models_app.models import Customer
from django.contrib.auth.models import User
from models_app.models import PaymentMethod

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['date_of_birth', 'gender', 'phone', 'mobile','shipping_address','billing_address','credit_card',]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        # customer is set from the logged-in user in the view
        exclude = ['customer', 'card_id']
        widgets = {
            'exp_date': forms.DateInput(attrs={'type': 'date'}),
            'card_num': forms.TextInput(attrs={'inputmode': 'numeric'}),
        }
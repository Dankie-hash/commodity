from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django import forms
from .models import Commodity, Category



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError("This field is required.")
        if User.objects.filter(email=self.cleaned_data['email']).count():
            raise ValidationError("Email is taken.")
        return self.cleaned_data['email']

class SearchForm(forms.Form):
    query = forms.CharField(max_length=150)


class CreateUserForm(UserCreationForm):
    firstname = forms.CharField(max_length=150)
    lastname = forms.CharField(max_length=150)
    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError('Email is required.')
        if User.objects.filter(email=email).count():
            raise ValidationError("This email is already registered.")
        return email


class CommodityForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = ['name', 'current_price', 'opening_price', 'month', 'year', 'unit',
                  'volume', 'image']

class LoginForm(forms.Form):
    email = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)



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
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


    def save(self,password, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.password1 = password
        user.password2 = password
        user.username = self.cleaned_data["first_name"]

        if commit:
            user.save()
            return user


class CommodityForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = ['name', 'current_price', 'opening_price', 'month', 'year', 'unit',
                  'volume', 'image']

class LoginForm(forms.Form):
    email = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def save(self, user=None):
        user_profile = super(UserProfileForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile



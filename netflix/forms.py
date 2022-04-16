from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    """Registration form class."""

    firstname = forms.CharField(label="First name", max_length=30)
    lastname = forms.CharField(label="Last name", max_length=30)
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

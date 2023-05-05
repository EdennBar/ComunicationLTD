from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Users, Customers
from django.forms import ModelForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class CustomerForm(ModelForm):
    class Meta:
        model = Customers
        fields = ('name', 'address', 'phone')

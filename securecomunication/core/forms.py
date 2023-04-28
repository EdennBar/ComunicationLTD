from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Users

class RegisterForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
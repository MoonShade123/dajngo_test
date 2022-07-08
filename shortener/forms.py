from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'username')


class UserAuthenticateForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('email', 'password')



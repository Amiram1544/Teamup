from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms


class UserForm(ModelForm):
    class Meta:
        email = forms.EmailField(required=True)
        
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
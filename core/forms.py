from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class UserForm(ModelForm):
    
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
    def clean(self):
        
        cleaned_data = super().clean()
        
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2 and password1!=password2:
            raise ValidationError("Passwords mismatch")
        
        return cleaned_data
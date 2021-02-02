from .models import userprofile
from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=40,help_text='*required')
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=200, help_text='*required')

    class Meta():
        model = User
        fields = ('username','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta():
        model = userprofile
        fields = ('std',)

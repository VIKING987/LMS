from django import forms
from django import forms
from django.db.models import fields
from .models import User
import re

from authenticate import models

def checkreqpass(password):
    f = [0,0,0]
    for ch in password:
        if ch.islower():
            f[0] = 1
        if ch.isupper():
            f[1] = 1
        if ch.isnumeric():
            f[2] = 1
    
    if f[0]==0 or f[1]==0 or f[2]==0:
        return 0
    
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if(regex.search(password) == None):
        return 0

    return 1

class RegisterForm(forms.ModelForm):
    passconf = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Your Password'}) ,max_length=100, label='Confirm Your Password')
    class Meta:
        model = User
        fields = ('username', 'email', 'fname', 'lname', 'designation', 'password')
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder':'Create A Password'}),
            'username': forms.TextInput(attrs={'placeholder':'Create a unique username'}),
            'email': forms.EmailInput(attrs={'placeholder':'Enter a Valid Email'}),
            'fname': forms.TextInput(attrs={'placeholder':'Enter Your First Name'}),
            'lname': forms.TextInput(attrs={'placeholder':'Enter Your Last Name'}),
        }
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A User with this Email Already Exists!!")
        return email
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username Already in Use!!")
        if len(username)>10:
            raise forms.ValidationError("Username can't be more than 10 characters")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if not checkreqpass(password):
            raise forms.ValidationError('Password Requirements Not Satisfied')
        if len(password)<6:
            raise forms.ValidationError('Password Too Short')
        return password

    def clean(self):
        form_data = self.cleaned_data
        try:
            pass1 = form_data['password']
        except KeyError:
            pass1 = None
        pass2 = form_data['passconf']
        if pass1 and pass2:
            if pass1!=pass2:
                self._errors["password"] = ["Passwords do not match!!"]
                del form_data['password']
        return form_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder':'Enter username'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
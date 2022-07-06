from django import forms
from django.contrib.auth.models import User
from .models import Student

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'User Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Your Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    agree_term = forms.BooleanField()

# form for login

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder' : 'Your Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Your Password'}))
    remember = forms.BooleanField(required=False)

class UserDetailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username']

class StudentDetailForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['photo','program','date_of_birth','is_mentor','describe_yourself','opinion']
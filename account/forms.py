from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . import models


class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'input-field'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input-field'}))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'input-field'}))
    confirm_password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'input-field'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username

    def clean(self):
        clean_data = super().clean() #return self.cleaned_datau8
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match')


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username or Email', 'class': 'input-field'}))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'input-field'}))


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'Enter your email'
        })
    )


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input-field',
        'placeholder': 'Email'
    }))

    class Meta:
        model = models.UserBio
        fields = ["bio", "age"]
        widgets = {
            'bio': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Bio'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'input-field',
                'placeholder': 'Age'
            }),
        }
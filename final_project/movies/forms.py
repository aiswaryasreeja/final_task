# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Movie, Review
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'category', 'trailer_link']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': True, 'placeholder': 'Username', 'title': 'Enter your username'
    }))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password', 'title': 'Enter your password'
    }))
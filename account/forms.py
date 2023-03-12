from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']


GENDER = (
        ('male', 'male'),
        ('female', 'female'),
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'bio', 'avatar', 'address']
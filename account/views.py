from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile, CustomUser
from .forms import CustomUserCreationForm, UserProfileForm, UserChangeForm
import re


def register_user(request):
    '''
        takes values from a form and register user to db
    '''
    regex = '^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
    form = CustomUserCreationForm()
    context = {'form': form}
    context['has_error'] = False
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        field_vals = request.POST
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if len(username) == 0 or len(password1) == 0:
            context['has_error'] = True
            messages.error(request, 'all fields are required.')
            return render(request, 'account/register.html', context, status=400)
        if len(username) < 2 or len(username) > 8:
            context['has_error'] = True
            messages.error(request, 'username must be between 2 or 8 characters.')
            return render(request, 'account/register.html', context, status=406)
        if not username.isalnum():
            context['has_error'] = True
            messages.error(request, 'Only alpha numeric characters allowed.')
            return render(request, 'account/register.html', context, status=400)
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'account/register.html', context, status=404)
        if not (re.search(regex, email)):
            context['has_error'] = True
            messages.error(request, 'Email is invalid.')
            return render(request, 'account/register.html', context, status=400)
        if CustomUser.objects.filter(email=email).exists():
            context['has_error'] = True
            messages.error(request, 'Email already taken, choose another.')
            return render(request, 'account/register.html', context, status=409)
        if CustomUser.objects.filter(username=username).exists():
            context['has_error'] = True
            messages.error(request, 'Username already taken, choose another.')
            return render(request, 'account/register.html', context, status=409)
        if context['has_error']:
            return render(request, 'account/register.html', context, status=400)
        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.set_password(password1)
        user.save()
        login(request, user)
        return redirect('account:signin')     
    return render(request, 'account/register.html', context)


def login_user(request):
    '''
        takes values from a for and login user to site
    '''
    return render(request, 'account/login.html')

@login_required()
def profile_page(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user=request.user)
    context = {'user_profile': user_profile, 'user': user}
    return render(request, 'account/profile_page.html', context)

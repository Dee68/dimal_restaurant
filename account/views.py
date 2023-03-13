from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .models import Profile, CustomUser
from .forms import CustomUserCreationForm, UserProfileForm, CustomUserChangeForm
import re
import json


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
        if username[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            context['has_error'] = True
            messages.error(request, 'Username can not start with a number')
            return render(request, 'account/register.html', context, status=400)
        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.set_password(password1)
        user.save()
        login(request, user)
        return redirect('account:signin')     
    return render(request, 'account/register.html', context)


def validate_username(request):
    data = json.loads(request.body)
    err_str = 'Only alpha numeric characters allowed.'
    err_str1 = 'Username must be between 2 and 8 characters.'
    err_str2 = 'Sorry username already in use, choose another.'
    username = data['username']
    if not str(username).isalnum():
        return JsonResponse({'username_error': err_str}, status=400)
    if len(data['username']) <= 1 or len(data['username']) >= 9:
        return JsonResponse({'username_error': err_str1}, status=406)
    if CustomUser.objects.filter(username=username).exists():
        return JsonResponse({'username_error': err_str2}, status=409)
    return JsonResponse({'username_valid': True}, status=200)


def validate_email(request):
    regex = '^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
    data = json.loads(request.body)
    err_str = 'Sorry,email already taken, choose another one'
    err_str1 = 'Email is invalid.'
    email = data['email']
    if CustomUser.objects.filter(email=email):
        return JsonResponse({'email_error': err_str}, status=409)
    if (re.search(regex, email)):
        return JsonResponse({'email_valid': True}, status=200)
    else:
        return JsonResponse({'email_error': err_str1}, status=400)


def login_user(request):
    '''
        takes values from a for and login user to site
    '''
    context = {
        'data': request.POST,
        'has_error': False
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == '' or password == '':
            context['has_error'] = True
            messages.error(request, 'All fields are required')
            return render(request, 'account/login.html', context, status=400)
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome {username}')
                return redirect('restaurant:home')
            context['has_error'] = True
            messages.error(request, 'Invalid Credentials')
            return render(request, 'account/login.html', context, status=401)
    return render(request, 'account/login.html', context)


def confirm_page(request):
    form = request.POST
    if request.method == 'POST':
        if form.get('yes'):
            logout(request)
            messages.success(request, 'You are now logged out.')
            return redirect('restaurant:home')
        else:
            return redirect('restaurant:home')
    return render(request, 'account/confirm.html')


def logout_page(request):
    return render(request, 'account/confirm.html')


@login_required()
def profile_page(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user=request.user)
    context = {'user_profile': user_profile, 'user': user}
    return render(request, 'account/profile_page.html', context)

@login_required(login_url='account/signin')
def profile_update(request):
    user_profile = Profile.objects.get(user_id=request.user.id)
    post_data = request.POST or None
    if request.method == 'POST':
        user_form = CustomUserChangeForm(post_data, instance=request.user)
        profile_form = UserProfileForm(post_data, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return HttpResponseRedirect(reverse_lazy('account:profile'))       
        messages.error(request, 'Something went wrong.')
        context={'user_form': user_form, 'profile_form': profile_form, 'user_profile': user_profile}
        return render(request, 'account/update_profile.html', context )
    user_form = CustomUserChangeForm(instance=request.user)
    profile_form = UserProfileForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form, 'user_profile': user_profile}
    return render(request, 'account/update_profile.html', context)

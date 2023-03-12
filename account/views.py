from django.shortcuts import render


def register_user(request):
    '''
        takes values from a for and register user to db
    '''
    return render(request, 'account/register.html')


def login_user(request):
    '''
        takes values from a for and login user to site
    '''
    return render(request, 'account/login.html')

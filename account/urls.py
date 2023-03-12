from django.urls import path
from . import views

app_name = 'account'


urlpatterns = [
   path('', views.profile_page, name='profile'),
   path('register', views.register_user, name='register'),
   path('signin', views.login_user, name='signin')
]

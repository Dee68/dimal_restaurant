from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'account'


urlpatterns = [
   path('', views.profile_page, name='profile'),
   path('update-profile/', views.profile_update, name='update-profile'),
   path('register', views.register_user, name='register'),
   path('signin', views.login_user, name='signin'),
   path('logout', views.logout_page, name='logout'),
   path('validate-username', csrf_exempt(views.validate_username), name='validate-username'),
   path('validate-email', csrf_exempt(views.validate_email), name='validate-email'),
   path('confirmation', views.confirm_page, name='confirmation'),
]

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=8,unique=True)
    email = models.EmailField(_('email address'),unique=True)

    # USERNAME_FIELD = email
    # REQUIRED_FIELDS = ['username','email','password1','password2']

    def __str__(self):
        return str(self.username)


class Profile(models.Model):
    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, choices=GENDER, default='male')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, upload_to='profile_pics/')
    address = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def image_tag(self):
        if self.avatar:
            return mark_safe('<img src="%s" height="50" width="50">' %self.avatar.url)
        return "No image found"
    image_tag.short_description = 'Avatar'

    def __str__(self):
        return str(f"{self.user.username.capitalize()}'s Profile")
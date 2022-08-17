from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class AbsrtactModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser):   
    email = models.EmailField(('email address'), blank=True, unique=True)
    image = models.ImageField(upload_to='profile_images')
    is_teacher = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return str(self.username)

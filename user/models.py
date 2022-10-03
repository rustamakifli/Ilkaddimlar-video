from pickle import TRUE
from django.db import models
from django.contrib.auth.models import AbstractUser

# # Create your models here.

class User(AbstractUser):
    birthday = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=6,choices=(('male','male'),('female','female')),default='female')
    mobile = models.CharField(max_length=15,null=True,blank=True)   
    email = models.EmailField(('email address'), blank=True, unique=True)
    image = models.ImageField(upload_to='profile_images')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    

    def __str__(self):
        return str(self.username)




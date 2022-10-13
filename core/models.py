from enum import unique
from django.db import models

from ckeditor.fields import RichTextField
from embed_video.fields  import  EmbedVideoField


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 


class Contact(AbstractModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=40)
    message = models.TextField()
    is_answered = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.name


class Subscriber(AbstractModel):
    email = models.EmailField("Email", unique = True, max_length=40)
    is_active = models.BooleanField("Is active", default=True)
    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'

    def __str__(self):
        return self.email

class HomeSettings(AbstractModel):
    title = models.CharField(max_length= 150, unique = True,)
    text = RichTextField(verbose_name = "İLK ADDIMLAR HAQQINDA")
    video = EmbedVideoField(verbose_name = "Home Page üçün video link")
    is_active = models.BooleanField()

    class Meta:
        verbose_name = 'Home Setting'
        verbose_name_plural = 'Home  Settings'

    def __str__(self):
        return self.title
  

class SliderImage(AbstractModel):
    title = models.CharField(max_length= 150)
    slider_image =  models.ImageField(
        upload_to='slider_image',
    )
    settings = models.ForeignKey(HomeSettings,on_delete=models.CASCADE,related_name='slider_image')

    def __str__(self):
        return self.title
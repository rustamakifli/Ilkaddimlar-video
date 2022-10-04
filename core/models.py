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

class WebsiteSettings(AbstractModel):
    about_text = RichTextField()
    about_video = EmbedVideoField()
    number_of_videos = models.IntegerField()
    number_of_users = models.IntegerField()
    number_of_teachers = models.IntegerField()

    class Meta:
        verbose_name = 'Website Settings'
        verbose_name_plural = 'Website  Settings'

  

class SliderImage(AbstractModel):
    title = models.CharField(max_length= 150)
    slider_image =  models.ImageField(
        upload_to='slider_image',
    )
    settings = models.ForeignKey(WebsiteSettings,on_delete=models.CASCADE,related_name='slider_image')
    def __str__(self):
        return self.title
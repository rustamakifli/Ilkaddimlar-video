from django.db import models


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
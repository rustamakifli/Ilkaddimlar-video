from django.db.models.signals import pre_save, post_save
from gallery.models import Category
from django.dispatch import receiver
from django.utils.text import slugify



@receiver(post_save, sender = Category)
def category_slug_create_func(sender, instance, created, **kwargs):
    old_slug = instance.slug
    new_slug = f"{slugify(instance.title)}"
    if old_slug != new_slug:
        instance.slug = new_slug
        instance.save()

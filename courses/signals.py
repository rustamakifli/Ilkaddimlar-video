from django.db.models.signals import pre_save, post_save
from courses.models import Course, Author
from django.dispatch import receiver
from django.utils.text import slugify


@receiver(pre_save, sender = Course)
def calculate_discounted_price (sender, instance, **kwargs):
    try:
        if instance.discount.percentage:
            discount = float(instance.price)*float(instance.discount.percentage)/100
        elif instance.discount.value:
            discount = float(instance.discount.value)
        result = float(instance.price)-discount
        instance.discounted_price = result
    except:
        instance.discounted_price = float(instance.price)


@receiver(post_save, sender = Course)
def course_slug_create_func(sender, instance, created, **kwargs):
    old_slug = instance.slug
    new_slug = f"{slugify(instance.title)}"
    if old_slug != new_slug:
        instance.slug = new_slug
        instance.save()


@receiver(post_save, sender = Author)
def author_slug_create_func(sender, instance, created, **kwargs):
    old_slug = instance.slug
    new_slug = f"{slugify(instance.name)}"
    if old_slug != new_slug:
        instance.slug = new_slug
        instance.save()
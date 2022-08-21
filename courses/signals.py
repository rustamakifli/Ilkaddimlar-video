from django.db.models.signals import pre_save
from courses.models import Course
from django.dispatch import receiver


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
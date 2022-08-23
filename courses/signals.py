from django.db.models.signals import pre_save
from courses.models import Course, Chapter, Lesson
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


@receiver(pre_save, sender = Course)
def course_duration (sender, instance, **kwargs):
    instance.duration = instance.course_duration

@receiver(pre_save, sender = Chapter)
def chapter_duration (sender, instance, **kwargs):
    instance.duration = instance.chapter_duration

@receiver(pre_save, sender = Lesson)
def lesson_duration (sender, instance, **kwargs):
    instance.duration = instance.lesson_duration
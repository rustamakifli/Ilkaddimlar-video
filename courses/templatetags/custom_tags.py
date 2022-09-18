
from django.template import Library
from courses.models import *
from django.db.models import Count

register = Library()


@register.simple_tag
def get_all_courses():
    return Course.objects.filter(is_active=True)

@register.simple_tag
def get_discounted_courses():
    return Course.objects.filter(discount__isnull=False)

@register.simple_tag
def get_categories():
    return Category.objects.annotate(number_of_courses = Count("category_courses")).all()

@register.simple_tag
def get_popularcourses():
    return Course.objects.all()[0:3]

@register.simple_tag
def get_tags():
    return Tag.objects.all()

@register.simple_tag
def get_authors():
    return Author.objects.annotate(number_of_courses = Count("author_courses")).all()[0:6]

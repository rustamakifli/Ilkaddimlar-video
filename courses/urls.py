from django.urls import path
from courses.views import get_courses

urlpatterns = [
    path('courses/', get_courses, name='courses'),
]
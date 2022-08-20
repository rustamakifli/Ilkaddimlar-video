from django.urls import path
from courses.views import get_courses
# ,courses

urlpatterns = [
    path('courses/', get_courses, name='courses'),
    # path('courses/<int:pk>', courses, name='single_courses'),

]
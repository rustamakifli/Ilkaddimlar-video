from django.urls import path
from courses import views as template_views
# ,courses

urlpatterns = [
    path('courses/', template_views.PaginatorCourseList, name='courses'),
    path('search/', template_views.SearchView.as_view(), name="search"),
    # path('courses/<int:pk>', courses, name='single_courses'),

]
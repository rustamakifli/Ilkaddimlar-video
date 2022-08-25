from django.urls import path
from courses import views as template_views

urlpatterns = [
    # path('courses/', template_views.PaginatorCourseList, name='courses'),
    path('courses/', template_views.CourseListView.as_view(), name='courses'),
    path('courses/<int:pk>', template_views.CourseDetailView.as_view(), name='single_courses'),
    path('search/', template_views.SearchView.as_view(), name="search"),
    path('comments/<int:pk>/', template_views.EditCommentView.as_view(), name='edit_comment'),
]
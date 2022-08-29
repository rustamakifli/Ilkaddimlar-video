from django.urls import path
from courses import views as template_views

urlpatterns = [
    path('courses/', template_views.CourseListView.as_view(), name='courses'),
    path('courses/<int:pk>', template_views.CourseDetailView.as_view(), name='single_courses'),
    path('search/', template_views.SearchView.as_view(), name="search"),
    path('comments/<int:pk>/update', template_views.UpdateCommentView.as_view(), name='edit_comment'),
    path('comments/<int:pk>/delete', template_views.DeleteCommentView.as_view(), name='delete_comment'),
    path('authors/<int:pk>', template_views.AuthorDetailView.as_view(), name='author_detail'),
    path('studentcourses/', template_views.UserCoursesListView.as_view(), name='student_courses'),
    path('comments/add', template_views.CommentCreateView.as_view(), name='create_comment'),
    # path('studentcourses/add', template_views.ApplyStudentCreateView.as_view(), name='apply_course'),
]
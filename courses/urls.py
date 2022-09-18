from django.urls import path
from courses import views as template_views

urlpatterns = [
    path('courses/', template_views.CourseListView.as_view(), name='courses'),
    path('courses/<slug:slug>', template_views.CourseDetailView.as_view(), name='single_courses'),
    path('search/', template_views.SearchView.as_view(), name="search"),
    path('comments/<int:pk>/update', template_views.UpdateCommentView.as_view(), name='edit_comment'),
    path('comments/<int:pk>/delete', template_views.DeleteCommentView.as_view(), name='delete_comment'),
    path('authors/<slug:slug>', template_views.AuthorDetailView.as_view(), name='author_detail'),
    path('studentcourses/', template_views.UserCoursesListView.as_view(), name='student_courses'),
    path('single_blog/', template_views.SingleBlogView.as_view(), name="single_blog"),
    path('blog/', template_views.BlogView.as_view(), name="blog"),
    path('home/', template_views.HomeView.as_view(), name="home"),
    path('gallery/', template_views.GalleryView.as_view(), name="gallery"),
    path('contact/', template_views.ContactView.as_view(), name="contact"),

]
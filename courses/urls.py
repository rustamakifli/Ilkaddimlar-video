from django.urls import path
from courses import views as template_views

urlpatterns = [
    path('courses/', template_views.CourseListView.as_view(), name='courses'),
    path('courses/<slug:slug>', template_views.CourseDetailView.as_view(), name='single_courses'),
    path('search/', template_views.SearchView.as_view(), name="search"),
    path('comments/<int:pk>/update', template_views.UpdateCommentView.as_view(), name='edit_comment'),
    path('comments/<int:pk>/delete', template_views.DeleteCommentView.as_view(), name='delete_comment'),
    path('404/', template_views.ErrorView.as_view(), name="404"),
    path('u_courses/', template_views.UserCourseView.as_view(), name='u_courses'),
    path("wishlist/", template_views.wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", template_views.add_to_wishlist, name="user_wishlist"),
    path('authors/', template_views.AuthorListView.as_view(), name='authors'),
    path('authors/<slug:slug>', template_views.AuthorDetailView.as_view(), name='author_detail'),

]
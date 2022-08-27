from django.urls import path
from courses.api import views as api_views


urlpatterns = [
    path('categories/', api_views.CategoryListCreateAPIView.as_view(), name="category-list"),
    path('categories/<int:pk>', api_views.CategoryDetailAPIView.as_view(), name="category-detail"),

    path('tags/', api_views.TagListCreateAPIView.as_view(), name="tag-list"),
    path('tags/<int:pk>', api_views.TagDetailAPIView.as_view(), name="tag-detail"),

    path('courses/', api_views.CourseListCreateAPIView.as_view(), name="course-list"),
    path('courses/<int:pk>', api_views.CourseDetailAPIView.as_view(), name="course-detail"),
    path('courses/<int:pk>/comments', api_views.CommentListCreateAPIView.as_view(), name="comment-list"),

    path('comments/', api_views.CommentListCreateAPIView.as_view(), name="comment-list"),
    path('comments/<int:pk>', api_views.CommentDetailAPIView.as_view(), name="comment-detail"),

    path('chapters/', api_views.ChapterListCreateAPIView.as_view(), name="chapter-list"),
    path('chapters/<int:pk>', api_views.ChapterDetailAPIView.as_view(), name="chapter-detail"),

    path('lessons/', api_views.LessonListCreateAPIView.as_view(), name="lesson-list"),
    path('lessons/<int:pk>', api_views.LessonDetailAPIView.as_view(), name="lesson-detail"),

    path('discounts/', api_views.DiscountListCreateAPIView.as_view(), name="discount-list"),
    path('discounts/<int:pk>', api_views.DiscountDetailAPIView.as_view(), name="discount-detail"),

    path('studentcourses/', api_views.StudentCourseListCreateAPIView.as_view(), name="student-course-list"),
    path('studentcourses/<int:pk>', api_views.StudentCourseDetailAPIView.as_view(), name="student-course-detail"),
]



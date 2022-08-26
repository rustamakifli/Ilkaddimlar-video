from rest_framework import generics
from rest_framework.response import Response
# from rest_framework.generics import get_object_or_404

from courses.api.serializers import (
    CategorySerializer, TagSerializer, CommentSerializer, DiscountSerializer, CourseSerializer,
    ChapterSerializer, LessonSerializer, StudentCourseSerializer)

from courses.models import (Category, StudentCourse, Tag, Course, Chapter, Lesson, Comment, Discount)


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        queryset = Course.objects.filter(is_active=True)
        featured = request.GET.get('featured')
        tags = request.GET.get('tags')
        category = request.GET.get('category')
        if category:
            queryset = queryset.filter(category__id=category)
        if tags:
            queryset = queryset.filter(tags__id=tags) 
        if featured:
            queryset = queryset.filter(featured=featured)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ChapterListCreateAPIView(generics.ListCreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


class ChapterDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class DiscountListCreateAPIView(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class DiscountDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class StudentCourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
    

class StudentCourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
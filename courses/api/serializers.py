from rest_framework import serializers
from courses.models import (Category, Tag, Course, Chapter, Lesson, Comment, Discount, StudentCourse)


class CategorySerializer(serializers.ModelSerializer):

    category_courses = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='course-detail',
    )
    parent_cat = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_parent_cat(self,obj):
        if obj.parent_cat:
            return obj.parent_cat.title
        return "None"


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, required=False)
    course_chapters = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='chapter-detail',
    )
    course_comments = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='comment-detail',
    )
    user = serializers.StringRelatedField(read_only=True)
    discount = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    course_duration = serializers.SerializerMethodField()
        
    def get_course_duration(self, obj):
        return obj.course_duration

    class Meta:
        model = Course
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):

    chapter_lessons = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='lesson-detail',
    )
    course = serializers.StringRelatedField(read_only=True)
    chapter_duration = serializers.SerializerMethodField()
        
    def get_chapter_duration(self, obj):
        return obj.chapter_duration

    class Meta:
        model = Chapter
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    chapter = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'

class StudentCourseSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StudentCourse
        fields = '__all__'
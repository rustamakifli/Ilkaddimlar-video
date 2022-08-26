from django.contrib import admin
from csv import *
from courses.models import *
from nested_admin import NestedModelAdmin, NestedTabularInline, NestedStackedInline


class LessonInline(NestedTabularInline):
    model = Lesson
    extra = 0


class ChapterInline(NestedStackedInline):
    model = Chapter
    extra = 0
    inlines = [LessonInline]


class CoursesAdmin(NestedModelAdmin):
    model = Course
    extra = 0
    inlines = [ChapterInline]
    classes = ["collapse"]

admin.site.register( Course,CoursesAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title',)
    search_fields = ('title', )
    classes = ['collapse']

admin.site.register(Category, CategoryAdmin) 

class TagAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title',)
    search_fields = ('title', )
    classes = ['collapse']

admin.site.register(Tag, TagAdmin) 


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title',)
    search_fields = ('title', )
    classes = ['collapse']

admin.site.register(Discount, DiscountAdmin) 


class CommentAdmin(admin.ModelAdmin):
    list_filter = ('user', 'rating','course')
    search_fields = ('comment', 'user', 'rating','course')
    readonly_fields = ["user",]
    ordering = ('-confirm',)

admin.site.register(Comment, CommentAdmin)

class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('user','course','add_time')
    list_filter = ('user','course','add_time')
    search_fields = ('user','course','add_time')

admin.site.register(StudentCourse, StudentCourseAdmin)
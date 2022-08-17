from django.contrib import admin
from csv import *
from courses.models import *
from nested_admin import NestedModelAdmin, NestedTabularInline, NestedStackedInline

class VideoInline(NestedTabularInline):
    model = Videos
    extra = 5

class ChapterInline(NestedStackedInline):
    model = Chapter
    extra = 1
    inlines = [VideoInline]

class CoursesAdmin(NestedModelAdmin):
    model = Course
    extra = 1
    inlines = [ChapterInline]
    classes = ["collapse"]

# class CoursesAdmin(NestedModelAdmin):
#     inlines = [CourseInline,]

admin.site.register( Course,CoursesAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title',)
    search_fields = ('title', )
    classes = ['collapse']
    

class CommentAdmin(admin.ModelAdmin):
    list_filter = ('user', 'rating',)
    search_fields = ('comment', 'user', 'rating',)
    readonly_fields = ["user",]
    ordering = ('-confirm',)
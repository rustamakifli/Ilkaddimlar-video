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
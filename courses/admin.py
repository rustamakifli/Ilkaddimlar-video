from django.contrib import admin
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
    exclude = ('users_wishlist',)
    model = Course
    extra = 0
    inlines = [ChapterInline]
    classes = ["collapse"]
    readonly_fields = ["discounted_price",]

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


class AuthorAdmin(admin.ModelAdmin):
    classes = ['collapse']

admin.site.register(Author, AuthorAdmin) 


class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_comment', 'confirm' )
    list_filter = ('user', 'rating','course')
    search_fields = ('comment', 'course', 'user', 'rating',)
    readonly_fields = ["user",]
    ordering = ('-confirm',)

    def get_comment(self, obj):
        return obj.comment[:100]


admin.site.register(Comment, CommentAdmin)


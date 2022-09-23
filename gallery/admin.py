from django.contrib import admin
from gallery.models import Category, Gallery


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_filter = ('title', 'slug')
    search_fields = ('title', )
    classes = ['collapse']

admin.site.register(Category, CategoryAdmin) 


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title',  )
    list_filter = ('title',)
    search_fields = ('title', )
    classes = ['collapse']

admin.site.register(Gallery, GalleryAdmin) 
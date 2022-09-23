from django.contrib import admin
from core.models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_answered' )
    list_filter = ('name', 'is_answered' )
    search_fields = ('name', )
    classes = ['collapse']

admin.site.register(Contact, ContactAdmin) 

from django.contrib import admin
from core.models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name',)
    search_fields = ('name', )
    classes = ['collapse']

admin.site.register(Contact, ContactAdmin) 

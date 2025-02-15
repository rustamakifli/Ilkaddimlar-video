from django.contrib import admin
from core.models import Contact, Subscriber,HomeSettings, SliderImage
from nested_admin import NestedModelAdmin, NestedTabularInline


class SliderImageInline(NestedTabularInline):
    model = SliderImage
    extra = 2


class HomeSettingsAdmin(NestedModelAdmin): 
    model = HomeSettings
    extra = 1 
    inlines = [SliderImageInline]
    classes = ["collapse"]

admin.site.register( HomeSettings,HomeSettingsAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_answered' )
    list_filter = ('name', 'is_answered' )
    search_fields = ('name', )
    classes = ['collapse']

admin.site.register(Contact, ContactAdmin) 


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', )
    list_filter = ('email', )
    search_fields = ('email', )
    classes = ['collapse']

admin.site.register(Subscriber, SubscriberAdmin) 

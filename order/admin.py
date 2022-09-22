from django.contrib import admin
from order.models import Cart,Cart_Item,Coupon
# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_ordered',)
    list_editable = ('is_ordered',)

    fieldsets = (
        ('Cart information', {
         'fields': ('get_user_username', 'is_ordered', 'ordered_at')}),
    )
    readonly_fields = ('get_user_username',)

    def get_user_username(self, obj):
        return obj.user.username
    get_user_username.short_description = 'Username'




@admin.register(Cart_Item)
class Cart_ItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'course', 'price', 'get_cart_detail')


    def get_cart_detail(self, obj):
        return obj.cart.is_ordered
    get_cart_detail.short_description = 'Is Ordered?'



class CouponAdmin(admin.ModelAdmin):
    list_display = ('code','used')
    list_filter = ('code','used')
    search_fields = ('code', )
    classes = ['collapse']

admin.site.register(Coupon, CouponAdmin) 
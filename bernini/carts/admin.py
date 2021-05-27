from django.contrib import admin
from carts.models import Cart, ItemCart

class CartAdmin(admin.ModelAdmin):
    pass

class ItemCartAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cart, CartAdmin)
admin.site.register(ItemCart, ItemCartAdmin)

from django.contrib import admin
from .models import Product, CartItem, Profile, Category, WishlistItem

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(WishlistItem)
# Register your models here.

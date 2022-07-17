from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from .models import Category, ProductAttribute, Product


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'state', 'active', 'photo')
    list_filter = ['category', 'state', 'active']

    def photo(self, obj):
        return format_html('<img src={}  width="auto" height="100" />', obj.img.url)


# admin.site.register(ProductoAdmin)

admin.site.register(Category, )
admin.site.register(ProductAttribute, )
admin.site.register(Product, ProductoAdmin)

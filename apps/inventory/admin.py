from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from .models import Category, ProductAttribute, Product


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'state', 'active', 'photo')
    list_filter = ['category', 'state', 'active']

    def photo(self, obj):
        return format_html('<img src={} style="width: 50px; height: 50px; border-radius: 50px;" />', obj.img)


# admin.site.register(ProductoAdmin)

admin.site.register(Category, )
admin.site.register(ProductAttribute, )
admin.site.register(Product, ProductoAdmin)

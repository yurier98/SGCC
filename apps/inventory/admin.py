from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
# Register your models here.

from .models import Category, ProductAttribute, Product


@admin.register(Product)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'state', 'active', 'photo')
    list_filter = ['category', 'state', 'active']

    def photo(self, obj):
        return format_html('<img src={} style="width: 50px; height: 50px; border-radius: 8px;" />', obj.img.url)



@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('is_active', 'name', 'created_date', 'modified_date')
    list_filter = ['is_active', 'created_date', 'modified_date']
    # list_editable = ['is_active']
    # list_display_links = ['name']
    list_editable = ['is_active', 'name']
    list_display_links = None


# admin.site.register(ProductoAdmin)
admin.site.register(ProductAttribute)


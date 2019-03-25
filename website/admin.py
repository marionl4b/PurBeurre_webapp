from django.contrib import admin
from .models.category import Category
from .models.product import Product


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('id', 'name', 'API_link', 'nutriscore')
    list_filter = ('categories', 'nutriscore')
    readonly_fields = ('favorites',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

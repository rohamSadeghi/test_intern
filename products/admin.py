from django.contrib import admin

from products.models import Store, Product, ProductRating, Category, ProductBookmark

# admin.site.register(Store)
# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(ProductRating)
# admin.site.register(ProductBookmark)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_enable', 'created_time']
    list_filter = ['is_enable', ]
    raw_id_fields = ['parent',]
    search_fields = ['name',]
    actions = ['set_enable', 'set_disable']

    def set_enable(self, request, queryset):
        queryset.filter(is_enable=False).update(is_enable=True)

    def set_disable(self, request, queryset):
        queryset.filter(is_enable=True).update(is_enable=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_enable', 'created_time']
    list_filter = ['is_enable', ]
    autocomplete_fields = ['categories', ]
    search_fields = ['name', ]


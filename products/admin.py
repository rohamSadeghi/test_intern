from django.contrib import admin

from products.models import Store, Product, ProductRating, Category, ProductBookmark

admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductRating)
admin.site.register(ProductBookmark)

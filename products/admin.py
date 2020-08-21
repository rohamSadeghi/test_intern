from django.contrib import admin

from products.models import Store, Product, ProductRating

admin.site.register(Store)
admin.site.register(Product)
admin.site.register(ProductRating)

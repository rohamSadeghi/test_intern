from django.urls import path

from products.views import product_detail_view, products_list, stores_list, create_product

urlpatterns = [
    path('<int:pk>/', product_detail_view, name='product-detail'),
    path('', products_list, name='products-list'),
    path('stores/', stores_list, name='stores-list'),
    path('create-product/', create_product, name='create-product')
]
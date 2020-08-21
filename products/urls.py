from django.urls import path

from products.views import (
    product_detail_view,
    products_list,
    stores_list,
    create_product,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView, RateView
)

urlpatterns = [
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('', ProductListView.as_view(), name='products-list'),
    path('stores/', stores_list, name='stores-list'),
    path('create-product/', ProductCreateView.as_view(), name='create-product'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/rate/', RateView.as_view(), name='product-rate'),
]
from django.urls import path, include

from products.views import (
    product_detail_view,
    products_list,
    stores_list,
    create_product,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView, RateView, RateDeleteView, CategoryListView, CategoryDetailView, BookmarkCreateView
)

urlpatterns = [
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/bookmark/', BookmarkCreateView.as_view(), name='bookmark'),
    # path('categories/', CategoryListView.as_view(), name='categories-list'),
    # path('categories/<int:pk>/', CategoryDetailView.as_view(), name='categories-detail'),
    path('', ProductListView.as_view(), name='products-list'),
    path('stores/', stores_list, name='stores-list'),
    path('create-product/', ProductCreateView.as_view(), name='create-product'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/rate/', RateView.as_view(), name='product-rate'),
    path('<int:pk>/rate-delete/', RateDeleteView.as_view(), name='product-rate-delete'),

    # APIs
    path('api/', include('products.api.urls')),
]
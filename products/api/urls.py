from django.urls import path

from products.api.views import InitialView, ProductViewSet, CategoryViewSet

urlpatterns = [
    path('initial/', InitialView.as_view(), name='initial'),
    path('categories/', CategoryViewSet.as_view({'get': 'list'}), name='categories-list'),
    path('categories/<int:id>/', CategoryViewSet.as_view({'get': 'retrieve'}), name='category-detail'),
    path('products/', ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve'}), name='product-list'),

]

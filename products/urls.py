from django.urls import path

from products.views import product_detail_view, products_list

urlpatterns = [
    path('<int:pk>/', product_detail_view),
    path('', products_list),
]
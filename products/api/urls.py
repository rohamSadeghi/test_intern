from django.urls import path, include
from rest_framework.routers import SimpleRouter

from products.api.views import InitialView, ProductViewSet, CategoryViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)


urlpatterns = [
    path('initial/', InitialView.as_view(), name='initial'),
    path('', include(router.urls),),

]

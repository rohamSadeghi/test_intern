from django.urls import path, include
from rest_framework.routers import SimpleRouter

from commenting.api.views import CommentViewSet

router = SimpleRouter()
router.register('', CommentViewSet)

urlpatterns = [
    path('', include(router.urls),),

]

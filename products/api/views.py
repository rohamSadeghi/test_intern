from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from products.api.serializers import ProductSerializer, CategorySerializer
from products.models import Product, Category


class InitialView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"Initial": "Hello World"})

    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(data)


class CategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_url_kwarg = 'id'


class ProductViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_enable=True)

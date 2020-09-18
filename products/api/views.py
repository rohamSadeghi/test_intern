from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from commenting.api.serializers import CommentSerializer
from commenting.models import ProductComment
from products.api.serializers import ProductSerializer, CategorySerializer, BookmarkSerializer, RatingSerializer
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
    # lookup_url_kwarg = 'id'

    # def retrieve(self, request, *args, **kwargs):
    #     category = self.get_object()
    #     related_products = Product.objects.filter(categories=category)
    #     serializer = ProductSerializer(related_products, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        products_properties = {}
        for p in category.properties:
            products_properties[p] = Product.objects.filter(
                    categories=category
                ).values_list(f'properties__{p}', flat=True).distinct()

        return Response(products_properties)


class ProductViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_enable=True)

    @action(methods=['post'], detail=True)
    def bookmark(self, request, *args, **kwargs):
        user = request.user
        product = self.get_object()
        serializer = BookmarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def rate(self, request, *args, **kwargs):
        user = request.user
        product = self.get_object()
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True)
    def comments(self, request, *args, **kwargs):
        product = self.get_object()
        related_comments = ProductComment.approves.filter(product=product)
        serializer = CommentSerializer(related_comments, many=True)
        return Response(serializer.data)

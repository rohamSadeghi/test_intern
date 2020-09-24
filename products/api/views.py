from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from commenting.api.serializers import CommentSerializer
from commenting.models import ProductComment
from products.api.serializers import ProductSerializer, CategorySerializer, BookmarkSerializer, RatingSerializer
from products.filters import CustomOrdering
from products.models import Product, Category


class InitialView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"Initial": "Hello World"})

    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(data)


class CategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.parents.all()
    # lookup_url_kwarg = 'id'

    # def retrieve(self, request, *args, **kwargs):
    #     category = self.get_object()
    #     related_products = Product.objects.filter(categories=category)
    #     serializer = ProductSerializer(related_products, many=True)
    #     return Response(serializer.data)

    def get_queryset(self):
        if self.action == 'retrieve':
            return Category.objects.all()
        return super().get_queryset()

    # def retrieve(self, request, *args, **kwargs):
    #     category = self.get_object()
    #     products_properties = {}
    #     for p in category.properties:
    #         products_properties[p] = Product.objects.filter(
    #                 categories=category
    #             ).values_list(f'properties__{p}', flat=True).distinct()
    #
    #     return Response(products_properties)


class ProductViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, CustomOrdering, SearchFilter]
    search_fields = ['name', 'categories__name']
    ordering_fields = ['id', 'name', 'rating_avg', 'rating_count']
    # filter_fields = ['id', 'categories']
    filter_fields = {'price': ['lt', 'gt']}
    queryset = Product.objects.filter(is_enable=True)

    def get_serializer_class(self):
        serializers_class = {
            'bookmark': BookmarkSerializer,
            "rate": RatingSerializer,
            "add_comment": CommentSerializer
        }
        return serializers_class.get(self.action) or super().get_serializer_class()

    @action(methods=['post'], detail=True)
    def bookmark(self, request, *args, **kwargs):
        user = request.user
        product = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def rate(self, request, *args, **kwargs):
        user = request.user
        product = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True)
    def comments(self, request, *args, **kwargs):
        product = self.get_object()
        related_comments = ProductComment.approves.filter(product=product)
        serializer = CommentSerializer(related_comments, many=True)
        return Response(serializer.data)

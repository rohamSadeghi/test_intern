from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
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
from rest_framework_simplejwt.authentication import JWTAuthentication

from commenting.api.serializers import CommentSerializer
from commenting.models import ProductComment
from products.api.serializers import ProductSerializer, CategorySerializer, BookmarkSerializer, RatingSerializer
from utils.filters import CustomOrdering
from products.models import Product, Category
from utils.paginations import CustomLimitOffsetPagination, CustomPageNumberPagination


class InitialView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"Initial": "Hello World"})

    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(data)


class CategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.parents.filter(is_enable=True).all()
    pagination_class = CustomPageNumberPagination
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

    @method_decorator(cache_page(30))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_enable=True)
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticatedOrReadOnly,]
    pagination_class = CustomLimitOffsetPagination
    filter_backends = [DjangoFilterBackend, CustomOrdering, SearchFilter]
    search_fields = ['name', 'categories__name']
    ordering_fields = ['id', 'name', 'rating_avg', 'rating_count']
    # filter_fields = ['id', 'categories']
    filter_fields = {'price': ['lt', 'gt'], 'categories__id': ['in',]}


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

from rest_framework import serializers

from products.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time', ]

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'categories', 'description', 'rating_avg', 'rating_count']

from rest_framework import serializers

from products.models import Product, Category, ProductBookmark, ProductRating


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time', ]

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    user_rate = serializers.SerializerMethodField()
    user_bookmark = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'image',
            'categories', 'description', 'user_rate', 'user_bookmark', 'rating_avg',
            'rating_count'
        ]

    def get_user_rate(self, obj):
        request = self.context['request']
        user = request.user
        if user and user.is_authenticated:
            try:
                rate = ProductRating.objects.get(user=user, product=obj).rate
            except ProductRating.DoesNotExist:
                pass
            else:
                return rate

    def get_user_bookmark(self, obj):
        request = self.context['request']
        user = request.user
        if user and user.is_authenticated:
            try:
                bookmark = ProductBookmark.objects.get(user=user, product=obj).like_status
            except ProductBookmark.DoesNotExist:
                pass
            else:
                return bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    like_status = serializers.BooleanField(required=True)

    class Meta:
        model = ProductBookmark
        fields = ['user', 'like_status', 'product']
        read_only_fields = ['user', 'product']

    def create(self, validated_data):
        like_status = {'like_status': validated_data.pop('like_status', False)}
        instance, _created = ProductBookmark.objects.update_or_create(
            **validated_data,
            defaults=like_status
        )
        return instance


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['rate',]

    def create(self, validated_data):
        rate = {'rate': validated_data.pop('rate')}
        instance, _created = ProductRating.objects.update_or_create(
            **validated_data,
            defaults=rate
        )
        return instance

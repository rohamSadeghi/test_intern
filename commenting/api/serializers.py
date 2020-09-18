from rest_framework import serializers

from commenting.models import ProductComment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ['id', 'product', 'user', 'content']

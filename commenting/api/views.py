from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from commenting.api.serializers import CommentSerializer, VoteSerializer
from commenting.models import ProductComment


class CommentViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = CommentSerializer
    queryset = ProductComment.approves.all()
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def list(self, request, *args, **kwargs):
        product_id = request.query_params.get('product')
        if product_id:
            try:
                product_id = int(product_id)
            except ValueError:
                pass
            else:
                related_comments = ProductComment.approves.filter(product_id=product_id)
                serializer = self.get_serializer(related_comments, many=True)
                return Response(serializer.data)

        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def vote(self, request, *args, **kwargs):
        comment = self.get_object()
        user = request.user
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, comment=comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

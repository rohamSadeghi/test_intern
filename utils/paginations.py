from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = 'l'
    offset_query_param = 'o'
    default_limit = 2


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'p'

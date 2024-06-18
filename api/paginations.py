from rest_framework.pagination import PageNumberPagination


class SmallPagination(PageNumberPagination):
    page_size = 12
    page_query_param = 'offset'
    page_size_query_param = 'limit'
    max_page_size = 100


class MediumPagination(PageNumberPagination):
    page_size = 24
    page_query_param = 'offset'
    page_size_query_param = 'limit'
    max_page_size = 200


class LargePagination(PageNumberPagination):
    page_size = 100
    page_query_param = 'offset'
    page_size_query_param = 'limit'
    max_page_size = 1000
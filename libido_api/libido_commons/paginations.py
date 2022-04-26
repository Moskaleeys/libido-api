from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import CursorPagination


class CommonPagination(PageNumberPagination):
    page_size = 20
    # page_size_query_param = 'page_size'
    max_page_size = 20


class SearchPagination(PageNumberPagination):
    page_size = 20
    # page_size_query_param = 'page_size'
    max_page_size = 50000


class CommonCursorPagination(CursorPagination):
    page_size = 50
    max_page_size = 250
    ordering = "-id"

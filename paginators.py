from rest_framework.pagination import CursorPagination

class OverrideCursorPaginator(CursorPagination):
    ordering = 'id'
    page_size = 5
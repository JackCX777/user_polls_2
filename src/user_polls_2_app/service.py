from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginationPolls(PageNumberPagination):
    page_size = 2
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'links': {'next': self.get_next_link(), 'previous': self.get_previous_link()},
            'results': data
        })

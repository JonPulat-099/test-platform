from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    TODO: 1. page size should be customized to query param number |inside Response, it is called: 'per_page': self.page_size
    """
    page_size_query_param = 'size'
    page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            # 'per_page': self.page_size,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'page_items': len(self.page),
            'total': self.page.paginator.count,
            'results': data
        })

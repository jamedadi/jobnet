from rest_framework.pagination import LimitOffsetPagination


class CompanyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 1
    max_limit = 10

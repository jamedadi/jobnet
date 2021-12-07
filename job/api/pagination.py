from rest_framework.pagination import LimitOffsetPagination


class JobLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 15
    max_limit = 20

import django_filters
from .models import Posts


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        Model = Posts
        fields = ['title']


class VoteFilter(django_filters.FilterSet):
    pass

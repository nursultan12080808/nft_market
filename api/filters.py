import django_filters
from nft_app.models import *

class NftFilter(django_filters.FilterSet):
    price_from = django_filters.NumberFilter(lookup_expr='gte', field_name='price')
    price_to = django_filters.NumberFilter(lookup_expr='lte', field_name='price')
    category = django_filters.ModelMultipleChoiceFilter(queryset=Categories.objects.all())

    class Meta:
        model = Nft
        fields = ['category', 'tags', 'user']
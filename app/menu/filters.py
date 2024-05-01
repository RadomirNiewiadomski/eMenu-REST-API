from django_filters import CharFilter, DateFilter, FilterSet

from menu.models import Menu


class MenuFilter(FilterSet):
    title = CharFilter(field_name='title',
                       lookup_expr='icontains', distinct=True)
    # format: YYYY-MM-DD
    created_from = DateFilter(field_name='created_date',
                              lookup_expr='gte', distinct=True)
    created_to = DateFilter(field_name='created_date',
                            lookup_expr='lte', distinct=True)
    modified_from = DateFilter(
        field_name='modified_date', lookup_expr='gte', distinct=True)
    modified_to = DateFilter(field_name='modified_date',
                             lookup_expr='lte', distinct=True)

    class Meta:
        model = Menu
        fields = [
            'title',
            'created_from',
            'created_to',
            'modified_from',
            'modified_to',
        ]

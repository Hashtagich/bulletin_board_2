from django.forms import DateInput
from django_filters import FilterSet, DateFilter, CharFilter
from .models import Response


class BaseResponseFilter(FilterSet):
    post__title = CharFilter(
        field_name='post__title',
        lookup_expr='icontains',
        label='Заголовок объявления'
    )

    post__text = CharFilter(
        field_name='post__text',
        lookup_expr='icontains',
        label='Содержание объявления'
    )

    datetime_response = DateFilter(
        field_name='datetime_response',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gte',
        label='Дата'
    )

    class Meta:
        model = Response
        fields = [
            'post__title',
            'post__text',
            'datetime_response',

        ]


class ResponseFilter(BaseResponseFilter):
    author = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Автор'
    )

    class Meta(BaseResponseFilter.Meta):
        fields = [
            'post__title',
            'post__text',
            'author',
            'datetime_response'
        ]


class MyResponseFilter(BaseResponseFilter):
    class Meta(BaseResponseFilter.Meta):
        pass
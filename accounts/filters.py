import django_filters
from django_filters import DateFilter
from django import forms
from .models import Order

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(
        field_name='date_created',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Start Date',
            'type': 'date'
        }),
        label='From'
    )

    end_date = DateFilter(
        field_name='date_created',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'End Date',
            'type': 'date'
        }),
        label='To'
    )
    # note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']
        # Optional: You can also customize the remaining fields using 'widgets' dict in the Meta class.

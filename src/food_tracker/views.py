from rest_framework import viewsets
from .models import FoodLog
from .serializers import (
    FoodLogSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters


class FoodLogFilter(filters.FilterSet):
    food_name = filters.CharFilter(
        field_name='food_name', lookup_expr='icontains')

    class Meta:
        model = FoodLog
        fields = ['food_name']


class FoodLogViewSet(viewsets.ModelViewSet):
    """
    Handles: list, create, retrieve, update, partial_update, delete, search
    """
    queryset = FoodLog.objects.all()
    serializer_class = FoodLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FoodLogFilter

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .models import Exercise, Workout, WorkoutSet
from .serializers import (
    ExerciseSerializer,
    WorkoutSerializer,
    WorkoutSetSerializer,
    WorkoutSetCreateSerializer,
)


class ExerciseFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Exercise
        fields = ['name']


class ExerciseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing exercises
    Handles: list, create, retrieve, update, partial_update, delete, search
    """
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExerciseFilter


class WorkoutFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    date_from = filters.DateTimeFilter(
        field_name='created_date', lookup_expr='gte')
    date_to = filters.DateTimeFilter(
        field_name='created_date', lookup_expr='lte')

    class Meta:
        model = Workout
        fields = ['name']


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing workouts
    Handles: list, create, retrieve, update, partial_update, delete, search
    """
    queryset = Workout.objects.prefetch_related('sets', 'sets__exercise').all()
    serializer_class = WorkoutSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkoutFilter

    @action(detail=True, methods=['post'])
    def add_set(self, request, pk=None):
        """
        Custom action to add a set to a workout
        POST /api/workout/workouts/{id}/add_set/
        """
        workout = self.get_object()
        serializer = WorkoutSetCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(workout=workout)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkoutSetFilter(filters.FilterSet):
    workout = filters.NumberFilter(field_name='workout__id')
    exercise = filters.NumberFilter(field_name='exercise__id')

    class Meta:
        model = WorkoutSet
        fields = ['workout', 'exercise']


class WorkoutSetViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing workout sets
    Handles: list, create, retrieve, update, partial_update, delete, search
    """
    queryset = WorkoutSet.objects.select_related('workout', 'exercise').all()
    serializer_class = WorkoutSetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkoutSetFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return WorkoutSetCreateSerializer
        return WorkoutSetSerializer

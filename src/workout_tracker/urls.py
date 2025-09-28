from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet, WorkoutViewSet, WorkoutSetViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet, basename='exercises')
router.register(r'workouts', WorkoutViewSet, basename='workouts')
router.register(r'workout_sets', WorkoutSetViewSet, basename='workout_sets')

urlpatterns = [
    path('', include(router.urls)),
]

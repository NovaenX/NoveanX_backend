from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodLogViewSet

router = DefaultRouter()
router.register(r'food_tracker', FoodLogViewSet, basename='food_tracker')

urlpatterns = [
    path('', include(router.urls)),
]

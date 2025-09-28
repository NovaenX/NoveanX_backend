from rest_framework import serializers
from .models import FoodLog


class FoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodLog
        fields = "__all__"


class FoodLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodLog
        fields = ["food_name", "calories", "protein"]
        read_only_fields = ['id']


class FoodLogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodLog
        fields = ["food_name", "calories", "protein", "created_date"]
        extra_kwargs = {
            "food_name": {"required": False},
            "calories": {"required": False},
            "protein": {"required": False},
            "created_date": {"required": False},
        }

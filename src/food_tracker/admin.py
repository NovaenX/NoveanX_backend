from django.contrib import admin
from .models import FoodLog


@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'food_name', 'calories', 'protein', 'created_date')
    search_fields = ('food_name',)

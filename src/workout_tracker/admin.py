from django.contrib import admin
from .models import Exercise, Workout, WorkoutSet


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_date']
    search_fields = ['name']
    list_filter = ['created_date']


class WorkoutSetInline(admin.TabularInline):
    model = WorkoutSet
    extra = 1
    fields = ['exercise', 'set_number', 'reps', 'weight', 'notes']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_date', 'total_sets']
    search_fields = ['name', 'notes']
    list_filter = ['created_date']
    date_hierarchy = 'created_date'
    inlines = [WorkoutSetInline]

    def total_sets(self, obj):
        return obj.sets.count()
    total_sets.short_description = 'Total Sets'


@admin.register(WorkoutSet)
class WorkoutSetAdmin(admin.ModelAdmin):
    list_display = ['workout', 'exercise',
                    'set_number', 'reps', 'weight', 'created_date']
    search_fields = ['exercise__name', 'workout__name']
    list_filter = ['exercise', 'created_date']
    list_select_related = ['workout', 'exercise']

from rest_framework import serializers
from .models import Exercise, Workout, WorkoutSet


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'created_date']
        read_only_fields = ['created_date']

    def to_representation(self, instance):
        """Ensure created_date is always returned without microseconds"""
        representation = super().to_representation(instance)
        if representation['created_date']:
            dt = instance.created_date
            representation['created_date'] = dt.replace(
                microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ')
        return representation


class WorkoutSetSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(
        source='exercise.name', read_only=True)

    class Meta:
        model = WorkoutSet
        fields = ['id', 'exercise', 'exercise_name', 'set_number',
                  'reps', 'weight', 'notes', 'created_date']
        read_only_fields = ['created_date']

    def to_representation(self, instance):
        """Ensure created_date is always returned without microseconds"""
        representation = super().to_representation(instance)
        if representation['created_date']:
            dt = instance.created_date
            representation['created_date'] = dt.replace(
                microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ')
        return representation


class WorkoutSerializer(serializers.ModelSerializer):
    sets = WorkoutSetSerializer(many=True, read_only=True)
    total_sets = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ['id', 'name', 'notes', 'created_date', 'sets', 'total_sets']
        read_only_fields = ['created_date']

    def get_total_sets(self, obj):
        return obj.sets.count()

    def to_representation(self, instance):
        """Ensure created_date is always returned without microseconds"""
        representation = super().to_representation(instance)
        if representation['created_date']:
            dt = instance.created_date
            representation['created_date'] = dt.replace(
                microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ')
        return representation


class WorkoutSetCreateSerializer(serializers.ModelSerializer):
    """Separate serializer for creating sets"""
    class Meta:
        model = WorkoutSet
        fields = ['id', 'workout', 'exercise',
                  'set_number', 'reps', 'weight', 'notes']

    def create(self, validated_data):
        return super().create(validated_data)

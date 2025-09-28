from django.db import models
from django.utils import timezone
import pytz

# Define Kolkata timezone
kolkata_tz = pytz.timezone('Asia/Kolkata')


def kolkata_now():
    """Return current time in Kolkata timezone"""
    return timezone.now().astimezone(kolkata_tz)


class Exercise(models.Model):
    """
    Exercise template - stores exercise names
    """
    name = models.CharField(max_length=200, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(
        default=kolkata_now, blank=False, null=False)

    class Meta:
        db_table = "exercises"
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Ensure created_date doesn't have microseconds
        if self.created_date:
            self.created_date = self.created_date.replace(microsecond=0)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Workout(models.Model):
    """
    Workout session - groups multiple exercise sets together
    """
    name = models.CharField(max_length=200, default="Workout Session")
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(
        default=kolkata_now, blank=False, null=False)

    class Meta:
        db_table = "workouts"
        ordering = ['-created_date']

    def save(self, *args, **kwargs):
        # Ensure created_date doesn't have microseconds
        if self.created_date:
            self.created_date = self.created_date.replace(microsecond=0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.created_date.strftime('%Y-%m-%d')}"


class WorkoutSet(models.Model):
    """
    Individual set within a workout
    """
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='sets'
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name='workout_sets'
    )
    set_number = models.IntegerField(default=1)
    reps = models.IntegerField(default=10, blank=False, null=False)
    weight = models.FloatField(default=20,
                               blank=False, null=False, help_text="Weight in kg")
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(
        default=kolkata_now, blank=False, null=False)

    class Meta:
        db_table = "workout_sets"
        ordering = ['workout', 'exercise', 'set_number']

    def save(self, *args, **kwargs):
        # Ensure created_date doesn't have microseconds
        if self.created_date:
            self.created_date = self.created_date.replace(microsecond=0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.exercise.name} - Set {self.set_number}: {self.reps} reps @ {self.weight}kg"

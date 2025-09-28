from django.utils.timezone import now
import pytz
from django.db import models


def kolkata_now():
    return now().astimezone(pytz.timezone("Asia/Kolkata"))


class FoodLog(models.Model):
    food_name = models.CharField(
        max_length=255, db_index=True, blank=False, null=False)
    calories = models.FloatField(default=0.0, blank=False, null=False)
    protein = models.FloatField(default=0.0, blank=False, null=False)
    created_date = models.DateTimeField(
        default=kolkata_now, blank=False, null=False)

    class Meta:
        db_table = "food_logs"

    def save(self, *args, **kwargs):
        # Ensure created_date doesn't have microseconds
        if self.created_date:
            self.created_date = self.created_date.replace(microsecond=0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.food_name} - {self.calories} cal"

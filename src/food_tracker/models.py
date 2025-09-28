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

    def __str__(self):
        return self.food_name

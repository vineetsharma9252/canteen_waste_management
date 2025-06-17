# waste_management/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class MenuItem(models.Model):
    MEAL_TYPES = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    )
    name = models.CharField(max_length=100)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)

    def _str_(self):
        return f"{self.name} ({self.meal_type})"

class Prebooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MenuItem.MEAL_TYPES)
    food_items = models.ManyToManyField(MenuItem)
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"{self.user.username} - {self.meal_type} on {self.date}"
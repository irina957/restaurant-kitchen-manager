from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser



class DishType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        ordering = ["username"]
        verbose_name = "cook"
        verbose_name_plural = "cooks"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE, related_name="dishes")
    cooks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="cooked_dishes")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"name: {self.name}, price: {self.price}"

from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import Dish, DishType


def index(request):
    num_cooks = get_user_model().objects.filter(is_staff=False).count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()
    context = {"num_cooks": num_cooks, "num_dishes": num_dishes,
               "num_dish_types": num_dish_types}
    return render(request, "kitchen/index.html", context=context)

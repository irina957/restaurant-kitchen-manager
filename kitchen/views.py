from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import generic

from .models import Dish, DishType, Cook


def index(request):
    num_cooks = get_user_model().objects.filter(is_staff=False).count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {"num_cooks": num_cooks, "num_dishes": num_dishes,
               "num_dish_types": num_dish_types,
               "num_visits": num_visits}
    return render(request, "kitchen/index.html", context=context)


class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"
    paginate_by = 5


class DishListView(generic.ListView):
    model = Dish
    queryset = Dish.objects.select_related("dish_type")
    paginate_by = 5


class CookListView(generic.ListView):
    model = Cook
    paginate_by = 5


class DishDetailView(generic.DetailView):
    model = Dish


class CookDetailView(generic.DetailView):
    model = Cook
    queryset = Cook.objects.prefetch_related("cooked_dishes")

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import Dish, DishType, Cook

@login_required
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


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"
    paginate_by = 5


class DishListView(LoginRequiredMixin,generic.ListView):
    model = Dish
    queryset = Dish.objects.select_related("dish_type")
    paginate_by = 5


class CookListView(LoginRequiredMixin,generic.ListView):
    model = Cook
    paginate_by = 5


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class CookDetailView(LoginRequiredMixin,generic.DetailView):
    model = Cook
    queryset = Cook.objects.prefetch_related("cooked_dishes")


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-list")
    template_name = "kitchen/dish_form.html"


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"

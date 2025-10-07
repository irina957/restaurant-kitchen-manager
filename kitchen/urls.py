from django.urls import path

from kitchen.views import index, DishTypeListView, DishListView, CookListView, DishDetailView, CookDetailView, \
    DishCreateView, DishTypeCreateView

urlpatterns = [
    path("", index, name="index"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("dish-types/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    ]

app_name = "kitchen"

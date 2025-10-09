from django.urls import path

from kitchen.views import index, DishTypeListView, DishListView, CookListView, DishDetailView, CookDetailView, \
    DishCreateView, DishTypeCreateView, DishTypeUpdateView, DishTypeDeleteView

urlpatterns = [
    path("", index, name="index"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish-types/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish-types/<int:pk>/update/", DishTypeUpdateView.as_view(), name="dish-type-update"),
    path("dish-types/<int:pk>/delete/", DishTypeDeleteView.as_view(), name="dish-type-delete"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("cooks/", CookListView.as_view(), name="cook-list"),

    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),


    ]

app_name = "kitchen"

from django.urls import path

from .views import (
    IndexView,
    DishTypeListView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
)


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("dish_type/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish_type/create/",
         DishTypeCreateView.as_view(),
         name="dish-type-create"),
    path("dish_type/<int:pk>/update/",
         DishTypeUpdateView.as_view(),
         name="dish-type-update"),
    path("dish_type/<int:pk>/delete/",
         DishTypeDeleteView.as_view(),
         name="dish-type-delete")
]

app_name = "kitchen"

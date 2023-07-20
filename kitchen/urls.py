from django.urls import path

from .views import (
    IndexView,
    DishTypeListView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    CookListView,
    CookDetailView,
    CookCreateView,
    CookDeleteView,
    CookUpdateView
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
         name="dish-type-delete"),
    
    path("cook/", CookListView.as_view(), name="cook-list"),
    path(
        "cook/<int:pk>/", CookDetailView.as_view(), name="cook-detail"
    ),
    path("cook/create/", CookCreateView.as_view(), name="cook-create"),
    path(
        "cook/<int:pk>/update/",
        CookUpdateView.as_view(),
        name="cook-update",
    ),
    path(
        "cook/<int:pk>/delete/",
        CookDeleteView.as_view(),
        name="cook-delete",
    ),
]

app_name = "kitchen"

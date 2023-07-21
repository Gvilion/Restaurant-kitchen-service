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
    CookUpdateView,
    ChefUpdateView,
    ChefUpdateListView,
    DishListView,
    DishDetailView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView
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
        "cook/<int:pk>/cook-update/",
        CookUpdateView.as_view(),
        name="cook-update",
    ),
    path(
        "cook/<int:pk>/chef-list-update/",
        ChefUpdateListView.as_view(),
        name="chef-list-update",
    ),
    path(
        "cook/<int:pk>/chef-update/",
        ChefUpdateView.as_view(),
        name="chef-update",
    ),
    path(
        "cook/<int:pk>/delete/",
        CookDeleteView.as_view(),
        name="cook-delete",
    ),

    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
]

app_name = "kitchen"

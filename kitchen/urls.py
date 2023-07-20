from django.urls import path

from .views import (
    IndexView,
)


urlpatterns = [
    path("", IndexView.as_view(), )
]

app_name = "kitchen"

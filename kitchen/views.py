from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from kitchen.models import Cook, DishType, Dish


class IndexView(View):

    def get_context_data(self, **kwargs):
        context = {
            "cookers": get_user_model().objects.count(),
            "dish_types": DishType.objects.count(),
            "dishes": Dish.objects.count(),
        }

        return context

    def get(self, request):
        return render(request,
                      "kitchen/index.html",
                      context=self.get_context_data())


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Dish, DishType


class ModelsTest(TestCase):
    def setUp(self):
        self.chef = get_user_model().objects.create_user(
            username="test_chef",
            password="123password123",
            position="A",
            years_of_experience=9
        )
        self.cook = get_user_model().objects.create_user(
            username="test_cook",
            password="123password123",
            position="B",
            years_of_experience=2
        )

        self.dish_type_1 = DishType.objects.create(
            name="dish_type_1"
        )
        self.dish_type_2 = DishType.objects.create(
            name="dish_type_2"
        )

        self.dish_1 = Dish.objects.create(
            name="test_dish_1",
            description="testing_dish_description",
            dish_type=self.dish_type_1,
            price=10,
        )
        self.dish_2 = Dish.objects.create(
            name="test_dish_2",
            description="testing_dish_description_for_second_dish",
            dish_type=self.dish_type_2,
            price=13,
        )

        self.dish_1.cooks.add(self.chef, self.cook)
        self.dish_2.cooks.add(self.cook)

    def test_dish_type_str(self):
        self.assertEqual(str(self.dish_type_1), "dish_type_1")

    def test_dish_str(self):
        self.assertEqual(str(self.dish_1), "test_dish_1")

    def test_position_str(self):
        self.assertEqual(
            str(self.chef.get_position_display()), "chef")
        self.assertEqual(str(self.cook.get_position_display()), "cook")

    def test_cook_get_absolute_url(self):
        self.assertEqual(
            self.chef.get_absolute_url(),
            reverse("kitchen:cook-detail", kwargs={"pk": self.chef.pk})
        )

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Dish, DishType

DISH_LIST_URL = reverse("kitchen:dish-list")


class PublicDishTests(TestCase):
    def test_login_required(self):
        dish_type = DishType.objects.create(name="dish_type_name")
        dish = Dish.objects.create(
            name="test_name",
            price=12,
            dish_type=dish_type
        )

        dish_detail_url = reverse(
            "kitchen:dish-detail",
            kwargs={"pk": dish.pk}
        )

        dish_create_url = reverse("kitchen:dish-create")

        dish_update_url = reverse(
            "kitchen:dish-update",
            kwargs={"pk": dish.pk}
        )

        dish_delete_url = reverse(
            "kitchen:dish-delete",
            kwargs={"pk": dish.pk}
        )

        dish_urls = [DISH_LIST_URL,
                     dish_detail_url,
                     dish_create_url,
                     dish_update_url,
                     dish_delete_url]

        for url in dish_urls:
            response = self.client.get(url)

            self.assertNotEqual(response.status_code, 200)


class PrivateDishTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username_1",
            password="test_1234",
            years_of_experience=2,
            position="A"
        )

        dish_type = DishType.objects.create(name="dish_type_name")
        self.dish = Dish.objects.create(
            name="test_dish_1",
            description="test_description_1",
            price=5,
            dish_type=dish_type
        )

        Dish.objects.create(
            name="test_dish_2",
            description="test_description_2",
            price=6,
            dish_type=dish_type
        )

        self.client.force_login(self.user)

    def test_retrieve_dish_list(self):
        response = self.client.get(DISH_LIST_URL)

        dishes = Dish.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_list"]),
            list(dishes)
        )
        self.assertTemplateUsed(response, "kitchen/dish_list.html")

    def test_retrieve_dish_detail(self):
        dish_detail_url = reverse(
            "kitchen:dish-detail",
            kwargs={"pk": self.dish.pk}
        )

        response = self.client.get(dish_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["dish"],
            self.dish
        )
        self.assertTemplateUsed(response, "kitchen/dish_detail.html")

    def test_use_dish_create(self):
        dish_data = {
            "name": "new_dish",
            "description": "test_description_1",
            "price": 5,
            "dish_type": self.dish.dish_type.id,
            "cooks": [],
        }
        dish_create_url = reverse("kitchen:dish-create")

        response = self.client.post(dish_create_url, dish_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dish.objects.filter(
            name="new_dish"
        ).exists())

    def test_use_dish_update(self):
        dish_type = DishType.objects.create(name="new_dish_type")
        dish_data = {
            "name": "New_name",
            "description": "bla-bla",
            "price": 4,
            "dish_type": dish_type.id,
        }

        dish_update_url = reverse(
            "kitchen:dish-update",
            kwargs={"pk": self.dish.id}
        )

        response = self.client.post(dish_update_url, dish_data)

        self.dish.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual("New_name", self.dish.name)
        self.assertEqual(dish_type, self.dish.dish_type)


class DishListSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username_2",
            password="test_1234",
            years_of_experience=2,
            position="A"
        )

        dish_type = DishType.objects.create(name="dish_type_name_2")
        self.dish = Dish.objects.create(
            name="1_test_dish",
            description="test_description_1",
            price=5,
            dish_type=dish_type
        )
        Dish.objects.create(
            name="2_test_dish",
            description="test_description",
            price=6,
            dish_type=dish_type
        )

        self.client.force_login(self.user)

    def test_search_form_display(self):
        response = self.client.get(DISH_LIST_URL)

        self.assertIn("search_form", response.context)

        self.assertContains(
            response,
            '<form action="" method="get" class="form-inline">'
        )

    def test_search_by_name(self):
        response = self.client.get(f"{DISH_LIST_URL}?name=1_te")
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)

        self.assertContains(response, "1_test_dish")
        self.assertNotContains(response, "2_test_dish")

    def test_search_no_results(self):
        response = self.client.get(f"{DISH_LIST_URL}?name=nonexistent_dish")
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No dishes found.")

    def test_invalid_search_form(self):
        response = self.client.get(reverse("kitchen:dish-list"), {"name": ""})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "1_test_dish")
        self.assertContains(response, "2_test_dish")

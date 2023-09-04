from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType

DISH_TYPE_LIST_URL = reverse("kitchen:dish-type-list")


class PublicDishTypeTests(TestCase):
    def test_login_required(self):
        dish = DishType.objects.create(name="test_name")

        dish_type_create_url = reverse("kitchen:dish-type-create")

        dish_type_update_url = reverse(
            "kitchen:dish-type-update",
            kwargs={"pk": dish.pk}
        )

        dish_type_delete_url = reverse(
            "kitchen:dish-type-delete",
            kwargs={"pk": dish.pk}
        )

        dish_type_urls = [DISH_TYPE_LIST_URL,
                          dish_type_create_url,
                          dish_type_update_url,
                          dish_type_delete_url]

        for url in dish_type_urls:
            response = self.client.get(url)

            self.assertNotEqual(response.status_code, 200)


class PrivateDishTypeTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username_1",
            password="test_1234",
            years_of_experience=2,
            position="A"
        )

        self.dish_type = DishType.objects.create(
            name="test_dish_type_2",
        )

        self.client.force_login(self.user)

    def test_retrieve_dish_type_list(self):
        response = self.client.get(DISH_TYPE_LIST_URL)

        dishes = DishType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dishes)
        )
        self.assertTemplateUsed(response, "kitchen/dish_type_list.html")

    def test_use_dish_type_create(self):
        dish_type_data = {
            "name": "new_dish",
        }
        dish_type_create_url = reverse("kitchen:dish-type-create")

        response = self.client.post(dish_type_create_url, dish_type_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(DishType.objects.filter(
            name="new_dish"
        ).exists())

    def test_use_dish_type_update(self):
        dish_type_data = {
            "name": "New_name",
        }

        dish_type_update_url = reverse(
            "kitchen:dish-type-update",
            kwargs={"pk": self.dish_type.id}
        )

        response = self.client.post(dish_type_update_url, dish_type_data)

        self.dish_type.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual("New_name", self.dish_type.name)


class DishTypeListSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username_2",
            password="test_1234",
            years_of_experience=2,
            position="A"
        )

        self.dish_type = DishType.objects.create(
            name="1_test_dish"
        )
        DishType.objects.create(name="2_test_dish")

        self.client.force_login(self.user)

    def test_search_form_display(self):
        response = self.client.get(DISH_TYPE_LIST_URL)

        self.assertIn("search_form", response.context)

        self.assertContains(
            response,
            '<form action="" method="get" class="form-inline">'
        )

    def test_search_by_name(self):
        response = self.client.get(f"{DISH_TYPE_LIST_URL}?name=1_te")
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)

        self.assertContains(response, "1_test_dish")
        self.assertNotContains(response, "2_test_dish")

    def test_search_no_results(self):
        response = self.client.get(f"{DISH_TYPE_LIST_URL}?name=nonexistent_dish")
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No dishes found.")

    def test_invalid_search_form(self):
        response = self.client.get(reverse("kitchen:dish-type-list"), {"name": ""})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "1_test_dish")
        self.assertContains(response, "2_test_dish")

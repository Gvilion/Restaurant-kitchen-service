from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


COOK_LIST_URL = reverse("kitchen:cook-list")


class PublicCookTests(TestCase):
    def test_login_required(self):
        cook = get_user_model().objects.create_user(
            username="test_username",
            password="123password123"
        )

        cook_detail_url = reverse(
            "kitchen:cook-detail",
            kwargs={"pk": cook.pk}
        )

        cook_create_url = reverse("kitchen:cook-create")

        cook_update_url = reverse(
            "kitchen:cook-update",
            kwargs={"pk": cook.pk}
        )

        cook_delete_url = reverse(
            "kitchen:cook-delete",
            kwargs={"pk": cook.pk}
        )

        cook_urls = [COOK_LIST_URL,
                     cook_detail_url,
                     cook_create_url,
                     cook_update_url,
                     cook_delete_url]

        for url in cook_urls:
            response = self.client.get(url)

            self.assertNotEqual(response.status_code, 200)


class PrivateCookTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username_1",
            password="test_1234",
            years_of_experience=2,
            position="A"
        )

        get_user_model().objects.create_user(
            username="test_username_2",
            password="test_1234",
            years_of_experience=2
        )

        self.client.force_login(self.user)

    def test_retrieve_cook_list(self):
        response = self.client.get(COOK_LIST_URL)

        cooks = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["cook_list"]),
            list(cooks)
        )
        self.assertTemplateUsed(response, "kitchen/cook_list.html")

    def test_retrieve_cook_detail(self):
        cook_detail_url = reverse(
            "kitchen:cook-detail",
            kwargs={"pk": self.user.pk}
        )

        response = self.client.get(cook_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["cook"],
            self.user
        )
        self.assertTemplateUsed(response, "kitchen/cook_detail.html")

    def test_use_cook_create(self):
        data = {
            "username": "new_cook",
            "first_name": "New",
            "last_name": "Cook",
            "password1": "123test123",
            "password2": "123test123",
            "years_of_experience": 2,
            "position": "B",
        }
        cook_create_url = reverse("kitchen:cook-create")

        response = self.client.post(cook_create_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(
            username="new_cook"
        ).exists())

    def test_use_cook_update(self):
        data = {
            "first_name": "New",
            "last_name": "Cook",
        }

        cook_update_url = reverse(
            "kitchen:cook-update",
            kwargs={"pk": self.user.id}
        )

        response = self.client.post(cook_update_url, data)

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual("Cook", self.user.last_name)
        self.assertEqual("New", self.user.first_name)


class CookListSearchTest(TestCase):
    def setUp(self) -> None:
        self.user1 = get_user_model().objects.create(
            username="1_test_user",
            first_name="Test1",
            last_name="User1",
            position="A",
            years_of_experience=5)
        get_user_model().objects.create(
            username="2_test_user",
            first_name="Test2",
            last_name="User2",
            position="B",
            years_of_experience=3
        )
        self.client.force_login(self.user1)

    def test_search_form_display(self):
        response = self.client.get(COOK_LIST_URL)

        self.assertIn("search_form", response.context)

        self.assertContains(
            response,
            '<form action="" method="get" class="form-inline">'
        )

    def test_search_by_username(self):
        response = self.client.get(f"{COOK_LIST_URL}?username=1_te")
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)

        self.assertContains(response, "Test1 User1")
        self.assertNotContains(response, "Test2 User2")

    def test_search_no_results(self):
        response = self.client.get(f"{COOK_LIST_URL}?username=nonexistent_user")
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No cooks found.")

    def test_invalid_search_form(self):
        response = self.client.get(reverse("kitchen:cook-list"), {"username": ""})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Test1 User1")
        self.assertContains(response, "Test2 User2")

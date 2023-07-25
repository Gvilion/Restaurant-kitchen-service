from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteMixin(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test12345"
        )
        self.client.force_login(self.admin_user)


class AdminSiteCookTests(AdminSiteMixin):
    def setUp(self) -> None:
        self.cook = get_user_model().objects.create_user(
            username="cook",
            password="driver12345",
            years_of_experience=3,
            position="A"
        )

    def test_cook_years_of_experience_listed(self):
        url = reverse("admin:kitchen_cook_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)

    def test_cook_detailed_years_of_experiencev_listed(self):
        url = reverse("admin:kitchen_cook_change", args=[self.cook.id])
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)

    def test_cook_position_listed(self):
        url = reverse("admin:kitchen_cook_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)

    def test_cook_detailed_position_listed(self):
        url = reverse("admin:kitchen_cook_change", args=[self.cook.id])
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)

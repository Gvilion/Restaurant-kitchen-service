from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Cook(AbstractUser):
    POSITION_CHOICES = (
        ("A", "chef"),
        ("B", "cook"),
    )

    years_of_experience = models.IntegerField(null=True)
    position = models.CharField(
        max_length=1,
        choices=POSITION_CHOICES,
        default="B"
    )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["position"]


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    dish_type = models.ForeignKey(
        DishType, related_name="dishes", on_delete=models.CASCADE
    )
    cooks = models.ManyToManyField(Cook, related_name="dishes")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "dishes"

    def __str__(self):
        return self.name


class CookManager(BaseUserManager):
    def create_superuser(self, username, years_of_experience, password):
        user = self.model(
            username=username,
            position="A",
            years_of_experience=years_of_experience,
            is_superuser=True,
            is_staff=True
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from kitchen.models import Cook, DishType, Dish


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience", "position")
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("years_of_experience", "position")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "years_of_experience",
                        "position",
                    )
                },
            ),
        )
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("dish_type",)


admin.site.register(DishType)

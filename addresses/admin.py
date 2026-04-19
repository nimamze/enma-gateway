from django.contrib import admin
from .models import UserAddresses


@admin.register(UserAddresses)
class UserAddressesAdmin(admin.ModelAdmin):
    list_display = (
        "get_user_phone",
        "user",
        "province",
        "city",
    )
    list_filter = ("province", "city")
    search_fields = (
        "user__phone",
        "user__first_name",
        "user__last_name",
        "province",
        "city",
        "postal_code",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Phone")
    def get_user_phone(self, obj):
        return obj.user.phone

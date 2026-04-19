from django.contrib import admin
from .models import UserAddresses


@admin.register(UserAddresses)
class UserAddressesAdmin(admin.ModelAdmin):
    list_display = (
        "get_user_phone",
        "get_user_fullname",
        "country",
        "province",
        "city",
    )
    list_filter = ("country", "province", "city")
    search_fields = (
        "user__phone",
        "user__first_name",
        "user__last_name",
        "country",
        "province",
        "city",
        "postal_code",
    )
    ordering = ("-created_at",)

    @admin.display(description="Phone")
    def get_user_phone(self, obj):
        return obj.user.phone

    @admin.display(description="Full Name")
    def get_user_fullname(self, obj):
        return obj.user.get_full_name()

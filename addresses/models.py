from django.db import models
from django.conf import settings
from core.models import BaseModel


class UserAddresses(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    country = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    building_number = models.CharField(max_length=50)
    floor = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.phone} - {self.city}"

    def full_address(self):
        return (
            f"{self.country}, {self.province}, {self.city}, "
            f"{self.address}, No.{self.building_number}, "
            f"Floor {self.floor}, Unit {self.unit}"
        )

from django.db import models
from django.conf import settings
from core.models import BaseModel


class UserAddresses(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    building_number = models.IntegerField()
    floor = models.IntegerField()
    unit = models.IntegerField()
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.phone} - {self.city}"

    def full_address(self):
        return (
            f"{self.province}، {self.city}، "
            f"{self.address}، پلاک {self.building_number}، "
            f"طبقه {self.floor}، واحد {self.unit}"
        )

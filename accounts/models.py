from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(
        User, related_name="user_account", on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    address = models.CharField(max_length=2049)

    def __str__(self) -> str:
        return self.user.username
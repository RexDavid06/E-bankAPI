from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ID_NUMBER_TYPE = [
        ("BVN", "BVN"),
        ("NIN", "NIN"),
    ]

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    id_number_type = models.CharField(max_length=3, choices=ID_NUMBER_TYPE)
    id_number = models.CharField(max_length=11, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
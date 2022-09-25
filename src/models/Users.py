from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class Roles(models.Model):
    name = models.CharField(unique=True, max_length=191)
    display_name = models.CharField(max_length=191, blank=True, null=True)
    description = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'MASTER ROLE'

class User(AbstractUser):
    USER_TYPE = (
        (0, 'Belum Terdaftar'),
        (1, 'Super Admin'),
        (2, 'Admin'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roles = models.ManyToManyField(Roles)
    group = models.IntegerField(default=0, choices=USER_TYPE)
    is_email_confirm = models.BooleanField(default=False)
    phone =  models.CharField(max_length=14, blank=True, null=True)
    nik = models.CharField(max_length=16, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
# custom_admin/models.py

from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    # Add more fields as needed

    def __str__(self):
        return self.email

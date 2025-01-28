from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now  # Import timezone utility

#attributes for each user; 
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('volunteer', 'Volunteer')])
    is_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_reg = models.DateTimeField(default=now,editable = True)  # Automatically set the current date/time when the review is created

    def __str__(self):
        return self.username


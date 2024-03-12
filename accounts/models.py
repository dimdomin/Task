from django.db import models
from django.contrib.auth.models import User


# модель пользователя
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    confirmation_code = models.CharField(max_length=20, unique=True)

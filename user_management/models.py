from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    user_type = models.CharField(max_length=10, choices=(('standard', 'Standard'), ('gold', 'Gold')), default='standard')

    def __str__(self):
        return self.user.username

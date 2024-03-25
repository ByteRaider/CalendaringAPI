from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    user_type = models.CharField(max_length=10, choices=(('standard', 'Standard'), ('gold', 'Gold')), default='standard')

    def __str__(self):
        return f"{self.user.username}'s profile"
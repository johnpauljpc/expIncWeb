from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userPrefrences(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    currency = models.CharField(max_length = 100, blank = True, null = True)

    def __str__(self):
        return f'user {self.user}'
    
    class Meta:
        verbose_name_plural = "user Prefrences"
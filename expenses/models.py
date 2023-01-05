from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateTimeField(default = now)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=30)


    def __str__(self) -> str:
        return self.category

    class Meta:
        ordering=['-date']
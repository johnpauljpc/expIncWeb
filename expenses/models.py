from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #category = models.ForeignKey('category', on_delete=models.CASCADE)
    category = models.CharField(max_length=225)


    def __str__(self) -> str:
        return self.category

    class Meta:
        ordering=['-date']



class Category(models.Model):
    name = models.CharField(max_length= 225)

    def __str__(self):
        return self.name
    # definning how we want the model name to be displayed in our admin panel
    class Meta:
        verbose_name_plural = "Categories"
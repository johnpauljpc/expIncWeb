from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #category = models.ForeignKey('category', on_delete=models.CASCADE)
    source = models.CharField(max_length=225)


    def __str__(self) -> str:
        return self.source

    class Meta:
        ordering=['-date']



class Source(models.Model):
    name = models.CharField(max_length= 225)

    def __str__(self):
        return self.name
    
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.


class Expense(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=7)
    timestamp = models.IntegerField()  # YYYYMMDD format
    local = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    item = models.CharField(max_length=100)
    volume = models.FloatField()
    cost = models.FloatField()

class Income(models.Model):
    id = models.BigAutoField(primary_key=True)

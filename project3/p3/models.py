from django.db import models

class listings (models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=60) #some types of listing
    price = models.FloatField()
# Create your models here.

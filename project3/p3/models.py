from django.db import models

# class listings (models.Model):
#     id = models.AutoField(primary_key=True)
#     type = models.CharField(max_length=60) #some types of listing
#     price = models.FloatField()

class person(models.Model):
    #id automantically added
    user_name = models.CharField(max_length=30)
    pwd = models.CharField(max_length=30)
# Create your models here.

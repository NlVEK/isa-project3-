from django.db import models

# Create your models here.
class person(models.Model):
    #id automantically added
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # create_time = models.DateTimeField(auto_now_add=True)


class thing(models.Model):
    # id = models.AutoField(primary_key=True)
    info = models.CharField(max_length=30)
    # create_time = models.DateTimeField(auto_now_add=True)




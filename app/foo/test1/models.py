from django.db import models

# Create your models here.
class person(models.Model):
    #id automantically added
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=32, default='abcdef', unique=True)
    pwd = models.CharField(max_length=256, default='123456')

    # create_time = models.DateTimeField(auto_now_add=True)


class thing(models.Model):
    # id = models.AutoField(primary_key=True)
    info = models.CharField(max_length=30)
    # create_time = models.DateTimeField(auto_now_add=True)

class auth(models.Model):
    user_name = models.CharField(max_length=30)
    auth = models.CharField(max_length=256)


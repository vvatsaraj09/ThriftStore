from django.db import models

# Create your models here.
class Followers(models.Model):
    follower  =  models.CharField(max_length=120)
    following =  models.CharField(max_length=120)
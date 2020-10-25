from django.db import models

class Product(models.Model):
    name        = models.CharField(max_length=120,unique=True)
    seller      = models.TextField()
    category = models.TextField(default='General',max_length=80,)
    color = models.TextField(default='MultiColor')
    picLink     = models.URLField(max_length=700)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2,max_digits=10000)
    active      = models.BooleanField(default=True)
    date        = models.DateField(null=True)
    lattitude  = models.DecimalField(decimal_places=14,max_digits=10000)
    longitude  = models.DecimalField(decimal_places=14,max_digits=10000)
from django.db import models


class Clothes(models.Model):
    label = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    clothes = models.ManyToManyField(Clothes)





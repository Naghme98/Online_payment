from django.db import models

from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(default=0, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return str(self.name)



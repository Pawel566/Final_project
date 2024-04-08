from django.db import models

# Create your models here.
class Tools(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    accessories = models.CharField(max_length=255)
    in_job = models.BooleanField(default=False, verbose_name="W pracy")
    in_service = models.BooleanField(default=False, verbose_name="W serwisie")

#class Add_to_service
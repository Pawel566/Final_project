from django.db import models

# Create your models here.
class Tools(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    accessories = models.CharField(max_length=255)
    in_job = models.BooleanField(default=False, verbose_name="W pracy")
    in_service = models.BooleanField(default=False, verbose_name="W serwisie")



class Service(models.Model):
    tool = models.ForeignKey(Tools, on_delete=models.CASCADE, verbose_name="Narzędzie", related_name='services_tool')
    fault_description = models.TextField(verbose_name="Opis usterki")
    expected_pickup_date = models.DateField(verbose_name="Przewidywany czas odbioru")
    repaired = models.BooleanField(default=False, verbose_name="Naprawione")

    def __str__(self):
        return f"Serwis narzędzia {self.tool.name} - {self.expected_pickup_date}"


class Jobs(models.Model):
    job_name = models.CharField(max_length=255, verbose_name="Nazwa zlecenia")
    address = models.CharField(max_length=255, verbose_name="Adres")


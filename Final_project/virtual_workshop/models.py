from django.db import models

# Create your models here.
class Tools(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    accessories = models.CharField(max_length=255)
    in_job = models.BooleanField(default=False, verbose_name="W pracy")
    in_service = models.BooleanField(default=False, verbose_name="W serwisie")

    def __str__(self):
        return f"{self.name} - {self.model}"



class Service(models.Model):
    tool = models.ForeignKey(Tools, on_delete=models.CASCADE, verbose_name="Narzędzie", related_name='services_tool')
    fault_description = models.TextField(verbose_name="Opis usterki")
    expected_pickup_date = models.DateField(verbose_name="Przewidywany czas odbioru")
    quantity = models.IntegerField(default=1, verbose_name="Ilość w serwisie")
    repaired = models.BooleanField(default=False, verbose_name="Naprawione")




class Jobs(models.Model):
    job_name = models.CharField(max_length=255, verbose_name="Nazwa zlecenia")
    address = models.CharField(max_length=255, verbose_name="Adres")
    tools = models.ManyToManyField(Tools, through='JobTool', verbose_name="Narzędzia")

    def __str__(self):
        return f"{self.job_name} - {self.address}"



class JobTool(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tools, on_delete=models.CASCADE)
    active = models.BooleanField(default=True, verbose_name="Aktywne")






from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Convict(models.Model):
    def __str__(self):
        return self.name +' - ' + str(self.pk)

    name=models.CharField(max_length=100)
    aliases=models.CharField(max_length=500)
    gender=models.CharField(max_length=20)
    place_of_birth=models.CharField(max_length=510)
    date_of_birth=models.DateField()
    education=models.CharField(max_length=100)
    financial_background=models.CharField(max_length=100)


class Block(models.Model):
    def __str__(self):
        return self.perp.name + ' - '+ str(self.pk)

    perp=models.ForeignKey(Convict, on_delete=models.CASCADE)
    charges=models.CharField(max_length=100)
    charges_code=models.CharField(max_length=200)
    known_accomplices=models.CharField(max_length=100)
    fir_date=models.DateField()
    conviction_date=models.DateField()
    comments=models.TextField(max_length=300)
    sentencer=models.CharField(max_length=100)
    sentence=models.CharField(max_length=100)





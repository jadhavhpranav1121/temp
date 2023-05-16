from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.forms import DateInput
from django.urls import reverse
from django.utils import timezone

from django import forms

# from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput


# Create your models here.


class Convict(models.Model):
    def __str__(self):
        return self.name + " - " + str(self.pk)

    name = models.CharField(max_length=100)
    aliases = models.CharField(max_length=500)
    gender = models.CharField(max_length=20)
    place_of_birth = models.CharField(max_length=510)
    place_of_birth_type = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField()
    education = models.CharField(max_length=100, blank=True)
    financial_background = models.CharField(max_length=100, blank=True)
    family_record = models.CharField(max_length=100, blank=True)


class ConvictValidate(models.Model):
    def __str__(self):
        return str(self.user.id) + " validated convict " + str(self.convict.id)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    convict = models.ForeignKey(Convict, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("convictdetail", kwargs={"pk": self.convict.pk})


class Block(models.Model):
    def __str__(self):
        return self.perp.name + " - " + str(self.pk)

    perp = models.ForeignKey(Convict, on_delete=models.CASCADE)
    charges = models.CharField(max_length=100)
    charges_code = models.CharField(max_length=200, blank=True, null=True)
    crime_type = models.CharField(max_length=100, blank=True, null=True)
    known_accomplices = models.CharField(max_length=100, blank=True)
    fir_date = models.DateField(blank=True)
    conviction_date = models.DateField(default=timezone.now)
    comments = models.TextField(max_length=300, blank=True)
    sentencer = models.CharField(max_length=100, blank=True)
    sentence = models.CharField(max_length=100, blank=True)

    # def get_absolute_url(self):
    #    return reverse('blockdetail', kwargs={'pk': self.block.pk})


class BlockValidate(models.Model):
    def __str__(self):
        return str(self.user.id) + " validated block " + str(self.block.id)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("blockdetail", kwargs={"pk": self.block.pk})

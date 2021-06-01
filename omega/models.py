from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.




class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('omega:list', args=[self.pk])


class Commodity(models.Model):
    name = models.CharField(max_length= 150)
    current_price = models.FloatField()
    opening_price = models.FloatField()
    available = models.BooleanField()
    year = models.IntegerField()
    month = models.IntegerField()
    unit = models.CharField(max_length=150)
    volume = models.FloatField()
    updated = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='commodities/')

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Commodities"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('omega:detail', args=[str(self.pk)])
from django.db import models
from django.urls import reverse
from datetime import date
# Import the User
from django.contrib.auth.models import User


class Brewery(models.Model):
    api_id = models.IntegerField()
    name = models.CharField(max_length=100)
    brewery_type = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    website_url = models.CharField(max_length=100)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)

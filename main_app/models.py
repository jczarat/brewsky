from django.db import models
from django.urls import reverse
from datetime import date
# Import the User
from django.contrib.auth.models import User

class Brewery(models.Model):
  name = models.CharField(max_length=100)
  api_id = models.IntegerField(max_length=100)
 
  

class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE) 
  brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
  comment = models.CharField(max_length=200)


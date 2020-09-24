from django.db import models
from django.urls import reverse
from datetime import date
# Import the User
from django.contrib.auth.models import User
RATING = (
    ('1', '1 Star'),
    ('2', '2 Stars'),
    ('3', '3 Stars'),
    ('4', '4 Stars'),
    ('5', '5 Stars'),
)

class Brewery(models.Model):
    api_id = models.IntegerField()
    name = models.CharField(max_length=100)
    brewery_type = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    website_url = models.CharField(max_length=100)


class Comment(models.Model):
    rating = models.CharField(max_length=1, choices=RATING, default=RATING[4][0])
    comment = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'brewery_id': self.brewery.api_id})


class Favorite(models.Model):
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'brewery_id': self.brewery.api_id})
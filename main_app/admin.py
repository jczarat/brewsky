from django.contrib import admin
from .models import Brewery, Comment, Favorite

# Register your models here.

admin.site.register(Brewery)
admin.site.register(Comment)
admin.site.register(Favorite)

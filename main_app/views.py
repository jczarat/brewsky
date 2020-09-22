import uuid
import boto3
import os
import requests
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Brewery

# API Stuff
my_key = os.environ['BREWERY_API_KEY']
b = requests.get(
    f'https://sandbox-api.brewerydb.com/v2/breweries/?key={my_key}')
l = requests.get(
    f'https://sandbox-api.brewerydb.com/v2/locations/?key={my_key}')
breweries = b.json()["data"]
locations = l.json()["data"]

S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'catcollector-sei-9-cw'


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def breweries_index(request):
    # breweries = Brewery.objects.filter(user=request.user)
    state_filter = []
    for location in locations:
        if 'region' in location and location["region"] == 'New York':
            state_filter.append(location)
    return render(request, 'breweries/index.html', {'breweries': breweries, 'state_filter': state_filter})


def breweries_detail(request, brewery_id):
    # brewery = Brewery.objects.get(id=brewery_id)
    for brewery in breweries:
        if brewery['id'] == brewery_id:
            print(brewery)
    print(brewery_id)
    return render(request, 'breweries/detail.html', {'brewery': brewery})


# @login_required
# def add_photo(request, cat_id):
#   # photo-file will be the "name" attribute on the <input>
#   photo_file = request.FILES.get('photo-file', None)
#   if photo_file:
#     s3 = boto3.client('s3')
#     # need a unique "key" / but keep the file extension (image type)
#     key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
#     # just in case we get an error
#     try:
#       s3.upload_fileobj(photo_file, BUCKET, key)
#       url = f"{S3_BASE_URL}{BUCKET}/{key}"
#       Photo.objects.create(url=url, cat_id=cat_id)
#     except:
#       print('An error occured uploading file to S3')
#   return redirect('detail', cat_id=cat_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

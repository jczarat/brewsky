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
from .models import Brewery, Comment
from .forms import CommentForm

# API Stuff
b = requests.get('https://api.openbrewerydb.org/breweries')

breweries = b.json()


S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'catcollector-sei-9-cw'

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['comment']


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def breweries_index(request):
    # breweries = Brewery.objects.filter(user=request.user)
    by_state = None
    by_city = None
    by_postal = None
    if 'state' in request.GET:
        state = request.GET['state']
        s = requests.get(f'https://api.openbrewerydb.org/breweries?by_state={state}&per_page=50&page={pnum}')
        by_state = s.json()
    if 'city' in request.GET:
        city = request.GET['city']
        c = requests.get(f'https://api.openbrewerydb.org/breweries?by_city={city}&per_page=50')
        by_city = c.json()
    if 'postal' in request.GET:
        postal = request.GET['postal']
        p = requests.get(f'https://api.openbrewerydb.org/breweries?by_postal={postal}&per_page=50')
        by_postal = p.json()
    return render(request, 'breweries/index.html', {'breweries': breweries, 'by_state': by_state, 'by_city': by_city , 'by_postal': by_postal, "pnum": pnum})


def breweries_detail(request, brewery_id):
    comment_form = CommentForm()
    d = requests.get(f'https://api.openbrewerydb.org/breweries/{brewery_id}')
    brewery = d.json()
    if Brewery.objects.filter(api_id=brewery['id']).exists() == False:
        new_brewery = Brewery.objects.create(
            api_id = brewery['id'],
            name = brewery['name'],
            brewery_type = brewery['brewery_type'],
            street = brewery['street'],
            city = brewery['city'],
            state = brewery['state'],
            postal_code = brewery['postal_code'],
            country = brewery['country'],
            longitude = brewery['longitude'],
            latitude = brewery['latitude'],
            phone = brewery['phone'],
            website_url = brewery['website_url']
        )
    db_brewery = Brewery.objects.get(api_id=brewery_id)
    comments = Comment.objects.filter(brewery=db_brewery.id)
    brewery_result = Brewery.objects.get(api_id=brewery_id)

    return render(request, 'breweries/detail.html', {'brewery_result': brewery_result, 'comment_form': comment_form, 'comments': comments})


@login_required
def add_comment(request, brewery_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.brewery_id = brewery_id
        new_comment.user_fk_id = request.user.id
        new_comment.username = request.user.username
        new_comment.save()
    brewery = Brewery.objects.get(id=brewery_id)
    return redirect('detail', brewery_id=brewery.api_id)

@login_required
def delete_comment(request, brewery_id, comment_id):
    Comment.objects.filter(id=comment_id).delete()
    return redirect('detail', brewery_id=brewery_id)

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

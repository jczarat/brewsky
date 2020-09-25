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


b = requests.get('https://api.openbrewerydb.org/breweries')
breweries = b.json()


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['comment', 'rating']


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def breweries_index(request):
    by_state = None
    by_city = None
    by_postal = None
    pnum = 1
    if request.POST and 'next' in request.POST:
        pnum = int(request.POST['next']) + 1
    if request.POST and 'previous' in request.POST and int(request.POST['previous']) > 1:
        pnum = int(request.POST['previous']) - 1
    if 'state' in request.GET:
        state = request.GET['state']
        s = requests.get(
            f'https://api.openbrewerydb.org/breweries?by_state={state}&per_page=50&page={pnum}')
        by_state = s.json()
    if 'city' in request.GET:
        city = request.GET['city']
        c = requests.get(
            f'https://api.openbrewerydb.org/breweries?by_city={city}&per_page=50&page={pnum}')
        by_city = c.json()
    if 'postal' in request.GET:
        postal = request.GET['postal']
        p = requests.get(
            f'https://api.openbrewerydb.org/breweries?by_postal={postal}&per_page=50%page={pnum}')
        by_postal = p.json()
    return render(request, 'breweries/index.html', {'breweries': breweries, 'by_state': by_state, 'by_city': by_city, 'by_postal': by_postal, "pnum": pnum})


def breweries_detail(request, brewery_id):
    comment_form = CommentForm()
    d = requests.get(f'https://api.openbrewerydb.org/breweries/{brewery_id}')
    brewery = d.json()
    if Brewery.objects.filter(api_id=brewery['id']).exists() == False:
        new_brewery = Brewery.objects.create(
            api_id=brewery['id'],
            name=brewery['name'],
            brewery_type=brewery['brewery_type'].capitalize(),
            street=brewery['street'],
            city=brewery['city'],
            state=brewery['state'],
            postal_code=brewery['postal_code'],
            country=brewery['country'],
            phone=brewery['phone'][:3] + '-' +
                brewery['phone'][3:6] + '-' + brewery['phone'][6:],
            website_url=brewery['website_url']
        )
    db_brewery = Brewery.objects.get(api_id=brewery_id)
    comments = Comment.objects.filter(brewery=db_brewery.id)
    total = 0
    average_rating = None
    for comment in comments:
        total = total + int(comment.rating)
    if len(comments):
        average_rating = total / len(comments)
    brewery_result = Brewery.objects.get(api_id=brewery_id)
    test = brewery['brewery_type'].capitalize()
    gm_token = os.environ['GOOGLE_MAPS_TOKEN']
    return render(request, 'breweries/detail.html', {'brewery_result': brewery_result, 'comment_form': comment_form, 'comments': comments, 'gm_token': gm_token, 'average_rating': average_rating})


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
def add_favorite(request, brewery_id):
    if Brewery.objects.filter(favorites__id=request.user.id).count() < 5:
        Brewery.objects.get(id=brewery_id).favorites.add(request.user.id)
    brewery = Brewery.objects.get(id=brewery_id)
    return redirect('detail', brewery_id=brewery.api_id)


@login_required
def delete_comment(request, brewery_id, comment_id):
    Comment.objects.filter(id=comment_id).delete()
    return redirect('detail', brewery_id=brewery_id)

@login_required
def delete_favorite(request, brewery_id):
    brewery = Brewery.objects.get(id=brewery_id)
    request.user.brewery_set.remove(brewery)
    return redirect('favorites_index')


@login_required
def favorites_index(request):
    breweries = Brewery.objects.filter(favorites__id=request.user.id)
    return render(request, 'favorite.html', {'breweries': breweries})


def signup(request):
    error_message=''
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message='Invalid sign up - try again'
    form=UserCreationForm()
    context={'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

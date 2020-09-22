from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('breweries/', views.breweries_index, name='index'),
    path('breweries/<int:brewery_id>/', views.breweries_detail, name='detail'),
    path('breweries/<int:brewery_id>/comments/', views.add_comment, name='add_comment'),
    path('accounts/signup/', views.signup, name='signup'),
]
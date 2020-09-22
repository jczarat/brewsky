from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('breweries/', views.breweries_index, name='index'),
    path('breweries/<str:brewery_id>/', views.breweries_detail, name='detail'),
    path('accounts/signup/', views.signup, name='signup'),
]
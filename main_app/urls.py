from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('breweries/', views.breweries_index, name='index'),
    path('breweries/<int:brewery_id>/', views.breweries_detail, name='detail'),
    path('breweries/<int:brewery_id>/add_comment/', views.add_comment, name='add_comment'),
    path('breweries/<int:brewery_id>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('breweries/<int:brewery_id>/update_comment/<int:pk>/', views.CommentUpdate.as_view(), name='update_comment'),
    path('breweries/<int:brewery_id>/add_favorite/', views.add_favorite, name='add_favorite'),
    path('breweries/<int:brewery_id>/delete_favorite/<int:favorite_id>/', views.delete_favorite, name='delete_favorite'),
    path('accounts/signup/', views.signup, name='signup'),
]
from django.forms import ModelForm
from .models import Comment, Favorite


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'rating']

class FavoriteForm(ModelForm):
    class Meta:
        model = Favorite
        fields = []

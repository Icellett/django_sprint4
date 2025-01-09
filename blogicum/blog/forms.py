from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'location', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class CustomUserCreationForm(UserCreationForm):

    # Наследуем класс Meta от соответствующего класса родительской формы.
    # Так этот класс будет не перезаписан, а расширен.
    class Meta(UserCreationForm.Meta):
        model = User
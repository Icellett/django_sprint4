from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    post_list = Post.objects.filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=datetime.now()
    )
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category.html', {'category': category,
                                                  'page_obj': page_obj})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True,
                             pub_date__lte=datetime.now(),
                             category__is_published=True)
    return render(request, 'blog/detail.html', {'post': post})

def custom_403_view(request, exception):
    return render(request, 'pages/403.html', status=403)

def custom_404_view(request, exception):
    return render(request, 'pages/404.html', status=404)

def custom_500_view(request):
    return render(request, 'pages/500.html', status=500)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление после успешной регистрации
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user)  # Получаем публикации пользователя
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'profile.html', {'user': user, 'page_obj': page_obj})
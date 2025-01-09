from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm


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
    comments = post.comments.all()  # Получаем все комментарии к посту
    form = CommentForm()  # Создаем пустую форму для комментариев

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('view_post', post_id=post.id)
    return render(request, 'blog/detail.html', {'post': post, 'form': form,
                                                'comments': comments})


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
            return redirect('login')
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/profile.html', {'user': user,
                                                 'page_obj': page_obj})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:index')
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('profile', username=request.user.username)
    return render(request, 'blog/confirm_delete.html', {'post': post})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', pk=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html',
                  {'form': form, 'post': post})


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('view_post', post_id=post_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/add_comment.html',
                  {'form': form, 'post': comment.post})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', pk=post_id)
    return render(request, 'blog/comment.html', {'comment': comment})
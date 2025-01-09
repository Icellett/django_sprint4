from django.conf.urls import handler403, handler404, handler500
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from . import views
from .views import profile

app_name = 'blog'

handler403 = 'blog.views.custom_403_view'
handler404 = 'blog.views.custom_404_view'
handler500 = 'blog.views.custom_500_view'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts,
         name='category_posts'),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('pages:index'),
        ),
        name='registration',
    ),
    path('profile/<str:username>/', profile, name='profile'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/comment/', views.add_comment,
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

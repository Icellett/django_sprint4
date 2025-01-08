from django.conf.urls import handler403, handler404, handler500
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import register

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
    path('registration/', register, name='registration'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from django.urls import include
from . import views
from .views import PostUpdateView, PostDeleteView


urlpatterns = [
    path('', include('users.urls')),
    path('welcome/', views.welcome, name='welcome'),
    path('new_post/', views.new_post, name='new_post'),
    path('home/', views.user_posts, name='user_posts'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('feed/', views.feed, name='feed'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]


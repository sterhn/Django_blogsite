from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('new_post/', views.new_post, name='new_post'),
    path('my_posts/', views.user_posts, name='user_posts'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('feed/', views.feed, name='feed')
]
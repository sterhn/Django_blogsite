from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from .models import Post, Comment

def welcome(request):
    return render(request, 'welcome.html')

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form': form})

@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'user_posts.html', {'posts': posts})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST, author=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            form = CommentForm()
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

# фильтрация и пагинация
def feed(request):
    posts = Post.objects.all()
    return render(request, 'feed.html', {'posts': posts})

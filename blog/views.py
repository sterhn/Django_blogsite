from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CommentForm, PostForm
from .models import Post, Comment

def welcome(request):
    return render(request, 'welcome.html')

def home(request):
    return render(request, 'home.html')

@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # Handle image upload
            if 'image' in request.FILES:
                image = request.FILES['image']
                fs = FileSystemStorage(location='media/post_images')
                filename = fs.save(image.name, image)
                post.image = 'post_images/' + filename
                post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form': form})



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


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('feed')

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'
    success_url = reverse_lazy('feed')

# фильтрация и пагинация
def feed(request):
    posts = Post.objects.all()
    return render(request, 'feed.html', {'posts': posts})

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm

# Create your views here.


def index(request):
    form = PostForm(request.POST, request.FILES)
    # IF method is POST
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        # if the form is valid
        if form.is_valid():
            #yes , save
            form.save()

            # Redirect to home
            return HttpResponseRedirect('/')
        else:

            # no show error
            return HttpResponseRedirect(form.errors.as_json())

    # Get all posts, limit =20
    posts = Post.objects.all().order_by('-created_at')[:20]

    # show
    return render(request, 'posts.html',
                  {'posts': posts, 'form': form})


def delete(request, post_id):
    # find user
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/')


def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    # if the method is post
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
    # If the form is valid
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    # yes save
    # redirect to home
    # no, show error
        else:
            return HttpResponseRedirect(form.errors.as_json())

    return render(request, 'edit.html', {'post': post})


def like(request, post_id):
    post = Post.objects.get(id=post_id)
    new_like = post.likes + 1
    post.likes = new_like
    post.save()
    return HttpResponseRedirect('/')

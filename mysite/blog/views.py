from django.contrib.auth.models import User

# Create your views here.

from django.shortcuts import render , get_object_or_404
from .models import Post,Comment
from django.utils import timezone
from django.shortcuts import redirect
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.,
# creating view post_list
def blog_details(request):
    return render(request,'post_detail.html',{})
@login_required
def post_list(request):
    u = User.objects.all()[:5]
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'blog.html',{'posts' : posts,'ranker':u})

@login_required
def post_detail(request,pk):
    u = User.objects.all()[:5]
    post = get_object_or_404(Post , pk = pk)
    same_user = False
    if(request.user == post.author):
        same_user= True
    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')[:5]
    return render(request , 'single-blog.html',{'post' : post,'ranker':u,'posts':posts,'same_user':same_user})

# methods for creating new post 

@login_required
def post_new(request):
    u = User.objects.all()[:5]
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')[:5]
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm()
    return render(request,'post_edit.html',{'form':form,'ranker':u,'posts':posts})

#methods for editing and saving the post in the draft 
#maintaining the decorators @login_required for editing the post
 

@login_required
def post_edit(request , pk):
    u = User.objects.all()[:5]
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    post = get_object_or_404(Post,pk = pk)
    if request.method == "POST":
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm(instance = post)
    return render(request ,'post_edit.html',{'form':form,'ranker':u,'posts':posts})


@login_required
def post_draft_list(request,pk):
    posts = Post.objects.filter(published_date__isnull = True,author__pk = pk).order_by('created_date')
    u = User.objects.all()[:5]
    draft = True
    return render(request,'blog.html',{'posts':posts,'drafts':draft,'ranker':u,'posts':posts})

# defining the method for publishing of unpublished post
# login required for publishing the post

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)
# defining the method for removing the published post
# login required for removing any post
@login_required
def post_remove(request,pk):
    post = get_object_or_404(Post,pk = pk)
    post.delete()
    return redirect('post')

def about(request):
    return render(request,'about.html',{})

# creating function for blog

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    u = User.objects.all()[:5]
    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')[:5]
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'single-blog.html', {'form': form,'post':post,'ranker':u,'posts':posts})
@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.delete()
    return redirect('post_detail' ,pk=comment.post.pk)


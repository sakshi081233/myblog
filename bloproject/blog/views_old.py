from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Post, Category, Comment
from django.db.models import Q
import requests


def home(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        )
    else:
        posts = Post.objects.filter(status='published')
    posts = Post.objects.filter(status='published')
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(status='published').order_by('-created_at')[:5]
    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]
    
    # Pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'categories': categories,
        'recent_posts': recent_posts,
        'popular_posts': popular_posts,
        'query': query,
    }
    return render(request, 'blog/home.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    post.views += 1
    post.save()
    
    comments = post.comments.filter(active=True)
    
    # Handle comment submission
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        
        Comment.objects.create(
            post=post,
            name=name,
            email=email,
            content=content
        )
        return redirect('post_detail', slug=slug)
    
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'blog/post_detail.html', context)

def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category, status='published')
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category_posts.html', context)
def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category, status='published')
    context = {'category': category, 'posts': posts}
    return render(request, 'blog/category_posts.html', context)

def search(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query),
        status='published'
    )
    
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'blog/search.html', context)

def about(request):
    # Get your blog’s trending and latest posts
    trending_posts = Post.objects.filter(status='published').order_by('-views')[:5]
    latest_posts = Post.objects.filter(status='published').order_by('-created_at')[:5]
    categories = Category.objects.all()

    #  Fetch world trending news from GNews API
    world_trends = []
    try:
        #  Replace 'YOUR_API_KEY' with your actual API key from https://gnews.io
        res = requests.get('https://gnews.io/api/v4/top-headlines?lang=en&token=59974532df38552bec5b6e28201f1092')
        if res.status_code == 200:
            data = res.json()
            world_trends = data.get('articles', [])[:5]
    except Exception as e:
        print("Error fetching world trends:", e)

    context = {
        'trending_posts': trending_posts,
        'latest_posts': latest_posts,
        'categories': categories,
        'world_trends': world_trends,
    }
    return render(request, 'blog/about.html', context)

def contact(request):
    return render(request, 'blog/contact.html')

# Create your views here.

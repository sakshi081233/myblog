from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from .models import Post, Category, Comment
import requests

# ------------------ HOME ------------------
""""
def home(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        )
    else:
        posts = Post.objects.filter(status='published')

    categories = Category.objects.all()
    recent_posts = Post.objects.filter(status='published').order_by('-created_at')[:5]
    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]

    # Pagination (6 posts per page)
    paginator = Paginator(posts, 6)
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

"""""
def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    posts = Post.objects.filter(status='published')

    if category_id:
        posts = posts.filter(category_id=category_id)
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    categories = Category.objects.all()
    recent_posts = Post.objects.filter(status='published').order_by('-created_at')[:5]
    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'categories': categories,
        'recent_posts': recent_posts,
        'popular_posts': popular_posts,
        'query': query,
        'selected_category': category_id,
    }
    return render(request, 'blog/home.html', context)
    

    # --- PAGINATION ---
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # --- SIDEBAR DATA ---
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(status='published').order_by('-created_at')[:5]
    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]

    context = {
        'posts': page_obj,
        'categories': categories,
        'recent_posts': recent_posts,
        'popular_posts': popular_posts,
        'query': query,
        'selected_category': category_id,
    }

    return render(request, 'blog/home.html', context)
# ------------------ POST DETAIL ------------------
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


# ------------------ CATEGORY POSTS ------------------
def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category, status='published')

    context = {'category': category, 'posts': posts}
    return render(request, 'blog/category_posts.html', context)

#def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})

# ------------------ SEARCH ------------------
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


# ------------------ ABOUT ------------------
def about(request):
    trending_posts = Post.objects.filter(status='published').order_by('-views')[:5]
    latest_posts = Post.objects.filter(status='published').order_by('-created_at')[:5]
    categories = Category.objects.all()

    world_trends = []
    api_key = '59974532df38552bec5b6e28201f1092'  # your GNews API key

    try:
        url = 'https://gnews.io/api/v4/top-headlines'
        params = {
            'lang': 'en',
            'country': 'us',
            'topic': 'world',
            'max': 5,
            'token': api_key
        }
        res = requests.get(url, params=params, timeout=10)

        if res.status_code == 200:
            data = res.json()
            world_trends = data.get('articles', [])[:5]
        else:
            print(f"GNews API Error {res.status_code}: {res.text}")
    except Exception as e:
        print("Error fetching world trends:", e)

    context = {
        'trending_posts': trending_posts,
        'latest_posts': latest_posts,
        'categories': categories,
        'world_trends': world_trends,
    }
    return render(request, 'blog/about.html', context)

#---------contact --------------------------------

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        # (You can later add logic to send email or save to DB)
    return render(request, "blog/contact.html")

#-----community--------------------
def community(request):
    contributors = [
        {
            'name': 'Aditi Sharma',
            'role': 'Eco Blogger',
            'bio': 'Writes about zero-waste travel and conscious living.',
            'image': 'images/community1.jpg'
        },
        {
            'name': 'Rohan Mehta',
            'role': 'Sustainability Researcher',
            'bio': 'Explores green technologies and climate innovations.',
            'image': 'images/community2.jpg'
        },
        {
            'name': 'Dhyansh Nair',
            'role': 'Wildlife Photographer',
            'bio': 'Captures the beauty of nature to inspire conservation.',
            'image': 'images/community3.jpg'
        },
        {
            'name': 'Arjun Patel',
            'role': 'Green Tech Blogger',
            'bio': 'Passionate about renewable energy, smart cities, and sustainable design.',
            'image': 'images/community4.jpg'
        },
    ]
    return render(request, 'blog/community.html', {'contributors': contributors})


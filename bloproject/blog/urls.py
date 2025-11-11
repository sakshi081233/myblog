from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog import views
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # path('post/<int:post_id>/', views.post_detail, name='post_detail'), 
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('search/', views.search, name='search'),
    path('community/', views.community, name='community'),
    path('categories/', views.category_posts, name='category_posts'),
    #path('categories/', views.categories, name='categories'),

]


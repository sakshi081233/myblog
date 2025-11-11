from django.contrib import admin
from .models import Category, Post, Comment, Tag

# ------------------ CATEGORY ADMIN ------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


# ------------------ POST ADMIN ------------------
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'views']
    list_filter = ['status', 'created_at', 'category']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}  # Automatically generate slug from title
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    autocomplete_fields = ['category', 'author']  # Easier selection in admin


# ------------------ COMMENT ADMIN ------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created_at', 'active']
    list_filter = ['active', 'created_at']
    search_fields = ['name', 'email', 'content']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Approve selected comments"


# ------------------ TAG ADMIN ------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

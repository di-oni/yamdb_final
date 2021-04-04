from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class MyAdminSite(AdminSite):
    site_header = 'Alexis Python administration'
    site_title = 'My Project Title Administration'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Managing categories in the admin area.
       Inherited from admin.ModelAdmin."""
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name', 'slug',)
    empty_value_display = '-empty-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Managing genres in the admin area.
       Inherited from admin.ModelAdmin."""
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name', 'slug',)
    empty_value_display = '-empty-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Managing titles in the admin area.
       Inherited from admin.ModelAdmin."""
    list_display = ('pk', 'name', 'year', 'category',)
    search_fields = ('name', 'year', 'category',)
    list_filter = ('year', 'category',)
    empty_value_display = '-empty-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Managing reviews in the admin area.
       Inherited from admin.ModelAdmin."""
    list_display = ('pk', 'title', 'text', 'author', 'score',)
    search_fields = ('title', 'author', 'score',)
    list_filter = ('score', 'title',)
    empty_value_display = '-empty-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Managing comments in the admin area.
       Inherited from admin.ModelAdmin."""
    list_display = ('pk', 'review', 'text', 'author', 'pub_date',)
    search_fields = ('review', 'text', 'author', 'pub_date',)
    list_filter = ('pub_date', 'review', 'author',)
    empty_value_display = '-empty-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Managing comments in the admin area.
       Inherited from admin.ModelAdmin."""
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'bio',
        'is_staff'
    )
    search_fields = ('username', 'email', 'role',)
    list_filter = ('role', 'is_active',)
    empty_value_display = '-empty-'

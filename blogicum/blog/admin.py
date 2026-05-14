from django.contrib import admin
from .models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_display_links = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_published',)
    list_editable = ('is_published',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('is_published',)
    list_editable = ('is_published',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'pub_date', 'author', 'category',
        'location', 'is_published', 'created_at'
    )
    list_display_links = ('title',)
    search_fields = ('title', 'text')
    list_filter = ('is_published', 'category', 'author')
    list_editable = ('is_published',)
    date_hierarchy = 'pub_date'

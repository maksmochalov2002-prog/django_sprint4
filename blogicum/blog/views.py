from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


def get_published_posts():
    """Возвращает QuerySet опубликованных постов с учётом даты и категории"""
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).select_related('category', 'location', 'author')


def index(request):
    template = 'blog/index.html'
    post_list = get_published_posts()[:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        get_published_posts(),
        id=id
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_published_posts().filter(category=category)
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)

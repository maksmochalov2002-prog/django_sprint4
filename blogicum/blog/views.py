from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.http import Http404

from .models import Post, Comment
from .forms import PostForm, CommentForm

User = get_user_model()


def get_visible_posts(user=None, show_all_author_posts=False):
    """
    Получить видимые посты.
    show_all_author_posts: True - показывать все посты автора (для профиля),
                           False - только опубликованные (для главной)
    """
    base_query = Post.objects.select_related('author', 'category', 'location')

    if not user or not user.is_authenticated or not show_all_author_posts:
        return base_query.filter(
            category__is_published=True,
            is_published=True,
            pub_date__lte=timezone.now()
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    return base_query.filter(
        Q(author=user) | Q(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')


def index(request):
    posts = get_visible_posts(request.user, show_all_author_posts=False)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def user_profile(request, username):
    author = get_object_or_404(User, username=username)
    show_all = request.user.is_authenticated and request.user == author
    posts = get_visible_posts(
        request.user,
        show_all_author_posts=show_all
    ).filter(author=author)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': author,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


def category_posts(request, category_slug):
    from .models import Category
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True)
    posts = Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('author', 'category', 'location'),
        id=post_id
    )

    if not post.is_visible(request.user):
        raise Http404("Пост не найден")

    comments = post.comments.select_related('author').all()
    form = CommentForm() if request.user.is_authenticated else None

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
        'is_edit': True
    }
    return render(request, 'blog/create.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)

    context = {
        'object': post,
        'object_type': 'пост',
        'cancel_url': 'blog:post_detail',
        'cancel_kwargs': {'post_id': post_id},
    }
    return render(request, 'blog/delete_form.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)

    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = CommentForm(instance=comment)

    context = {
        'form': form,
        'comment': comment,
        'post_id': post_id,
        'is_edit': True,
    }
    return render(request, 'blog/edit_comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)

    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)

    context = {
        'object': comment,
        'object_type': 'комментарий',
        'cancel_url': 'blog:post_detail',
        'post_id': post_id,
    }
    return render(request, 'blog/delete_form.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = UserChangeForm(instance=request.user)

    context = {'form': form}
    return render(request, 'blog/edit_profile.html', context)

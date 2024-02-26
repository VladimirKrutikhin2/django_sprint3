from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Now

from blog.models import Post, Category


POSTS_LIMIT = 5


def index(request):
    template = 'blog/index.html'

    post_list = (
        Post.objects
        .filter(is_published=True,
                category__is_published=True,
                pub_date__lte=Now(),
                ).order_by('pub_date')
    )[:POSTS_LIMIT]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
            is_published=True,
            category__is_published=True),
        pk=post_id,
        pub_date__lte=Now(),
    )
    context = {
        'post': post
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = (
        Post.objects
        .filter(category=category,
                is_published=True,
                pub_date__lte=Now()
                ).order_by('pub_date')
    )
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)
from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Now

from blog.models import Post, Category


POSTS_LIMIT = 5


def get_post_list(category=None):
    post_list = (
        Post.objects
        .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=Now(),
        ).order_by('pub_date')
    )
    if category is not None:
        post_list = post_list.filter(category=category,)
    else:
        post_list = post_list[:POSTS_LIMIT]

    return post_list


def index(request):
    context = {'post_list': get_post_list()}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
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
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    context = {
        'category': category,
        'post_list': get_post_list(category),
    }
    return render(request, 'blog/category.html', context)

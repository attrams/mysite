from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def post_list(request):
    post_list = Post.published.all()
    # pagination with 3 posts per page
    paginator = Paginator(object_list=post_list, per_page=3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer division deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page_number is out of range deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request=request, template_name='blog/post/list.html', context={'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return render(request=request, template_name='blog/post/detail.html', context={'post': post})

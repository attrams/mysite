import re
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
# Create your views here.


class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


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


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"

            send_mail(
                subject=subject,
                message=message,
                from_email='attramspapa@gmail.com',
                recipient_list=[cd['to']]
            )
            sent = True

    else:
        form = EmailPostForm()

    return render(request=request, template_name='blog/post/share.html', context={'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request=request, template_name='blog/post/comment.html', context={'post': post, 'form': form, 'comment': comment})

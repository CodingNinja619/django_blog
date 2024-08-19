from django.shortcuts import render
from .models import *
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 2)
    page_number = int(request.GET.get("page", 1))
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    # print(type(posts))
    posts.adjusted_elided_pages = posts.paginator.get_elided_page_range(number=page_number, on_each_side=3, on_ends=2)

    return render(request, 'blog/post/list.html', {"posts": posts, "current_page_number": page_number})


def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.objects.get(id=id)
    # except:
    #     raise Http404

    post = get_object_or_404(Post,
                             status = Post.Status.PUBLISHED,
                             slug = post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    return render(request, "blog/post/detail.html", {"post": post})
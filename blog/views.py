from django.shortcuts import render
from .models import *
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 1)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    # print(type(posts))

    pages_list = {}

    if posts.number - 1 != 1:
        pages_list["before"] = True
    else:
        pages_list["before"] = False
    
    if posts.number + 1 != posts.paginator.num_pages:
        pages_list["after"] = True
    else:
        pages_list["after"] = False

    # Checking if there's a page before previous one by substracting first page from the current page
    if posts.number - 1 >= 2 and posts.number - 2 != 1:
        pages_list['before_prev'] = True
    else:
        pages_list["before_prev"] = False
    
    # Checking if there's a page after next one by substracting current page from the last page
    if posts.paginator.num_pages - posts.number >= 2 and posts.paginator.num_pages - posts.number != 1:
        pages_list["after_next"] = True
    else:
        pages_list["after_next"] = False

    return render(request, 'blog/post/list.html', {"posts": posts, "pages_list": pages_list})


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
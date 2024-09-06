from django.shortcuts import render
from .models import *
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import *
from django.core.mail import send_mail

class PostListView(ListView):
    queryset = Post.published.all() # or model = Post if I want default Post.objects.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context["paginator"]
        page_obj = context["page_obj"]
        page_range = paginator.get_elided_page_range(number=page_obj.number)
        context["page_range"] = page_range
        context["current_page_number"] = page_obj.number
        return context


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

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form validated
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            body = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comment: {cd['comment']}"
            
            send_mail(subject, body, "hitmanabsolution25@gmail.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, "blog/post/share.html", {"post": post, "form": form, "sent": sent})
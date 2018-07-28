
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect ,reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ArticlePostForm, CommentForm
from .models import ArticleColumn, ArticlePost, Comment

import json
# Create your views here.


@login_required(login_url='/login')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            new_article = ArticlePost()
            new_article.author = request.user
            new_article.title = cd.get('title')
            new_article.ueditor_body = cd.get('content')
            new_article.save()
            test_article  = ArticlePost.objects.filter(slug=new_article.slug).first()
            # return HttpResponse("1")
            return redirect(reverse('article_detail', kwargs={'pid': new_article.pid, 'slug':new_article.slug}))
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        return render(request, "x_fatie_demo.html", {"article_post_form":article_post_form})


def article_detail(request, pid, slug):
    article = get_object_or_404(ArticlePost, pid=pid, slug=slug)
    author = article.author

    comments = Comment.objects.all()



    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            cd = comment_form.cleaned_data
            new_comment = Comment()
            new_comment.body = cd.get('comment_content')
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()




    return render(request, "x_huitie_demo.html", {"article":article, "comment_form":comment_form, "author":author, "comments":comments})
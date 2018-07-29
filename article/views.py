from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
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
    if request.method=="POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            #try:
            new_article = ArticlePost()
            new_article.author = request.user
            new_article.title = cd.get('title')
            new_article.ueditor_body = cd.get('content')
            new_article.save()
            #url = reverse('')
            url = reverse('article_detail', kwargs={'pid':new_article.pid,'slug':new_article.slug})
            #print(url)
            return HttpResponseRedirect(url)
                #return HttpResponse('1')
            #except:
                #return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        return render(request, "x_fatie_demo.html", {"article_post_form":article_post_form})

@login_required(login_url='/login')
@csrf_exempt
def article_detail(request, pid, slug, page):
    article = get_object_or_404(ArticlePost, pid=pid, slug=slug)
    author = article.author

    comments = Comment.objects.filter(article=article).all()[page * 10 - 10: page * 10]
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            cd = comment_form.cleaned_data
            new_comment = Comment()
            new_comment.article = article
            new_comment.ueditor_body = cd.get('comment_body')
            new_comment.save()
            url = reverse('article_detail', kwargs={'pid': article.pid, 'slug': article.slug})
            return HttpResponseRedirect(url)
    else:
        comment_form = CommentForm()
    return render(request, "x_huitie_demo.html", {"article":article, "comment_form":comment_form, "author":author, "comments":comments})
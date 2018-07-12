from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ArticlePostForm
from .models import ArticleColumn, ArticlePost

import json
# Create your views here.
@login_required(login_url='/account/login/')
def article_colmn(request):
         columns = ArticleColumn.objects.filter(user=request.user)
         return render(request, "article/column/article_column.html", {"columns": columns})

@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method=="POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
			#cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                tags = request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag = request.user.tag.get(tag=atag)
                        new_article.article_tag.add(tag)
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()    #⑦
        #article_tags = request.user.tag.all()    #①
        article_tags = {}
        return render(request, "article/column/article_post.html", {"article_post_form":article_post_form, "article_columns":article_columns, "article_tags":article_tags})

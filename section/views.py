from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SectionForum
from article.models import ArticlePost
# Create your views here.


@login_required(login_url='/login/')
def section_all(request, section_slug):
    section = SectionForum.objects.filter(slug=section_slug).all()[0]

    if request.method == 'GET' and len(request.GET):
        print('get')
        posts = None
    else:
        posts = ArticlePost.objects.filter(section_belong_fk=section).all()[0:10]
    context = {
        'section': section,
        'posts': posts,
    }

    return render(request, 'tiezi_demo.html', context)

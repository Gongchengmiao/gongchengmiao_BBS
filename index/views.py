from django.shortcuts import render
from article.models import forum_post

# Create your views here.

def index(request):
    latest_posts = forum_post.objects.order_by('pub_date')
    context = {
        'latest_posts':latest_posts
    }
    return render(request, 'BBS_index_demo.html', context)

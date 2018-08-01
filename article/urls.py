from django.conf.urls import url
from django.urls import path, re_path
from . import views, search_views

app_name = 'article'
urlpatterns = [
    path('article-post/', views.article_post, name="article_post"),
    path('article-detail/<int:pid>/<slug:slug>/', views.article_detail, name="article_detail"),
    path('like-article/', views.like_article, name="like_article"),
    url(r'^like/$', 'article.views.like', name='like'),
]
from django.conf.urls import url
from django.urls import path, re_path
from . import views

app_name = 'article'
urlpatterns = [
    path('article-post/', views.article_post, name="article_post"),
    path('article-detail/<int:pid>/<slug:slug>/', views.article_detail, name="article_detail"),
]
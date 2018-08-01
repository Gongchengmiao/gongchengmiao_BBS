"""gongchengmiao_BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from index import views as index_views
from django.conf.urls.static import static
from gongchengmiao_BBS import settings
from user import views as user_views
from homepage import views as homepage_views
from chat import views as chat_views
from article import views as article_views
from article import search_views
from section import views as section_views
from haystack.views import SearchView
from django.views.generic import TemplateView
# from django.conf.urls import url
# from django.views.static import serve as static_serve
# from gongchengmiao_BBS.settings import STATIC_ROOT

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('index/', index_views.index_shell, name='index'),
    path('index_core/', index_views.index, name='index_core'),
    path('', index_views.redirect_to_login, name='main'),

    path('register/', user_views.register, name='register'),
    path('login/', user_views.login, name='login'),
    path('logout/', user_views.logout, name='logout'),
    path('verify/<uidb64>/<token>/', user_views.email_active, name='verify_user'),
    path('waitemail/<username>/', user_views.jump_to_wait, name='wait_email'),
    path('waitemailback/<username>/', user_views.pswdgetback_jump, name='wait_email_back'),
    path('pswdgetback', user_views.pswdgetback, name='pswd_get_back'),
    path('pswdgetback/<uidb64>/<token>/', user_views.pswd_get_back_view, name='pswd_get_beck_2'),
    path('pswdgetbackjmp/<username>/', user_views.pswdgetback_jump, name='pswdgetback_jump'),

    path('article/', include('article.urls', namespace='article')),
    path('article/article-detail/<int:pid>/<slug:slug>/', article_views.article_detail, name='article_detail'),
    path('article/article-post/', article_views.article_post, name='article_post'),
    path('article/', article_views.article_post, name="article_post"),
    path('article/like-article/', article_views.like_article, name="like_article"),
    path('search/', search_views.MySearchView(), name='haystack_search'),

    path('like/', article_views.like, name='like'),

    path('chat/', chat_views.index, name='chat_index'),
    path('chat/<room_name>/', chat_views.room, name='room'),

    path('homepage/self/', homepage_views.view_self_info, name='view_self_info'),
    path('homepage/edit/', homepage_views.edit_info, name='edit_info'),
    path('homepage/uid=<slug>/', homepage_views.show_info, name='show_info'),
    path('homepage/ajax_follow', homepage_views.show_info_ajax_follow, name='show_info_ajax_follow'),
    path('homepage/ajax_star', homepage_views.show_info_ajax_star, name='show_info_ajax_star'),
    path('homepage/ajax_more', homepage_views.show_info_ajax_more, name='show_info_ajax_more'),
    path('homepage/ajax_scroll', homepage_views.view_self_ajax_scroll, name='view_self_ajax_scroll'),
    path('homepage/ajax_save_portrait', homepage_views.edit_info_ajax_save_portrait, name='edit_info_save_portrait'),
    path('homepage/ajax_upload_temp', homepage_views.edit_info_ajax_upload_temp, name='edit_info_ajax_upload_temp'),
    path('homepage/ajax_get_temp', homepage_views.edit_info_ajax_get_temp, name='edit_info_ajax_get_temp'),
    path('homepage/ajax_delete_temp', homepage_views.delete_temp, name='edit_info_ajax_delete_temp'),



    path('section/sec=<section_slug>', section_views.section_all, name='section_all'),
    path('section/open_posts_list', section_views.section_open_posts_list, name='open_posts_list'),
    path('section/follow_sec', section_views.section_follow, name='section_follow'),

    path('ueditor/', include('DjangoUeditor.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

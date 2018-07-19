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
from django.urls import path,include
from index import views as index_views
from django.conf.urls.static import static
from gongchengmiao_BBS import settings
from user import views as user_views
from homepage import views as homepage_views
from django.views.generic import TemplateView
# from django.conf.urls import url
# from django.views.static import serve as static_serve
# from gongchengmiao_BBS.settings import STATIC_ROOT

urlpatterns = [
    path('index/', index_views.index_shell, name='index'),
    path('', index_views.redirect_to_login, name='main'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login, name='login'),
    path('logout/', user_views.logout, name='logout'),
    path('verify/<uidb64>/<token>/', user_views.email_active, name='verify_user'),
    path('waitemail/<username>/', user_views.jump_to_wait, name='wait_email'),
    path('admin/', admin.site.urls, name='admin'),
    path('article/', include('article.urls', namespace='article')),
    path('index_core/', index_views.index, name='index_core'),
    path('pswdgetback', user_views.pswdgetback, name='pswd_get_back'),
    path('waitemailback/<username>/', user_views.pswdgetback_jump, name='wait_email_back'),
    path('homepage/self', homepage_views.view_self_info, name='view_self_info'),
    # path('self/', homepageViews.view_self_info, name='view_self_info'),
    path('homepage/edit/', homepage_views.edit_info, name='edit_info'),
    path('homepage/uid=<username>', homepage_views.show_info, name='show_info'),
    path('pswdgetback/<uidb64>/<token>/', user_views.pswd_get_back_view, name='pswd_get_beck_2'),
    path('pswdgetbackjmp/<username>/', user_views.pswdgetback_jump, name='pswdgetback_jump'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

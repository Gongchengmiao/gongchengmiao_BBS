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
from django.urls import path
from index import views as index_views
from django.conf.urls.static import static
from gongchengmiao_BBS import settings
from user import views as user_views
# from django.conf.urls import url
# from django.views.static import serve as static_serve
# from gongchengmiao_BBS.settings import STATIC_ROOT

urlpatterns = [
    path('index/', index_views.index, name='index'),
    path('', index_views.redirect_to_login, name='main'),
    # path('index/', index_views.index),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login, name='login'),
    path('verify/<username>/', user_views.email_active, name='verify_user'),
    path('admin/', admin.site.urls, name='admin'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

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
from gongchengmiao_BBS.settings import STATIC_ROOT
from django.conf.urls import url
from django.views.static import serve as static_serve

urlpatterns = [
    path('', index_views.index, name='index'),
    url(r'^static/(?P<path>.*)$', static_serve, {'document_root': STATIC_ROOT}),
    path('admin/', admin.site.urls),
]

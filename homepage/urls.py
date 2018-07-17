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
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from homepage import views as homepageViews
from gongchengmiao_BBS import settings
from django.conf.urls.static import static


# urlpatterns = [
#     # path('', index_views),
#     # path('accounts/login/', auth_views.LoginView.as_view()),
#     path('self/', homepageViews.view_self_info, name='view_self_info'),
#     path('edit/', homepageViews.edit_info, name='edit_info'),
#     path('uid=<username>', homepageViews.show_info, name='show_info'),
#
# ]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


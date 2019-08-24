"""feiuauth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from user import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^captcha', include('captcha.urls')),  #图片验证码
    path(r'login/', views.login,name='login'),
    path(r'register/', views.register),
    path(r'logout/', views.logout,name='logout'),
    path(r'forget/',views.forget,name='forget_pwd'),
    path(r'index/',views.index),
    path(r'edit_user/',views.edit_user),
    url(r'books',views.manage_books),
    url(r'^confirm/$', views.user_confirm),
    #忘记密码
    # path('^forget/',views.forget,name='forget_pwd'),
    url(r'^pwd_reset/$', views.pwd_reset, name='pwd_reset'),
    #重置密码
    url(r'^reset/$',views.reset,name='reset'),
    path(r'', views.index),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

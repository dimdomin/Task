"""
URL configuration for Task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from ckeditor_uploader.views import upload, browse
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import url
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache

from accounts.forms import register
from accounts.views import confirm_registration

from board.views import profile

urlpatterns = [

    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/signup/', register, name='register'),
    path('accounts/register/', confirm_registration, name='confirm'),
    path('profile/', profile, name='profile'),
    path('accounts/', include('allauth.urls')),
    path('', include('board.urls')),
    re_path(r'^upload/', login_required(upload), name='ckeditor_upload'),       # для загрузки файлов в ckeditor всеми пользователями
    re_path(r'^browse/', login_required(never_cache(browse)), name='ckeditor_browse'),          # для загрузки файлов в ckeditor всеми пользователями
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
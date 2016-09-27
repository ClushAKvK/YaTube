"""datingapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from datingapp import settings
from datingapp.views import auth_views, user_views, views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/', views.test_view)
]

urlpatterns += [
    url(r'^login/$', auth_views.login),
    url(r'^registration/$', auth_views.register),
    url(r'^facebook/$', auth_views.facebook)
]

urlpatterns += [
    url(r'^profile/photo/$', user_views.profile_photo),
    url(r'^profile/edit/(\w+)/$', user_views.profile),
    url(r'^users/$', user_views.get_users),
    url(r'^request_user/$', user_views.get_req_user),
    url(r'^likes/(\w+)/', user_views.likes_friendship),
    url(r'^refresh_token/$', user_views.refresh_token),
    url(r'^visitors/(\w+)/', user_views.get_visitors)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

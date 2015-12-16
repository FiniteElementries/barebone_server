"""server URL Configuration

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
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/userprofile/', include('userprofile.urls')),
    url(r'^api/account/', include('account.urls')),

    # password resets todo add customized views
    url(r'^password_reset_done$', 'django.contrib.auth.views.password_reset_done',
        name='password_reset_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name="reset_password"),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>,+)/$',
        'django.contrib.auth.views.password_reset_confirm'),
    url(r'^password_reset_complete$', 'django.contrib.auth.views.password_reset_complete'),
]

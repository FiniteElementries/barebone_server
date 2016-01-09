

from django.conf.urls import patterns, url
from api_account import *


urlpatterns = patterns('',
                       url(r'^login', account_login),
                       url(r'^create', create_account),
                       url(r'^logout', account_logout),
                       url(r'^change_password', change_password),
                       # url(r'^overview', getUserDetails, {}, 'getUserDetailsAPI'),
                       )
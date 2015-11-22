

from django.conf.urls import patterns, url
from func import *


urlpatterns = patterns('',
                       url(r'^login', account_login),
                       url(r'^create', create_account),
                       url(r'^logout', account_logout),
                       # url(r'^overview', getUserDetails, {}, 'getUserDetailsAPI'),
                       )
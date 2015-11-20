
from django.conf.urls import patterns, url
from api_userprofile import *


urlpatterns = patterns('',
                       url(r'^overview', get_userprofile_generic),
                       url(r'^detail', get_userprofile_all),
                       # url(r'^overview', getUserDetails, {}, 'getUserDetailsAPI'),
                       )

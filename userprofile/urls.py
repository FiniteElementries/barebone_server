
from django.conf.urls import patterns, url
from api_userprofile import *


urlpatterns = patterns('',
                       url(r'^overview', get_userprofile_generic),
                       url(r'^detail', get_userprofile_detail),
                       url(r'^friends/list', get_friend_list),
                       url(r'^friends/change', friend_action),
                       # url(r'^overview', getUserDetails, {}, 'getUserDetailsAPI'),
                       )

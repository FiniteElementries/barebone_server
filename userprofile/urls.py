
from django.conf.urls import patterns, url
from api_userprofile import *


urlpatterns = patterns('',
                       url(r'^info', get_userprofile_detail),
                       url(r'^friends/list', get_friend_list),
                       url(r'^friends/change', friend_action),
                       )

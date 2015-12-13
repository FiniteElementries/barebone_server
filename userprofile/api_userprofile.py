
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

from userprofile.models import UserProfile
import account.func
from helper.auth import server_auth


@csrf_exempt
@server_auth
def get_userprofile_detail(request):
    """
    :param
    :return:
    """

    response=dict()
    response['success'] = False

    user=request.user
    my_profile=user.profile

    try:
        target_username=request.POST['target_username']
    except KeyError:
        account.func.error_response("provide target_username")

    try:
        target_userprofile=UserProfile.objects.get(user__username=target_username)
    except UserProfile.DoesNotExist:
        account.func.error_response("target_username does not exist")

    package=target_userprofile.get_userprofile_info(my_profile)

    response['success']=True
    response['message']="success"
    response['package']=dict()

    for key, value in package.iteritems():
        response['package'][key]=value

    return HttpResponse(json.dumps(response))


@csrf_exempt
@server_auth
def friend_action(request):
    """
    POST method
    :param request:
    :return:
    """

    user=request.user

    try:
        action=request.POST['action']
        target_username=request.POST['target_username']
    except KeyError:
        return account.func.error_response("user POST method to include 'action' and 'target_username'")

    try:
        target_userprofile=UserProfile.objects.get(user__username=target_username)
    except User.DoesNotExist:
        return account.func.error_response("target username does not exist")

    response=dict()

    if action=="follow":
        user.profile.rs_follow(target_userprofile)
        # todo send friend request notification

    elif action=="block":
        user.profile.rs_block(target_userprofile)

    elif action=="unfollow" or action=="unblock":
        user.profile.rs_reset(target_userprofile)

    response['success']=True
    response['message']="success"

    return HttpResponse(json.dumps(response))


@csrf_exempt
@server_auth
def get_friend_list(request):
    """

    :param request:
    :return: list of friend usernames
    """
    user=request.user

    friend_list = user.profile.get_follower()

    package=",".join(friend_list)

    response=dict()
    response['success']=True
    response['message']="success"

    response['package']=package

    return HttpResponse(json.dumps(response))




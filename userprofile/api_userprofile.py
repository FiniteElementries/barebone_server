
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

from userprofile.models import UserProfile
import account.func
from account.func import server_auth

#todo merger get generic and detail together, filter based on permission level

@csrf_exempt
@server_auth
def get_userprofile_generic(request):
    """

    :param request: json format: {"userid", integer_value}
    :return: user details in json
    """
    response=dict()
    response['success'] = False

    user=request.user

    try:
        user_profile=UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return account.func.error_response("Server error")

    response['first_name']=user_profile.user.first_name
    response['last_name']=user_profile.user.last_name
    response['about_me']=user_profile.about_me
    response['success'] = True
    response['message'] = "success"

    return HttpResponse(json.dumps(response))

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
    my_profile=UserProfile.objects.get(user=user)


    try:
        target_username=request.POST['target_username']
    except KeyError:
        account.func.error_response("provide target_username")

    try:
        target_userprofile=UserProfile.objects.get(user__username=target_username)
    except UserProfile.DoesNotExist:
        account.func.error_response("target_username does not exist")

    print my_profile,target_userprofile
    print my_profile in target_userprofile.follower.all()
    if my_profile==target_userprofile:
        print "return full access"  # todo implement access full_access
        response['message']="full_access"
    elif my_profile in target_userprofile.follower.all():
        print "return follower access"  # todo implement access foloower
        response['message']="follower"
    elif my_profile in target_userprofile.blocked.all():
        print "return block access"
        response['message']="block" # todo implement access blocked
    else:
        print "stranger access"
        response['message']="stranger"  # todo implement access stranger

    response['success']=True

    return HttpResponse(json.dumps(response))


# todo check if this works
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

    try:
        myprofile=UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return account.func.error_response("server internal error")

    if action=="follow":
        myprofile.rs_follow(target_userprofile)
        # todo send friend request notification

    elif action=="block":
        myprofile.rs_block(target_userprofile)

    elif action=="unfollow" or action=="unblock":
        myprofile.rs_reset(target_userprofile)

    response['success']=True
    response['message']="success"

    return HttpResponse(json.dumps(response))


# todo check if this works
@csrf_exempt
@server_auth
def get_friend_list(request):
    """

    :param request:
    :return: list of friend usernames
    """
    user=request.user
    profile=UserProfile.objects.get(user=user)

    friend_list = profile.get_follower()

    package=",".join(friend_list)

    response=dict()
    response['success']=True
    response['message']="success"

    response['package']=package

    return HttpResponse(json.dumps(response))




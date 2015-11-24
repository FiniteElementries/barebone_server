
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from rest_framework.authtoken.models import Token

from userprofile.models import UserProfile
import account.func
from account.func import server_auth, check_friendship



@csrf_exempt
def get_userprofile_generic(request):
    """

    :param request: json format: {"userid", integer_value}
    :return: user details in json
    """
    response=dict()
    response['success'] = False

    username = request.GET['username']

    if username is None:
        return account.func.error_response("Need to provide username")

    try:
        user_profile=UserProfile.get_userprofile_by_username(username)
    except UserProfile.DoesNotExist:
        return account.func.error_response("Invalid username")

    response['first_name']=user_profile.user.first_name
    response['last_name']=user_profile.user.last_name
    response['about_me']=user_profile.about_me
    response['success'] = True
    response['message'] = "success"

    return HttpResponse(json.dumps(response))

@csrf_exempt
@server_auth
@check_friendship
def get_userprofile_detail(request):
    """
    :param request: GET method
    :return:
    """

    response=dict()
    response['success'] = False

    user=request.user
    target_userprofile=request.target_userprofile

    perm=request.perm

    response['message']=perm
    response['success']=True

    if user.has_perm('full_access', target_userprofile):
        request.perm='full_access' # todo implement access full_access
    elif user.has_perm('friend', target_userprofile):
        request.perm='friend' # todo implement access friend
    elif user.has_perm('blocked', target_userprofile):
        request.perm='blocked' # todo implement access blocked
    else:
        request.perm='stranger' # todo implement access stranger

    return HttpResponse(json.dumps(response))



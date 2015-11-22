
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from rest_framework.authtoken.models import Token

from userprofile.models import UserProfile
import api.func



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
        return api.func.error_response("Need to provide username")

    try:
        user_profile=UserProfile.get_userprofile_by_username(username)
    except UserProfile.DoesNotExist:
        return api.func.error_response("Invalid username")

    response['first_name']=user_profile.user.first_name
    response['last_name']=user_profile.user.last_name
    response['about_me']=user_profile.about_me
    response['success'] = True
    response['message'] = "success"

    return HttpResponse(json.dumps(response))


@csrf_exempt
def get_userprofile_all(request):
    """

    :param request: GET method
    :return:
    """

    response=dict()
    response['success'] = False

    username = request.GET['username']
    token = request.GET['token']
    target_username = request.GET['target_username']

    verified=api.func.verify_token(username,token)

    if not verified:
        return api.func.error_response("Invalid username or token")

    # try to get userprofile
    try:
        target_userprofile=UserProfile.objects.get(user__username=target_username)
    except UserProfile.DoesNotExist:
        return api.func.error_response("Invalid target username")

    # check for permission
    user=User.objects.get(username=username)
    if not user.has_perm('full_access', target_userprofile):
         return api.func.error_response("Permission denied")

    response['success'] = True
    response['message'] = "success"

    return HttpResponse(json.dumps(response))




from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json

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


# @login_required
def get_userprofile_all(request):

    response=dict()
    response['success'] = False

    username = request.GET['username']

    user=request.user

    print user

    if not user.is_authenticated():
        return api.func.error_response("Login is required")

    try:
        user_profile=UserProfile.get_userprofile_by_username(username)
    except UserProfile.DoesNotExist:
        return api.func.error_response("Invalid username")


    if not user.has_perm('full_access', user_profile):
        return api.func.error_response("Permission denied")

    response['success'] = True

    return HttpResponse(json.dumps(response))

@login_required
def getMyDetails(request):
    response=dict()

    return  HttpResponse(json.dumps(response))

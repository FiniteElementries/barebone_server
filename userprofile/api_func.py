
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

from userprofile.models import UserProfile
import api.func


@csrf_exempt
def create_user(request):
    """
    :param request: json format '{"username": "username_value",
                                    "email":"email_value" ,
                                    "password": "password_value,}'
    :return:new UserProfile object
    """
    serialized=json.loads(request)

    new_user = User.objects.create_user(username=serialized['username'],
                                        email=serialized['email'],
                                        password=serialized['password'])

    new_user_profile = UserProfile(user = new_user)
    new_user_profile.save()

    return new_user_profile


# http verison
# @csrf_exempt
# def getUserDetails(request):
#     response=dict()
#
#     userid = request.REQUEST.get('userid', None)
#
#     if userid is None:
#         return api.func.errorResponse("Need to provide userid")
#
#     try:
#         user_profile=UserProfile.getUser(userid)
#     except UserProfile.DoesNotExist:
#         return api.func.errorResponse("Invalid userid")
#
#     response['first_name']=user_profile.user.first_name
#
#     return HttpResponse(json.dumps(response))

# json version

@csrf_exempt
def getUserDetails(request):
    """

    :param request: json format: {"userid", integer_value}
    :return: user details in json
    """
    response=dict()

    serialized=json.loads(request)

    userid = serialized['userid']

    if userid is None:
        return api.func.errorResponse("Need to provide userid")

    try:
        user_profile=UserProfile.getUser(userid)
    except UserProfile.DoesNotExist:
        return api.func.errorResponse("Invalid userid")

    response['first_name']=user_profile.user.first_name

    return  json.dumps(response)

   # return HttpResponse(json.dumps(response))
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from userprofile.models import UserProfile
from helper.http_handler import error_response, package_handle
from helper.auth import server_auth
import datetime
import sys


# todo test profile picture in UserProfile model


def create_account(request):
    """
    :param request: POST method
                        json format '{"username": "username_value",
                                    "email":"email_value" ,
                                    "password": "password_value,}'
    :return:new UserProfile object
    """
    response=dict()
    response['success']=False
    response['message']=""
    try:
        username = request.POST['username']
        password = request.POST['password']
        email= request.POST['email']

        if User.objects.filter(username=username).exists():
            return error_response("username exists")

        if User.objects.filter(email=email).exists():
            return error_response("email exists")

        new_user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
        token=Token.objects.create(user=new_user)
        new_user_profile = UserProfile(user = new_user)
        new_user_profile.save()

        response['success']=True
        response['message']="success"
        response['token']=token.key

    except ValueError:
        return error_response("Please provide username, password and email")

    return package_handle(response)


def account_login(request):
    """

    :param request: GET method
    :return:
    """
    response=dict()

    username = request.POST['username']
    password = request.POST['password']

    user=authenticate(username=username, password=password)

    response['message']=""
    response['userid']=""
    response['success']=False

    if user is not None:
        if user.is_active:
            response['success']=True
            response['message']="sucess"

            try:
                exist_token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                return error_response("server error")

            exist_token.delete()
            token=Token.objects.create(user=user)
            token.created = datetime.datetime.utcnow()

            response['token']=token.key

        else:
            # Return a 'disabled account' error message
            response['message']="disabled account"

    else:
        # Return an 'invalid login' error message.
        response['message']="invalid login"


    return package_handle(response)


def account_logout(request):
    """
    log user out, reset access token
    :param request: POST method
    :return:
    """
    response=dict()
    response['success']=False

    user=request.user

    try:
        exist_token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        return error_response("server error")

    exist_token.delete()
    Token.objects.create(user=user)

    response['success']=True
    response['message']="success"

    return package_handle(response)


def change_password(request):
    """
    change user account password
    :param request:
    :return:
    """

    new_password=request.POST['new_password']
    old_password=request.POST['old_password']
    username=request.POST['username']
    response=dict()

    user=authenticate(username=username, password=old_password)
    token_user=request.user

    if not user:
        print "auth error"
        return error_response("Invalid username or old password")
    else:
        user.set_password(new_password)
        user.save()
        response['success']=True
        response['message']="success"

        return package_handle(response)

# todo need to be tested
def delete_account(request):
    """
    delete user account and its related profile
    :param request:
    :return:
    """

    user=request.user
    profile=user.profile

    user.delete()

    try:
        profile.delete()
    except:
        pass

    response=dict()
    response['success']=True
    response['message']="success"

    return package_handle(response)
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from guardian.models import UserObjectPermission
from rest_framework.authtoken.models import Token

from userprofile.models import UserProfile
import sys


# todo friendship check decorator
def check_friendship(original_function):
    def wrapper(request):
        try:
            username = request.GET['username']
            token = request.GET['token']
            target_username=request.GET['target_username']
        except:
            username = request.POST['username']
            token = request.POST['token']
            target_username=request.POST['target_username']

        user = request.user
        target_user = User.objects.get(username=target_username)
        target_userprofile = UserProfile.objects.get(user=target_user)
        request.target_userprofile=target_userprofile

        if user.has_perm('full_access', target_userprofile):
            request.perm='full_access'
        elif user.has_perm('friend', target_userprofile):
            request.perm='friend'
        elif user.has_perm('blocked', target_userprofile):
            request.perm='blocked'
        else:
            request.perm='stranger'

        return original_function(request)
    return wrapper





def server_auth(original_function):
    """
    server access authentication
    request should include username and access token
    attaches user object to request if successful
    :param original_function:
    :return:
    """
    def wrapper(request):
        username=""
        token=""

        try:
            username = request.GET['username']
            token = request.GET['token']
        except:
            username = request.POST['username']
            token = request.POST['token']

        authorized = verify_token(username=username, token=token)

        if authorized:
            user=User.objects.get(username=username)
            request.user=user
            return original_function(request)
        else:
            return error_response("Authentication error.")
    return wrapper


def error_response(error, response=None):
    if not response:
        response = dict()

    response['message'] = error
    response['success'] = False

    return HttpResponse(json.dumps(response))


def verify_token(username, token):
    """
    :param username: string
    :param token: string
    :return: true or false
    """

    # check user account existance
    try:
        user=User.objects.get(username=username)
    except User.DoesNotExist:
        return False

    # check token
    try:
        exist_token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        return False

    if token != exist_token.key:
        return False
    return True


@csrf_exempt
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
            print "username exists."
            response['message']="username exists"
            raise ValueError
        if User.objects.filter(email=email).exists():
            print "email exists."
            response['message']="email exists"
            raise ValueError

        new_user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
        token=Token.objects.create(user=new_user)
        new_user_profile = UserProfile(user = new_user)
        new_user_profile.save()

        UserObjectPermission.objects.assign_perm('full_access', user=new_user, obj = new_user_profile)

        response['success']=True
        response['message']="success"
        response['token']=token.key

    except ValueError:
        print("Value error")
        pass

    return HttpResponse(json.dumps(response))


@csrf_exempt
def account_login(request):
    """

    :param request: GET method
    :return:
    """
    response=dict()

    username = request.GET['username']
    password = request.GET['password']

    user=authenticate(username=username, password=password)

    response['message']=""
    response['userid']=""
    response['success']=False

    if user is not None:
        print "user authenticated"
        if user.is_active:
            # login(request, user)
            response['success']=True
            response['message']="sucess"
            token = Token.objects.get(user=user)
            response['token']=token.key

        else:
            # Return a 'disabled account' error message
            response['message']="disabled account"

    else:
        # Return an 'invalid login' error message.
        print "invalid login"
        response['message']="invalid login"


    return HttpResponse(json.dumps(response))


@csrf_exempt
@server_auth
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

    return HttpResponse(json.dumps(response))
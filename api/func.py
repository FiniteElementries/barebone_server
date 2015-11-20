import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from guardian.models import UserObjectPermission

from userprofile.models import UserProfile
import sys

def error_response(error, response=None):
    if not response:
        response = dict()

    response['message'] = error
    response['success'] = False
    # return json.dumps(response)
    return HttpResponse(json.dumps(response))


@csrf_exempt
def create_account(request):
    """
    :param request: json format '{"username": "username_value",
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

        new_user_profile = UserProfile(user = new_user)
        new_user_profile.save()

        UserObjectPermission.objects.assign_perm('full_access', user=new_user, obj = new_user_profile)

        response['success']=True
        response['message']="success"
    except ValueError:
        print("Value error")
        pass

    return HttpResponse(json.dumps(response))


@csrf_exempt
def account_login(request):
    response=dict()

    username= request.GET['username']
    password= request.GET['password']

    user=authenticate(username=username, password=password)

    response['message']=""
    response['userid']=""
    response['success']=False

    if user is not None:
        print "user authenticated"
        if user.is_active:
            login(request, user)
            response['success']=True
            response['message']="sucess"
        else:
            # Return a 'disabled account' error message
            response['message']="disabled account"

    else:
        # Return an 'invalid login' error message.
        print "invalid login"
        response['message']="invalid login"


    return HttpResponse(json.dumps(response))
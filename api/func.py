import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

from userprofile.models import UserProfile


def errorResponse(error, response=None):
    if not response:
        response = dict()

    response['error'] = error
    response['success'] = False
    return json.dumps(response)
    # return HttpResponse(json.dumps(response))


def login(request):
    response=dict()

    serialized=json.loads(request)

    username=serialized['username']
    password=serialized['password']

    user=authenticate(username=username, password=password)


    if user is not None:
        if user.is_active:
            login(request, user)
            response['success']=True
        else:
            # Return a 'disabled account' error message
            response['success']=False
    else:
        # Return an 'invalid login' error message.
        response['success']=False

    return json.dumps(response)
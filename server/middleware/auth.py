
from django.conf import settings
from django.contrib.auth.models import User
from helper.http_handler import error_response
from django.http import HttpResponse

from helper.auth import verify_token

class ServerAuth(object):

    def process_request(self, request):

        if request.method == 'GET':
            return error_response("Please use POST")

        try:
            username = request.POST['username']
        except:
            return error_response("Please provide username")

        try:
            password = request.POST['password']

            print password
            return None  # do nothing, user is trying to login
        except:
            pass

        try:
            token = request.POST['token']
        except:
            return error_response("Please provide username and access token for authentication")

        if not (username and token):
            return error_response("Something is wrong")

        authorized = verify_token(username=username, token=token)

        if authorized==1:
            user=User.objects.get(username=username)
            request.user=user
            return None
        elif authorized==-1:
            return error_response("expired token")
        elif authorized==0:
            return error_response("Authentication error")

        return None
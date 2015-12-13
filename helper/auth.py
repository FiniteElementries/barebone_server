from django.contrib.auth.models import User
from helper.http_handler import error_response
from rest_framework.authtoken.models import Token


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

        if not (username and token):
            return error_response("Please provide username and access token for authentication")

        authorized = verify_token(username=username, token=token)

        if authorized:
            user=User.objects.get(username=username)
            request.user=user
            return original_function(request)
        else:
            return error_response("Authentication error")
    return wrapper


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
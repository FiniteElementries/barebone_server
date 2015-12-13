import json
from django.http import HttpResponse


def error_response(error, response=None):
    if not response:
        response = dict()

    response['message'] = error
    response['success'] = False

    return HttpResponse(json.dumps(response))
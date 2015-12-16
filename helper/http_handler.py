import json
from django.http import HttpResponse
import json

def error_response(error, response=None):
    if not response:
        response = dict()

    response['message'] = error
    response['success'] = False

    return HttpResponse(json.dumps(response))



def loadJson(bytes):
    return json.loads(bytes.decode('UTF-8'))
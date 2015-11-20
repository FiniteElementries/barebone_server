import json

def loadJson(bytes):
    return json.loads(bytes.decode('UTF-8'))
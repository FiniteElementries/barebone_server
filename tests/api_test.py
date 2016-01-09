import urllib
import urllib2
import json
import requests

import time

client="http://192.168.0.10:8000/api"
# client="http://127.0.0.1:8000/api"

def loadJson(bytes):
    return json.loads(bytes.decode('UTF-8'))


def fetch_url(url, params, method):
    params = urllib.urlencode(params)
    if method=="GET":
        f = urllib.urlopen(url+"?"+params)
    else:
        # Usually a POST
        f = urllib.urlopen(url, params)

    response = json.loads(f.read())

    return response


def testCreate_Account(username):
    print("================")
    print("create user account")

    api="/account/create/"

    url=client+api

    password="12345"
    email=username + "@mail.com"

    values={'username': username,
            'password': password,
            'email': email}

    response = fetch_url(url,values,"POST")

    print "success", response['success']
    print "message", response['message']

def testLogin(username, password):
    print("================")
    print("log user in")

    api="/account/login"

    url=client+api



    values={'username': username,
            'password': password}

    response = fetch_url(url,values,"POST")

    print "success", response['success']
    print "message", response['message']
    print "token", response['token']
    return response['token']

def testGetUserInfo(username, token, target_username):
    print("================")
    print("Get user all info")

    api="/userprofile/info"

    url=client+api

    values={'username': username,
            'token': token,
            'target_username': target_username}



    response = fetch_url(url,values,"POST")

    print "success?", response['success']
    print "message?", response['message']
    print "package", response['package']
    # print 'first_name', response['first_name']
    # print 'last_name', response['last_name']
    # print 'about_me', response['about_me']

def testLogUserout(username, token):
    print("================")
    print("log user out")

    api="/account/logout"

    url=client+api

    values={'username': username,
            'token': token}

    response = fetch_url(url,values,"POST")

    print "success", response['success']
    print "message", response['message']

def get_follower_list(username, token):
    print("================")
    print("get follower list")

    api="/userprofile/friends/list"

    url=client+api

    values={'username': username,
            'token': token}

    response = fetch_url(url,values,"POST")

    print "success", response['success']
    print response
    print response['package']

def change_password(username, token):

    print("================")
    print("change pwd")

    api="/account/change_password"

    url=client+api

    username="first_user"

    values={'username': username,
            'token': token,
            'old_password': "12345",
            'new_password': "54321"}

    response = fetch_url(url,values,"POST")

    print "success", response['success']
    print response


def add_follower(username, token, target_username, action):

    print("================")
    print("add friend")

    api="/userprofile/friends/change"

    url=client+api

    values={'username': username,
            'token': token,
            'target_username':target_username,
            'action': action}

    response = fetch_url(url,values,"POST")

    print "success", response['success']
    print response

def change_user_info(username, token, field_name, field_value):

    print("================")
    print("change user info")

    api="/userprofile/change_info"

    url=client+api

    package=dict()
    package[field_name]=field_value

    values={'username': username,
            'token': token,
            'package':package,
            }

    response = fetch_url(url,values,"POST")

    print "success", response['success']
    print response

#
# testCreate_Account("user1")
# testCreate_Account("user2")
# testCreate_Account("user3")

token1=testLogin("user1", "12345")
# change_user_info(username="user1",token=token1,field_name='about_me', field_value="hey i changed my description")

# add_follower("user1", token1, "user2", "follow")
#
# token3=testLogin("user3", "12345")
# add_follower("user3", token3, "user2", "follow")
#
# token2=testLogin("user2", "12345")
# get_follower_list("user2", token2)


testGetUserInfo("user1", token1, "user1")
# testGetUserInfo("user2", token2, "user1")

# check token expiry
# time.sleep(2)
# testGetUserInfo("user1", token1, "user2")


testLogUserout("user1",token1)
# testLogUserout("user2",token2)

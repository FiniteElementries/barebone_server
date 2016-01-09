from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import json
from helper.http_handler import loadJson

from django.contrib.auth.models import User
from userprofile.models import UserProfile

# Create your tests here.
class UserDetailsTests(TestCase):
    def setUp(self):
        print("================")
        print("setup test users")
        user = User.objects.create(first_name="first_user1", last_name="last", email="email", username='asfasf')
        self.userProfile = UserProfile.objects.create(user=user,phone_number="2211265")

        user2 = User.objects.create(first_name="first2", last_name="last2", email="email2", username='aq1fqwq')
        self.userProfile2 = UserProfile.objects.create( user=user2,phone_number="4662521")


class UserAccountTests(TestCase):
    def setUp(self):
        self.testCreate_Account()
        # client=Client()
        # username="first_user"
        # password="12345"
        # email="test@mail.com"
        #
        # test_user = User.objects.create_user(username, email, password)

    def testCreate_Account(self):
        print("================")
        print("create user account")

        client=Client()

        username="first_user"
        password="12345"
        email="test@mail.com"

        response = client.post('/account/create/',{'username':username, 'password':password, 'email':email})

        response = loadJson(response.content)

        print "success", response['success']

    def testLogin(self):
        print("================")
        print("log user in")
        client=Client()

        username="first_user"
        password="12345"
        email="test@mail.com"


        response = client.get('/account/login/',{'username': username, 'password': password})
        response = loadJson(response.content)
        print "login success: ", response['success']

    # def testUserGeneric(self):
    #     print("================")
    #     print("Get user generic")
    #     client=Client()
    #
    #     username="first_user"
    #
    #     response = client.get('/userprofile/overview/',{'username': username})
    #     response = loadJson(response.content)
    #
    #     print "success: ", response['success']
    #     print "message: ", response['message']

    def testGetUserAll(self):

        print("================")
        print("Get user all info")


        self.testLogin()

        client=Client()

        username="first_user"
        print username
        response = client.get('/userprofile/detail/', {'username': username})
        response = loadJson(response.content)

        print "success: ", response['success']
        print "message: ", response['message']